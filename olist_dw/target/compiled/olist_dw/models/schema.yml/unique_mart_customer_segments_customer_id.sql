
    
    

select
    customer_id as unique_field,
    count(*) as n_records

from "postgres"."analytics"."mart_customer_segments"
where customer_id is not null
group by customer_id
having count(*) > 1


