select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      SELECT COUNT(*) 
FROM "postgres"."analytics"."stg_reviews" 
WHERE review_score NOT BETWEEN 1 AND 5
      
    ) dbt_internal_test