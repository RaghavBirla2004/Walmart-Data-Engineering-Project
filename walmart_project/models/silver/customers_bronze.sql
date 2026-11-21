{{
    config(
        materialized='incremental',
        unique_key='customer_id',
        schema='silver'
    )
}}



select
customer_id,
first_name,
last_name,
email,
phone,
city,
province,
country,
created_timestamp,
updated_timestamp,
is_active
from 
{{source("walmart_database", "customers")}}

{% if is_incremental() %}

WHERE updated_timestamp > (SELECT coalesce(MAX(updated_timestamp), '1900-01-01') FROM {{ this }})

{% endif %}

QUALIFY ROW_NUMBER() OVER (
    PARTITION BY customer_id
    ORDER BY updated_timestamp DESC
) = 1