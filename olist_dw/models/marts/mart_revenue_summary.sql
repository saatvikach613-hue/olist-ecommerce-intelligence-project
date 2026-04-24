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
