# 🛰️ Olist E-Commerce Intelligence: Professional Command Center

An end-to-end, high-fidelity Business Intelligence and Machine Learning suite built for the Brazilian Olist ecosystem. This project moves beyond static reporting to provide a real-time, cloud-connected "Tactical Command Center" for executive decision-making.

![Olist Dashboard](https://img.shields.io/badge/Project-Production--Ready-gold?style=for-the-badge)
![Database](https://img.shields.io/badge/DB-AWS_RDS_PostgreSQL-blue?style=for-the-badge)
![Modeling](https://img.shields.io/badge/Modeling-dbt_Analytics_Marts-orange?style=for-the-badge)

---

## 📈 1. Business Problem & Solution
The Olist dataset (100k+ orders) presents a classic "High-Volume, High-Friction" e-commerce scenario. The primary challenges are **Logistics Latency** across the massive Brazilian geography and **Customer Retention** in a competitive marketplace.

**The Solution:** This project implements a **Cloud Data Warehouse** architecture using AWS RDS, processes data through a **dbt modular transformation layer**, and serves insights via a **Machine Learning-integrated Streamlit dashboard**.

---

## 🏗️ 2. The Data Architecture
This project follows a professional **Modern Data Stack** architecture:
1. **Raw Layer**: 9 relational CSV files ingested into **AWS RDS PostgreSQL**.
2. **Transformation Layer (dbt)**: 
   - **Staging**: Cleaning and schema standardization.
   - **Marts**: Complex analytical models for Revenue, Customer RFM, Seller Scorecards, and Delivery SLAs.
3. **Intelligence Layer**: A **Random Forest Classifier** trained on behavioral features to forecast churn risk.
4. **Presentation Layer**: A bespoke Streamlit HUD with custom CSS-injected "Matrix Scanner."

---

## 💎 3. The "Big Six" Intelligence Modules

### **🛰️ 01. Revenue Composition**
- **Logic**: Time-series analysis of GMV using Spline-Area smoothing.
- **Impact**: Visualizes "Share of Wallet" across the top 5 product categories, identifying seasonal expansion and contraction.

### **🚀 02. Logistics Friction Hotspots**
- **Logic**: Multi-dimensional bubble mapping of `avg_delay` vs. `late_delivery_rate`.
- **Impact**: pinpoints the exact product categories causing supply chain bottlenecks, enabling targeted carrier optimization.

### **🪐 03. Customer Universe (RFM)**
- **Logic**: Recency, Frequency, and Monetary (RFM) segmentation using a sunburst hierarchy.
- **Impact**: Provides a deep-dive into Customer Lifetime Value (LTV) cohorts, separating "Champions" from "At-Risk" segments.

### **🗺️ 04. Geospatial Revenue Power**
- **Logic**: Aggregated revenue ranking by Brazilian State.
- **Impact**: Identifies the geographic "Power Centers" (SP, RJ, MG) and quantifies regional market dominance.

### **🧬 05. Seller Revenue Contribution**
- **Logic**: Concentration analysis across Platinum, Gold, and Silver seller tiers.
- **Impact**: Identifies "Single-Point-of-Failure" risks where a tiny % of sellers drive the majority of GMV.

### **🎯 06. Strategy Simulation Engine**
- **Logic**: Live-responsive inference using a pre-trained **Random Forest** model.
- **Impact**: Allows executives to simulate "What-If" scenarios by adjusting Spend and Decay sliders to see real-time Churn Probability.

---

## 🤖 4. Machine Learning Implementation
The churn model was developed using **Scikit-learn** and focuses on three primary behavioral features:
- `total_spend`: Cumulative monetary contribution.
- `total_orders`: Interaction frequency.
- `days_since_last_order`: Recency/Decay factor.

The model is persisted using **Joblib** and served via an optimized "Matrix Scanner" UI for instant tactical feedback.

---

## 🚀 5. Technical Setup & Deployment

### **Prerequisites**
- Python 3.9+
- AWS RDS Instance (PostgreSQL)
- dbt Core (for model rebuilding)

### **Installation**
1. **Clone & Environment**:
   ```bash
   git clone https://github.com/saatvikach613-hue/olist-ecommerce-intelligence-project.git
   cd olist-ecommerce-intelligence-project
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Database Configuration**:
   Create a `.env` file in the root directory:
   ```env
   DB_HOST=your-aws-endpoint.rds.amazonaws.com
   DB_NAME=postgres
   DB_USER=your-user
   DB_PASSWORD=your-password
   DB_PORT=5432
   ```
3. **Execution**:
   ```bash
   streamlit run app.py
   ```

---
**Developed by Chokkapu Saatvika | Olist BI Ecosystem V2.0**
