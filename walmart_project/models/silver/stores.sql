{{
    config(
        materialized='incremental',
        unique_key='store_id'
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

{% if is_incremental() %}

WHERE updated_timestamp > (SELECT coalesce(MAX(updated_timestamp), '1900-01-01') FROM {{ this }})

{% endif %}

