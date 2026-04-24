
  create view "postgres"."analytics"."int_customer_rfm__dbt_tmp"
    
    
  as (
    WITH customer_orders AS (
    SELECT 
        c.customer_unique_id,
        c.customer_id,
        o.purchase_timestamp,
        o.payment_value,
        o.order_id
    FROM "postgres"."analytics"."stg_customers" c
    JOIN "postgres"."analytics"."int_orders_enriched" o ON c.customer_id = o.customer_id
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
  );