
    
    

with all_values as (

    select
        rfm_segment as value_field,
        count(*) as n_records

    from "postgres"."analytics"."mart_customer_segments"
    group by rfm_segment

)

select *
from all_values
where value_field not in (
    'Champions','Loyal','At-Risk','Lost'
)


