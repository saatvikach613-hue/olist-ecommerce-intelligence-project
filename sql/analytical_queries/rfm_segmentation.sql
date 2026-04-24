-- RFM Segmentation Query using the Star Schema

WITH rfm_base AS (
    SELECT 
        c.customer_id,
        MAX(d.full_date) AS last_order_date,
        COUNT(DISTINCT f.order_id) AS frequency,
        SUM(f.payment_value) AS monetary
    FROM analytics.fact_orders f
    JOIN analytics.dim_customers c ON f.customer_id = c.customer_id
    JOIN analytics.dim_date d ON f.order_date_key = d.date_key
    GROUP BY c.customer_id
),
rfm_scoring AS (
    SELECT 
        customer_id,
        last_order_date,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY last_order_date ASC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
    FROM rfm_base
)
SELECT 
    customer_id,
    last_order_date,
    frequency,
    monetary,
    (r_score + f_score + m_score) AS rfm_score,
    CASE 
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At-Risk'
        ELSE 'Lost'
    END AS rfm_segment
FROM rfm_scoring;
