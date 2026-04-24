SELECT COUNT(*) 
FROM "postgres"."analytics"."int_orders_enriched" 
WHERE delivered_customer_date < purchase_timestamp