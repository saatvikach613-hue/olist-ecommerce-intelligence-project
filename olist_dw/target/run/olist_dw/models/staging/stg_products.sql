
  create view "postgres"."analytics"."stg_products__dbt_tmp"
    
    
  as (
    SELECT 
    p.product_id,
    p.product_category_name,
    t.product_category_name_english,
    p.product_name_lenght AS product_name_length,
    p.product_description_lenght AS product_description_length,
    p.product_photos_qty,
    p.product_weight_g AS weight_g,
    p.product_length_cm AS length_cm,
    p.product_height_cm AS height_cm,
    p.product_width_cm AS width_cm
FROM "postgres"."raw"."olist_products" p
LEFT JOIN "postgres"."raw"."product_category_name_translation" t
  ON p.product_category_name = t.product_category_name
WHERE p.product_id IS NOT NULL
  );