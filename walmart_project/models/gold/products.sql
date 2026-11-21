{{
    config(
        materialized='table',
        schema='gold'
    )
}}

select
product_id,
product_name,
category,
brand,
price,
created_timestamp,
updated_timestamp,
is_active
from 
{{source("walmart_database", "products")}}