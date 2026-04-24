import nbformat as nbf
import os

os.makedirs('notebooks', exist_ok=True)

# ---------------------------------------------------------
# Notebook 1: Exploratory Data Analysis
# ---------------------------------------------------------
nb1 = nbf.v4.new_notebook()

nb1.cells = [
    nbf.v4.new_markdown_cell("# Exploratory Data Analysis (EDA)\nIn this notebook, we connect to our PostgreSQL data warehouse and visualize key business metrics from the `analytics` schema built by dbt."),
    nbf.v4.new_code_cell("""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv('../.env')

# Connect to Database
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
"""),
    nbf.v4.new_markdown_cell("## 1. Monthly Revenue Trend\nVisualizing the Gross Merchandise Value (GMV) over time."),
    nbf.v4.new_code_cell("""
query_revenue = "SELECT order_month, SUM(gmv) as total_gmv FROM analytics.mart_revenue_summary GROUP BY order_month ORDER BY order_month;"
df_rev = pd.read_sql(query_revenue, engine)

plt.figure(figsize=(12, 6))
sns.lineplot(data=df_rev, x='order_month', y='total_gmv', marker='o')
plt.title('Monthly Gross Merchandise Value (GMV)')
plt.ylabel('GMV (BRL)')
plt.xlabel('Month')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
"""),
    nbf.v4.new_markdown_cell("## 2. Customer RFM Segments\nVisualizing the distribution of customer segments based on our RFM model."),
    nbf.v4.new_code_cell("""
query_rfm = "SELECT rfm_segment, COUNT(customer_id) as count FROM analytics.mart_customer_segments GROUP BY rfm_segment;"
df_rfm = pd.read_sql(query_rfm, engine)

plt.figure(figsize=(8, 8))
plt.pie(df_rfm['count'], labels=df_rfm['rfm_segment'], autopct='%1.1f%%', colors=sns.color_palette('pastel'))
plt.title('Customer RFM Segments Distribution')
plt.show()
"""),
    nbf.v4.new_markdown_cell("## 3. Late Delivery Analysis\nAnalyzing how many days orders were delayed past their estimated delivery date."),
    nbf.v4.new_code_cell("""
query_delivery = "SELECT delay_in_days FROM analytics.mart_delivery_sla WHERE is_late_delivery = true AND delay_in_days IS NOT NULL;"
df_del = pd.read_sql(query_delivery, engine)

plt.figure(figsize=(10, 6))
sns.histplot(df_del['delay_in_days'], bins=50, kde=True, color='red')
plt.title('Distribution of Delay in Days (For Late Orders)')
plt.xlabel('Days Late')
plt.ylabel('Frequency')
plt.xlim(0, 50)
plt.show()
""")
]
with open('notebooks/01_exploratory_data_analysis.ipynb', 'w') as f:
    nbf.write(nb1, f)

# ---------------------------------------------------------
# Notebook 2: Predictive Modeling
# ---------------------------------------------------------
nb2 = nbf.v4.new_notebook()

nb2.cells = [
    nbf.v4.new_markdown_cell("# Customer Churn Prediction\nIn this notebook, we build an XGBoost/Random Forest model to predict customer churn based on their RFM metrics."),
    nbf.v4.new_code_cell("""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

load_dotenv('../.env')

# Connect to Database
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
"""),
    nbf.v4.new_markdown_cell("## 1. Load Data\nWe fetch the `mart_customer_segments` table. Our target variable is `churn_risk_flag`."),
    nbf.v4.new_code_cell("""
query_customers = "SELECT customer_id, total_spend, total_orders, days_since_last_order, churn_risk_flag FROM analytics.mart_customer_segments;"
df = pd.read_sql(query_customers, engine)

# Drop missing
df = df.dropna()

print(df.head())
print("\\nTarget Distribution:")
print(df['churn_risk_flag'].value_counts(normalize=True))
"""),
    nbf.v4.new_markdown_cell("## 2. Train Model\nWe split the data and train a Random Forest classifier."),
    nbf.v4.new_code_cell("""
X = df[['total_spend', 'total_orders', 'days_since_last_order']]
y = df['churn_risk_flag']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print("Classification Report:")
print(classification_report(y_test, y_pred))

# Plot Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()
"""),
    nbf.v4.new_markdown_cell("## 3. Feature Importance"),
    nbf.v4.new_code_cell("""
feature_imp = pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=False)

plt.figure(figsize=(8, 5))
sns.barplot(x=feature_imp, y=feature_imp.index)
plt.title('Feature Importance for Churn Prediction')
plt.xlabel('Importance Score')
plt.show()
"""),
    nbf.v4.new_markdown_cell("## 4. Export Predictions to Database\nWe will save the test set predictions back to the data warehouse."),
    nbf.v4.new_code_cell("""
df_results = X_test.copy()
df_results['customer_id'] = df.loc[X_test.index, 'customer_id']
df_results['actual_churn_risk'] = y_test
df_results['predicted_churn_risk'] = y_pred

# Save to Postgres
print("Writing predictions to analytics.ml_churn_predictions...")
df_results.to_sql('ml_churn_predictions', engine, schema='analytics', if_exists='replace', index=False)
print("Done!")
""")
]
with open('notebooks/02_predictive_modeling.ipynb', 'w') as f:
    nbf.write(nb2, f)

print("Successfully generated notebooks in notebooks/")
