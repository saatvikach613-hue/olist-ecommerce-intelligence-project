SELECT COUNT(*) 
FROM {{ ref('mart_revenue_summary') }} 
WHERE gmv < 0
