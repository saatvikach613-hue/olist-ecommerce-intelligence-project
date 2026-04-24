import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    print("SUCCESS: Connection to AWS RDS PostgreSQL was successful!")
    conn.close()
except Exception as e:
    print(f"FAILED: Could not connect to database. Error: {e}")
