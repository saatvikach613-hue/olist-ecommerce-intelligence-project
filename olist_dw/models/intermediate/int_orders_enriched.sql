SELECT 
    o.order_id,
    o.customer_id,
    o.order_status,
    o.purchase_timestamp,
    o.delivered_customer_date,
    o.estimated_delivery_date,
    EXTRACT(EPOCH FROM (o.delivered_customer_date - o.purchase_timestamp))/86400 AS days_to_deliver,
    o.delivered_customer_date > o.estimated_delivery_date AS is_late_delivery,
    i.product_id,
    i.seller_id,
    i.price,
    i.freight_value,
    p.payment_value,
    p.payment_type,
    r.review_score
FROM {{ ref('stg_orders') }} o
LEFT JOIN {{ ref('stg_order_items') }} i ON o.order_id = i.order_id
LEFT JOIN {{ ref('stg_payments') }} p ON o.order_id = p.order_id
LEFT JOIN {{ ref('stg_reviews') }} r ON o.order_id = r.order_id
