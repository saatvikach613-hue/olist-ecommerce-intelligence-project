
  create view "postgres"."analytics"."stg_payments__dbt_tmp"
    
    
  as (
    SELECT 
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value
FROM "postgres"."raw"."olist_order_payments"
  );