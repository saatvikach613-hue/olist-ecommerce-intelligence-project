SELECT COUNT(*) 
FROM {{ ref('stg_reviews') }} 
WHERE review_score NOT BETWEEN 1 AND 5
