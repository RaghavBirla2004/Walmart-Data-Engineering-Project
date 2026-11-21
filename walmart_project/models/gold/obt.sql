{{
    config(
        materialized='table',
        schema='gold'
    )
}}

SELECT
    -- Orders fields
    o.order_id,
    o.customer_id,
    o.store_id,
    o.order_timestamp,
    o.payment_method,
    o.order_status,
    o.total_amount,
    o.created_timestamp AS order_created_timestamp,
    o.updated_timestamp AS order_updated_timestamp,
    o.is_active AS order_is_active,

    -- Customers fields
    c.first_name AS customer_first_name,
    c.last_name AS customer_last_name,
    c.email AS customer_email,
    c.phone AS customer_phone,
    c.city AS customer_city,
    c.province AS customer_province,
    c.country AS customer_country,
    c.created_timestamp AS customer_created_timestamp,
    c.updated_timestamp AS customer_updated_timestamp,
    c.is_active AS customer_is_active,

    -- Order Items fields
    oi.order_item_id,
    oi.product_id,
    oi.quantity,
    oi.unit_price,
    oi.line_amount,
    oi.created_timestamp AS order_item_created_timestamp,
    oi.updated_timestamp AS order_item_updated_timestamp,
    oi.is_active AS order_item_is_active,

    -- Products fields
    p.product_name,
    p.category AS product_category,
    p.brand AS product_brand,
    p.price AS product_price,
    p.created_timestamp AS product_created_timestamp,
    p.updated_timestamp AS product_updated_timestamp,
    p.is_active AS product_is_active,

    -- Stores fields
    s.store_name,
    s.city AS store_city,
    s.province AS store_province,
    s.country AS store_country,
    s.created_timestamp AS store_created_timestamp,
    s.updated_timestamp AS store_updated_timestamp,
    s.is_active AS store_is_active,

    -- Employees fields
    e.employee_id,
    e.first_name AS employee_first_name,
    e.last_name AS employee_last_name,
    e.email AS employee_email,
    e.job_title AS employee_job_title,
    e.salary AS employee_salary,
    e.created_timestamp AS employee_created_timestamp,
    e.updated_timestamp AS employee_updated_timestamp,
    e.is_active AS employee_is_active

FROM {{ ref('orders_bronze') }} AS o
LEFT JOIN {{ ref('customers_bronze') }} AS c
    ON o.customer_id = c.customer_id
LEFT JOIN {{ ref('order_item_bronze') }} AS oi
    ON o.order_id = oi.order_id
LEFT JOIN {{ ref('products') }} AS p
    ON oi.product_id = p.product_id
LEFT JOIN {{ ref('stores') }} AS s
    ON o.store_id = s.store_id
LEFT JOIN {{ ref('employees_bronze') }} AS e
    ON s.store_id = e.store_id

