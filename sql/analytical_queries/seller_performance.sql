-- Seller Performance Scorecard

WITH seller_stats AS (
    SELECT 
        s.seller_id,
        s.seller_state,
        SUM(f.payment_value) AS total_revenue,
        COUNT(f.order_id) AS total_orders,
        COUNT(CASE WHEN f.is_late_delivery = TRUE THEN 1 END) AS late_deliveries,
        AVG(f.review_score) AS avg_review_score
    FROM analytics.fact_orders f
    JOIN analytics.dim_sellers s ON f.seller_id = s.seller_id
    GROUP BY s.seller_id, s.seller_state
)
SELECT 
    seller_id,
    seller_state,
    total_revenue,
    RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank,
    ROUND(late_deliveries::numeric / NULLIF(total_orders, 0), 4) AS late_delivery_rate,
    ROUND(avg_review_score, 2) AS avg_review_score,
    NTILE(4) OVER (ORDER BY total_revenue DESC) AS seller_tier
FROM seller_stats
ORDER BY revenue_rank;
