import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import glob

# Load environment variables
load_dotenv()

# Build connection string
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# SQLAlchemy URL for psycopg3
DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def main():
    print("Connecting to database...")
    engine = create_engine(DATABASE_URL)
    
    # Create schemas if they don't exist
    try:
        with engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS analytics;"))
            conn.commit()
        print("Schemas 'raw' and 'analytics' verified/created.")
    except Exception as e:
        print(f"Error creating schemas: {e}")
        return

    # Find all CSVs in the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_files = glob.glob(os.path.join(project_root, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {project_root}!")
        return

    print(f"Found {len(csv_files)} CSV files to ingest.")
    
    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        # clean table name (e.g. olist_orders_dataset.csv -> olist_orders)
        table_name = file_name.replace('_dataset.csv', '').replace('.csv', '')
        
        print(f"Processing {file_name} -> raw.{table_name}...")
        
        try:
            # Read CSV
            df = pd.read_csv(file_path)
            
            # Idempotent write: replace table if exists
            df.to_sql(
                name=table_name,
                con=engine,
                schema='raw',
                if_exists='replace',
                index=False
            )
            print(f"✅ Loaded {len(df)} rows into raw.{table_name}")
        except Exception as e:
            print(f"❌ Failed to load {file_name}. Error: {e}")

if __name__ == "__main__":
    main()
