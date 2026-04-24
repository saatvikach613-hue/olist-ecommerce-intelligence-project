
  create view "postgres"."analytics"."stg_reviews__dbt_tmp"
    
    
  as (
    SELECT 
    review_id,
    order_id,
    review_score,
    review_comment_title,
    review_comment_message,
    CAST(review_creation_date AS TIMESTAMP) AS creation_date,
    CAST(review_answer_timestamp AS TIMESTAMP) AS answer_timestamp
FROM "postgres"."raw"."olist_order_reviews"
  );