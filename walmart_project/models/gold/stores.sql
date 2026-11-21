{{
    config(
        materialized='table',
        schema='gold'
    )
}}
select
store_id,
store_name,
city,
province,
country,
created_timestamp,
updated_timestamp,
is_active
from 
{{source("walmart_database", "stores")}}