SELECT 
    order_id,
    is_late_delivery,
    days_to_deliver,
    delay_in_days,
    product_category_name_english,
    seller_state,
    customer_state,
    review_score
FROM {{ ref('int_delivery_analysis') }}
