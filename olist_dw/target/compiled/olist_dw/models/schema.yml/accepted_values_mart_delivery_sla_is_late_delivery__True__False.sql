
    
    

with all_values as (

    select
        is_late_delivery as value_field,
        count(*) as n_records

    from "postgres"."analytics"."mart_delivery_sla"
    group by is_late_delivery

)

select *
from all_values
where value_field not in (
    'True','False'
)


