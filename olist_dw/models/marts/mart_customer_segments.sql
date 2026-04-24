SELECT 
    customer_unique_id AS customer_id,
    rfm_segment,
    total_spend,
    total_orders,
    days_since_last_order,
    churn_risk_flag
FROM {{ ref('int_customer_rfm') }}
