select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select gmv
from "postgres"."analytics"."mart_revenue_summary"
where gmv is null



      
    ) dbt_internal_test