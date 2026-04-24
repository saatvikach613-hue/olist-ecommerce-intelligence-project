-- Create Dimension Tables

CREATE TABLE IF NOT EXISTS analytics.dim_customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    city VARCHAR(100),
    state VARCHAR(50),
    region VARCHAR(50) -- Engineered: North/Northeast/Southeast/South/Central-West
);

CREATE TABLE IF NOT EXISTS analytics.dim_products (
    product_id VARCHAR(50) PRIMARY KEY,
    category_name_english VARCHAR(100),
    weight_g INT,
    volume_cm3 INT,
    price_band VARCHAR(20) -- Engineered: Low/Mid/High/Premium based on NTILE
);

CREATE TABLE IF NOT EXISTS analytics.dim_sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_city VARCHAR(100),
    seller_state VARCHAR(50),
    seller_tenure_days INT -- Engineered from first order date
);

CREATE TABLE IF NOT EXISTS analytics.dim_date (
    date_key INT PRIMARY KEY, -- Format YYYYMMDD
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20),
    week_of_year INT,
    day_of_week INT,
    is_weekend BOOLEAN
);

-- Create Fact Table

CREATE TABLE IF NOT EXISTS analytics.fact_orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) REFERENCES analytics.dim_customers(customer_id),
    seller_id VARCHAR(50) REFERENCES analytics.dim_sellers(seller_id),
    product_id VARCHAR(50) REFERENCES analytics.dim_products(product_id),
    order_date_key INT REFERENCES analytics.dim_date(date_key),
    delivery_date_key INT REFERENCES analytics.dim_date(date_key),
    payment_value DECIMAL(10, 2),
    freight_value DECIMAL(10, 2),
    review_score INT,
    days_to_deliver INT,
    is_late_delivery BOOLEAN
);

-- Add Indexes for Query Performance

CREATE INDEX IF NOT EXISTS idx_fact_orders_customer_id ON analytics.fact_orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_fact_orders_seller_id ON analytics.fact_orders(seller_id);
CREATE INDEX IF NOT EXISTS idx_fact_orders_product_id ON analytics.fact_orders(product_id);
CREATE INDEX IF NOT EXISTS idx_fact_orders_order_date_key ON analytics.fact_orders(order_date_key);
CREATE INDEX IF NOT EXISTS idx_fact_orders_delivery_date_key ON analytics.fact_orders(delivery_date_key);
