{{
    config(
        materialized='table',
        schema='gold'
    )
}}

select
order_id,
customer_id,
store_id,
order_timestamp,
payment_method,
order_status,
total_amount,
created_timestamp,
updated_timestamp,
is_active
from 
{{source("walmart_database", "orders")}}