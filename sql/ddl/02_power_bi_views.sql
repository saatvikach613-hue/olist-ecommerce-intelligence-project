-- This view combines dbt Marts with ML Predictions for easier Power BI ingestion
CREATE OR REPLACE VIEW analytics.vw_powerbi_customer_insights AS
SELECT 
    c.customer_id,
    c.rfm_segment,
    c.total_spend,
    c.total_orders,
    c.days_since_last_order,
    ml.predicted_churn_risk,
    ml.actual_churn_risk
FROM analytics.mart_customer_segments c
LEFT JOIN analytics.ml_churn_predictions ml ON c.customer_id = ml.customer_id;

-- View for Revenue and Category Analysis
CREATE OR REPLACE VIEW analytics.vw_powerbi_revenue_performance AS
SELECT * FROM analytics.mart_revenue_summary;

-- View for Delivery SLA Analysis
CREATE OR REPLACE VIEW analytics.vw_powerbi_delivery_sla AS
SELECT * FROM analytics.mart_delivery_sla;
