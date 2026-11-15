{{
    config(
        materialized='incremental',
        unique_key='employee_id'
    )
}}



select
employee_id,
store_id,
first_name,
last_name,
email,
job_title,
salary,
created_timestamp,
updated_timestamp,
is_active
from 
{{source("walmart_database", "employees")}}

{% if is_incremental() %}

WHERE updated_timestamp > (SELECT coalesce(MAX(updated_timestamp), '1900-01-01') FROM {{ this }})

{% endif %}

