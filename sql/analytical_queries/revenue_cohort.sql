-- Revenue Cohort & Retention Analysis

WITH customer_first_purchase AS (
    SELECT 
        f.customer_id,
        MIN(d.full_date) AS first_purchase_date
    FROM analytics.fact_orders f
    JOIN analytics.dim_date d ON f.order_date_key = d.date_key
    GROUP BY f.customer_id
),
cohort_base AS (
    SELECT 
        c.customer_id,
        DATE_TRUNC('month', cfp.first_purchase_date) AS acquisition_month,
        DATE_TRUNC('month', d.full_date) AS order_month,
        f.payment_value
    FROM analytics.fact_orders f
    JOIN customer_first_purchase cfp ON f.customer_id = cfp.customer_id
    JOIN analytics.dim_date d ON f.order_date_key = d.date_key
),
cohort_months AS (
    SELECT 
        acquisition_month,
        EXTRACT(MONTH FROM AGE(order_month, acquisition_month)) + 1 AS cohort_month,
        SUM(payment_value) AS total_revenue,
        COUNT(DISTINCT customer_id) AS active_customers
    FROM cohort_base
    GROUP BY acquisition_month, EXTRACT(MONTH FROM AGE(order_month, acquisition_month)) + 1
)
SELECT 
    acquisition_month,
    cohort_month,
    total_revenue,
    active_customers,
    LAG(active_customers) OVER (PARTITION BY acquisition_month ORDER BY cohort_month) AS prev_month_customers,
    ROUND(active_customers::numeric / NULLIF(LAG(active_customers) OVER (PARTITION BY acquisition_month ORDER BY cohort_month), 0), 4) AS retention_rate
FROM cohort_months
ORDER BY acquisition_month, cohort_month;
