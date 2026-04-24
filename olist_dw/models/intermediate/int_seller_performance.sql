SELECT 
    seller_id,
    COUNT(DISTINCT order_id) AS total_order_count,
    SUM(payment_value) AS total_revenue,
    AVG(review_score) AS average_review_score,
    COUNT(CASE WHEN is_late_delivery THEN 1 END)::FLOAT / NULLIF(COUNT(order_id), 0) AS late_delivery_rate
FROM {{ ref('int_orders_enriched') }}
WHERE seller_id IS NOT NULL
GROUP BY seller_id
