import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

sql_file = 'sql/ddl/02_power_bi_views.sql'

try:
    conn = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        autocommit=True
    )
    
    with open(sql_file, 'r') as f:
        sql = f.read()
        
    with conn.cursor() as cur:
        cur.execute(sql)
        print("✅ Power BI views created successfully in PostgreSQL.")
            
    conn.close()
except Exception as e:
    print(f"❌ Failed to create views. Error: {e}")
