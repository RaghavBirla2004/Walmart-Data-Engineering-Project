{{
    config(
        materialized='incremental',
        unique_key='order_item_id',
        schema='silver'
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

{% if is_incremental() %}

WHERE updated_timestamp > (SELECT coalesce(MAX(updated_timestamp), '1900-01-01') FROM {{ this }})

{% endif %}

QUALIFY ROW_NUMBER() OVER (
    PARTITION BY order_item_id
    ORDER BY updated_timestamp DESC
) = 1

