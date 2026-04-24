-- Late Delivery Root Cause Analysis

WITH category_delays AS (
    SELECT 
        p.category_name_english,
        COUNT(f.order_id) AS total_orders,
        COUNT(CASE WHEN f.is_late_delivery = TRUE THEN 1 END) AS late_orders,
        AVG(f.days_to_deliver) AS avg_days_to_deliver
    FROM analytics.fact_orders f
    JOIN analytics.dim_products p ON f.product_id = p.product_id
    GROUP BY p.category_name_english
),
state_delays AS (
    SELECT 
        s.seller_state,
        COUNT(f.order_id) AS total_orders,
        COUNT(CASE WHEN f.is_late_delivery = TRUE THEN 1 END) AS late_orders,
        AVG(f.days_to_deliver) AS avg_days_to_deliver
    FROM analytics.fact_orders f
    JOIN analytics.dim_sellers s ON f.seller_id = s.seller_id
    GROUP BY s.seller_state
)
SELECT 
    'Category' AS dimension_type,
    category_name_english AS dimension_value,
    ROUND(late_orders::numeric / NULLIF(total_orders, 0), 4) AS late_delivery_rate,
    ROUND(avg_days_to_deliver, 1) AS avg_delay_days
FROM category_delays
WHERE total_orders > 100

UNION ALL

SELECT 
    'Seller State' AS dimension_type,
    seller_state AS dimension_value,
    ROUND(late_orders::numeric / NULLIF(total_orders, 0), 4) AS late_delivery_rate,
    ROUND(avg_days_to_deliver, 1) AS avg_delay_days
FROM state_delays
WHERE total_orders > 100
ORDER BY late_delivery_rate DESC;
