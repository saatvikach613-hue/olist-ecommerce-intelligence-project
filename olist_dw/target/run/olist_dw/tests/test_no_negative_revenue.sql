select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      SELECT COUNT(*) 
FROM "postgres"."analytics"."mart_revenue_summary" 
WHERE gmv < 0
      
    ) dbt_internal_test