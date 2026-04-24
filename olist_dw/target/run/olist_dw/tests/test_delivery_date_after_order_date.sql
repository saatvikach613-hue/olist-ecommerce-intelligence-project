select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      SELECT COUNT(*) 
FROM "postgres"."analytics"."int_orders_enriched" 
WHERE delivered_customer_date < purchase_timestamp
      
    ) dbt_internal_test