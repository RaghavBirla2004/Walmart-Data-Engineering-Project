{{
    config(
        materialized='table',
        schema='gold'
    )
}}

select
order_item_id,
order_id,
product_id,
quantity,
unit_price,
line_amount,
created_timestamp,
updated_timestamp,
is_active
from 
{{source("walmart_database", "order_items")}}