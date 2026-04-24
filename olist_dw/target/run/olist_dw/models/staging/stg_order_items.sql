
  create view "postgres"."analytics"."stg_order_items__dbt_tmp"
    
    
  as (
    SELECT 
    order_id,
    order_item_id,
    product_id,
    seller_id,
    CAST(shipping_limit_date AS TIMESTAMP) AS shipping_limit_date,
    price,
    freight_value
FROM "postgres"."raw"."olist_order_items"
  );