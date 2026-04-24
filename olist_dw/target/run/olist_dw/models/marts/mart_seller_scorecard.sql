
  
    

  create  table "postgres"."analytics"."mart_seller_scorecard__dbt_tmp"
  
  
    as
  
  (
    SELECT 
    sp.seller_id,
    sp.total_revenue,
    sp.total_order_count,
    sp.late_delivery_rate,
    sp.average_review_score,
    CASE 
        WHEN sp.late_delivery_rate > 0.2 THEN TRUE 
        ELSE FALSE 
    END AS sla_breach_flag,
    NTILE(4) OVER (ORDER BY sp.total_revenue DESC) AS seller_tier
FROM "postgres"."analytics"."int_seller_performance" sp
  );
  