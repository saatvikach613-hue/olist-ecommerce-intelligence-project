# Olist Data Quality Notes

During the initial exploration of the Olist E-Commerce dataset, the following data quality issues and structural notes were identified:

## Missing Values
- **`olist_order_reviews`**: 
  - Significant missing values in `review_comment_title` (~88% missing) and `review_comment_message` (~58% missing).
  - The `review_score` itself is fully populated, but text analysis will have gaps.
- **`olist_orders`**:
  - `order_approved_at`, `order_delivered_carrier_date`, and `order_delivered_customer_date` contain missing values, specifically for canceled or unavailable orders. This must be handled in the dbt staging models.
- **`olist_products`**:
  - A small percentage (~1.8%) of products are missing `product_category_name`, along with their physical dimensions and weight.

## Structural Notes
- **Timestamps**: Most date columns are provided as strings and must be explicitly cast to `TIMESTAMP` in dbt or during ingestion to enable time-series analysis.
- **Foreign Keys**: 
  - Some `product_id` values in `olist_order_items` may not exist in `olist_products` due to dataset trimming.
  - Some `customer_id` values in `olist_orders` map uniquely to `customer_unique_id` in `olist_customers`, meaning `customer_id` is actually an order-specific customer token.
- **Geolocation**: The `olist_geolocation` table contains over 1 million rows, with many duplicated zip code prefixes. A deduplication strategy (e.g., taking the average lat/lng per zip code) will be necessary in the dbt intermediate layer before joining to customers or sellers.
