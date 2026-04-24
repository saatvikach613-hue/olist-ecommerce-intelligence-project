
  create view "postgres"."analytics"."int_delivery_analysis__dbt_tmp"
    
    
  as (
    SELECT 
    o.order_id,
    o.is_late_delivery,
    o.days_to_deliver,
    EXTRACT(EPOCH FROM (o.delivered_customer_date - o.estimated_delivery_date))/86400 AS delay_in_days,
    p.product_category_name_english,
    s.state AS seller_state,
    c.state AS customer_state,
    o.review_score
FROM "postgres"."analytics"."int_orders_enriched" o
LEFT JOIN "postgres"."analytics"."stg_products" p ON o.product_id = p.product_id
LEFT JOIN "postgres"."analytics"."stg_sellers" s ON o.seller_id = s.seller_id
LEFT JOIN "postgres"."analytics"."stg_customers" c ON o.customer_id = c.customer_id
WHERE o.delivered_customer_date IS NOT NULL
  );