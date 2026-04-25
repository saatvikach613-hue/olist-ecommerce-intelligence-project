import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestClassifier
import joblib

load_dotenv()

# Connect to Database
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Load Data
query = "SELECT total_spend, total_orders, days_since_last_order, churn_risk_flag FROM analytics.mart_customer_segments;"
df = pd.read_sql(query, engine).dropna()

X = df[['total_spend', 'total_orders', 'days_since_last_order']]
y = df['churn_risk_flag']

# Train Model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)

# Save Model
os.makedirs('models', exist_ok=True)
joblib.dump(clf, 'models/churn_model.joblib')
print("✅ Model saved to models/churn_model.joblib")
