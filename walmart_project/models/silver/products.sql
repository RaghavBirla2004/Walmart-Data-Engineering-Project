{{
    config(
        materialized='incremental',
        unique_key='product_id',
        schema='silver'
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

{% if is_incremental() %}

WHERE updated_timestamp > (SELECT coalesce(MAX(updated_timestamp), '1900-01-01') FROM {{ this }})

{% endif %}

