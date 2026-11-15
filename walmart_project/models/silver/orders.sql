{{
    config(
        materialized='incremental',
        unique_key='order_id',
        schema='silver'
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

{% if is_incremental() %}

WHERE updated_timestamp > (SELECT coalesce(MAX(updated_timestamp), '1900-01-01') FROM {{ this }})

{% endif %}