-- Payment Behavior Analysis

SELECT 
    p.category_name_english,
    c.state AS customer_state,
    op.payment_type,
    COUNT(f.order_id) AS total_orders,
    SUM(f.payment_value) AS total_revenue,
    AVG(op.payment_installments) AS avg_installments
FROM analytics.fact_orders f
JOIN analytics.dim_products p ON f.product_id = p.product_id
JOIN analytics.dim_customers c ON f.customer_id = c.customer_id
JOIN raw.olist_order_payments op ON f.order_id = op.order_id
GROUP BY 
    p.category_name_english,
    c.state,
    op.payment_type
ORDER BY total_revenue DESC;
