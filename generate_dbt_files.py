import os

files = {
    "olist_dw/dbt_project.yml": """
name: 'olist_dw'
version: '1.0.0'
config-version: 2
profile: 'olist_dw'
model-paths: ["models"]
test-paths: ["tests"]
macro-paths: ["macros"]
seed-paths: ["seeds"]
models:
  olist_dw:
    staging:
      +materialized: view
    intermediate:
      +materialized: view
    marts:
      +materialized: table
""",
    "olist_dw/profiles.yml": """
olist_dw:
  target: dev
  outputs:
    dev:
      type: postgres
      host: "{{ env_var('DB_HOST') }}"
      port: 5432
      user: "{{ env_var('DB_USER') }}"
      password: "{{ env_var('DB_PASSWORD') }}"
      dbname: "{{ env_var('DB_NAME') }}"
      schema: analytics
      threads: 4
""",
    "olist_dw/models/staging/sources.yml": """
version: 2
sources:
  - name: olist_raw
    schema: raw
    tables:
      - name: olist_orders
      - name: olist_customers
      - name: olist_order_items
      - name: olist_order_payments
      - name: olist_order_reviews
      - name: olist_products
      - name: olist_sellers
      - name: olist_geolocation
      - name: product_category_name_translation
""",
    "olist_dw/models/staging/stg_orders.sql": """
SELECT 
    order_id,
    customer_id,
    order_status,
    CAST(order_purchase_timestamp AS TIMESTAMP) AS purchase_timestamp,
    CAST(order_approved_at AS TIMESTAMP) AS approved_at,
    CAST(order_delivered_carrier_date AS TIMESTAMP) AS delivered_carrier_date,
    CAST(order_delivered_customer_date AS TIMESTAMP) AS delivered_customer_date,
    CAST(order_estimated_delivery_date AS TIMESTAMP) AS estimated_delivery_date
FROM {{ source('olist_raw', 'olist_orders') }}
WHERE order_id IS NOT NULL
""",
    "olist_dw/models/staging/stg_customers.sql": """
SELECT 
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix AS zip_code_prefix,
    customer_city AS city,
    customer_state AS state
FROM {{ source('olist_raw', 'olist_customers') }}
WHERE customer_id IS NOT NULL
""",
    "olist_dw/models/staging/stg_order_items.sql": """
SELECT 
    order_id,
    order_item_id,
    product_id,
    seller_id,
    CAST(shipping_limit_date AS TIMESTAMP) AS shipping_limit_date,
    price,
    freight_value
FROM {{ source('olist_raw', 'olist_order_items') }}
""",
    "olist_dw/models/staging/stg_payments.sql": """
SELECT 
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value
FROM {{ source('olist_raw', 'olist_order_payments') }}
""",
    "olist_dw/models/staging/stg_reviews.sql": """
SELECT 
    review_id,
    order_id,
    review_score,
    review_comment_title,
    review_comment_message,
    CAST(review_creation_date AS TIMESTAMP) AS creation_date,
    CAST(review_answer_timestamp AS TIMESTAMP) AS answer_timestamp
FROM {{ source('olist_raw', 'olist_order_reviews') }}
""",
    "olist_dw/models/staging/stg_products.sql": """
SELECT 
    p.product_id,
    p.product_category_name,
    t.product_category_name_english,
    p.product_name_lenght AS product_name_length,
    p.product_description_lenght AS product_description_length,
    p.product_photos_qty,
    p.product_weight_g AS weight_g,
    p.product_length_cm AS length_cm,
    p.product_height_cm AS height_cm,
    p.product_width_cm AS width_cm
FROM {{ source('olist_raw', 'olist_products') }} p
LEFT JOIN {{ source('olist_raw', 'product_category_name_translation') }} t
  ON p.product_category_name = t.product_category_name
WHERE p.product_id IS NOT NULL
""",
    "olist_dw/models/staging/stg_sellers.sql": """
SELECT 
    seller_id,
    seller_zip_code_prefix AS zip_code_prefix,
    seller_city AS city,
    seller_state AS state
FROM {{ source('olist_raw', 'olist_sellers') }}
WHERE seller_id IS NOT NULL
""",
    "olist_dw/models/intermediate/int_orders_enriched.sql": """
SELECT 
    o.order_id,
    o.customer_id,
    o.order_status,
    o.purchase_timestamp,
    o.delivered_customer_date,
    o.estimated_delivery_date,
    EXTRACT(EPOCH FROM (o.delivered_customer_date - o.purchase_timestamp))/86400 AS days_to_deliver,
    o.delivered_customer_date > o.estimated_delivery_date AS is_late_delivery,
    i.product_id,
    i.seller_id,
    i.price,
    i.freight_value,
    p.payment_value,
    p.payment_type,
    r.review_score
FROM {{ ref('stg_orders') }} o
LEFT JOIN {{ ref('stg_order_items') }} i ON o.order_id = i.order_id
LEFT JOIN {{ ref('stg_payments') }} p ON o.order_id = p.order_id
LEFT JOIN {{ ref('stg_reviews') }} r ON o.order_id = r.order_id
""",
    "olist_dw/models/intermediate/int_customer_rfm.sql": """
WITH customer_orders AS (
    SELECT 
        c.customer_unique_id,
        c.customer_id,
        o.purchase_timestamp,
        o.payment_value,
        o.order_id
    FROM {{ ref('stg_customers') }} c
    JOIN {{ ref('int_orders_enriched') }} o ON c.customer_id = o.customer_id
),
rfm_base AS (
    SELECT 
        customer_unique_id,
        MAX(purchase_timestamp) AS last_order_date,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(payment_value) AS total_spend
    FROM customer_orders
    GROUP BY customer_unique_id
),
rfm_scoring AS (
    SELECT 
        customer_unique_id,
        last_order_date,
        total_orders,
        total_spend,
        EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - last_order_date))/86400 AS days_since_last_order,
        NTILE(5) OVER (ORDER BY last_order_date ASC) AS r_score,
        NTILE(5) OVER (ORDER BY total_orders ASC) AS f_score,
        NTILE(5) OVER (ORDER BY total_spend ASC) AS m_score
    FROM rfm_base
)
SELECT 
    customer_unique_id,
    days_since_last_order,
    total_orders,
    total_spend,
    CASE 
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At-Risk'
        ELSE 'Lost'
    END AS rfm_segment,
    r_score <= 2 AS churn_risk_flag
FROM rfm_scoring
""",
    "olist_dw/models/intermediate/int_seller_performance.sql": """
SELECT 
    seller_id,
    COUNT(DISTINCT order_id) AS total_order_count,
    SUM(payment_value) AS total_revenue,
    AVG(review_score) AS average_review_score,
    COUNT(CASE WHEN is_late_delivery THEN 1 END)::FLOAT / NULLIF(COUNT(order_id), 0) AS late_delivery_rate
FROM {{ ref('int_orders_enriched') }}
WHERE seller_id IS NOT NULL
GROUP BY seller_id
""",
    "olist_dw/models/intermediate/int_delivery_analysis.sql": """
SELECT 
    o.order_id,
    o.is_late_delivery,
    o.days_to_deliver,
    EXTRACT(EPOCH FROM (o.delivered_customer_date - o.estimated_delivery_date))/86400 AS delay_in_days,
    p.product_category_name_english,
    s.state AS seller_state,
    c.state AS customer_state,
    o.review_score
FROM {{ ref('int_orders_enriched') }} o
LEFT JOIN {{ ref('stg_products') }} p ON o.product_id = p.product_id
LEFT JOIN {{ ref('stg_sellers') }} s ON o.seller_id = s.seller_id
LEFT JOIN {{ ref('stg_customers') }} c ON o.customer_id = c.customer_id
WHERE o.delivered_customer_date IS NOT NULL
""",
    "olist_dw/models/marts/mart_revenue_summary.sql": """
SELECT 
    DATE_TRUNC('month', o.purchase_timestamp) AS order_month,
    p.product_category_name_english,
    c.state AS customer_state,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(o.payment_value) AS gmv,
    SUM(o.freight_value) AS freight_value,
    AVG(o.payment_value) AS aov
FROM {{ ref('int_orders_enriched') }} o
LEFT JOIN {{ ref('stg_products') }} p ON o.product_id = p.product_id
LEFT JOIN {{ ref('stg_customers') }} c ON o.customer_id = c.customer_id
GROUP BY 1, 2, 3
""",
    "olist_dw/models/marts/mart_customer_segments.sql": """
SELECT 
    customer_unique_id AS customer_id,
    rfm_segment,
    total_spend,
    total_orders,
    days_since_last_order,
    churn_risk_flag
FROM {{ ref('int_customer_rfm') }}
""",
    "olist_dw/models/marts/mart_seller_scorecard.sql": """
SELECT 
    sp.seller_id,
    sp.total_revenue,
    sp.total_order_count,
    sp.late_delivery_rate,
    sp.average_review_score,
    CASE 
        WHEN sp.late_delivery_rate > 0.2 THEN TRUE 
        ELSE FALSE 
    END AS sla_breach_flag,
    NTILE(4) OVER (ORDER BY sp.total_revenue DESC) AS seller_tier
FROM {{ ref('int_seller_performance') }} sp
""",
    "olist_dw/models/marts/mart_delivery_sla.sql": """
SELECT 
    order_id,
    is_late_delivery,
    days_to_deliver,
    delay_in_days,
    product_category_name_english,
    seller_state,
    customer_state,
    review_score
FROM {{ ref('int_delivery_analysis') }}
""",
    "olist_dw/models/schema.yml": """
version: 2
models:
  - name: mart_revenue_summary
    description: "Monthly GMV and AOV summary for executive dashboard"
    columns:
      - name: order_month
        description: "Month of purchase"
      - name: gmv
        description: "Gross Merchandise Value"
        tests:
          - not_null
  - name: mart_customer_segments
    description: "Customer level table with RFM segments"
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      - name: rfm_segment
        tests:
          - accepted_values:
              values: ['Champions', 'Loyal', 'At-Risk', 'Lost']
  - name: mart_seller_scorecard
    description: "Seller performance and SLA monitoring"
    columns:
      - name: seller_id
        tests:
          - unique
          - not_null
  - name: mart_delivery_sla
    description: "Order level delivery performance"
    columns:
      - name: is_late_delivery
        tests:
          - accepted_values:
              values: [true, false]
""",
    "olist_dw/tests/test_no_negative_revenue.sql": """
SELECT COUNT(*) 
FROM {{ ref('mart_revenue_summary') }} 
WHERE gmv < 0
""",
    "olist_dw/tests/test_delivery_date_after_order_date.sql": """
SELECT COUNT(*) 
FROM {{ ref('int_orders_enriched') }} 
WHERE delivered_customer_date < purchase_timestamp
""",
    "olist_dw/tests/test_review_score_range.sql": """
SELECT COUNT(*) 
FROM {{ ref('stg_reviews') }} 
WHERE review_score NOT BETWEEN 1 AND 5
"""
}

for path, content in files.items():
    with open(path, "w") as f:
        f.write(content.strip() + "\n")
print("All dbt files created successfully.")
