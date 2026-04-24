
  create view "postgres"."analytics"."stg_customers__dbt_tmp"
    
    
  as (
    SELECT 
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix AS zip_code_prefix,
    customer_city AS city,
    customer_state AS state
FROM "postgres"."raw"."olist_customers"
WHERE customer_id IS NOT NULL
  );