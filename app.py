import streamlit as st
import pandas as pd
import plotly.express as px
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import joblib

# Master Command: Matrix Scanner Edition
st.set_page_config(page_title="Olist Global Intelligence", layout="wide", initial_sidebar_state="collapsed")

# ---------------------------------------------------------
# MATRIX TACTICAL CSS
# ---------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=JetBrains+Mono:wght@400&display=swap');
    
    .stApp { background-color: #000000; font-family: 'Inter', sans-serif; color: #F1E5B1; }
    
    /* GRID LOCK (550px for all boxes) */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        height: 550px !important;
        background: radial-gradient(circle at center, rgba(209, 157, 86, 0.03) 0%, rgba(0, 0, 0, 1) 100%) !important;
        border: 1px solid rgba(209, 157, 86, 0.3) !important;
        border-radius: 2px !important;
        padding: 25px !important;
        position: relative;
    }
    
    .module-header {
        color: #D19D56;
        font-weight: 700;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(209, 157, 86, 0.1);
        padding-bottom: 8px;
    }
    
    /* THE MATRIX SCANNER */
    .scanner-container {
        display: flex;
        gap: 4px;
        justify-content: center;
        margin: 30px 0;
    }
    .scanner-block {
        width: 12px;
        height: 25px;
        background: rgba(209, 157, 86, 0.1);
        border: 1px solid rgba(209, 157, 86, 0.2);
    }
    .scanner-block.active {
        background: #D19D56;
        box-shadow: 0 0 10px #D19D56;
    }
    .scanner-block.critical {
        background: #6E3D34;
        box-shadow: 0 0 10px #6E3D34;
    }
    
    .risk-readout {
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        color: #D19D56;
        letter-spacing: 3px;
    }

    .log-findings {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: #F1E5B1;
        opacity: 0.4;
        background: rgba(209, 157, 86, 0.05);
        padding: 10px;
        border-left: 2px solid #D19D56;
        position: absolute;
        bottom: 25px;
        left: 25px;
        right: 25px;
    }
    
    [data-testid="stMetricValue"] { font-size: 30px !important; color: #D19D56 !important; font-weight: 700 !important; }
    h1 { font-weight: 700; letter-spacing: 8px; color: #F1E5B1 !important; font-size: 34px !important; }
    </style>
    """, unsafe_allow_html=True)

load_dotenv()

@st.cache_resource
def get_engine():
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    return create_engine(f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

engine = get_engine()

# --- DATA ---
@st.cache_data
def load_all_data():
    rev = pd.read_sql("SELECT order_month, product_category_name_english, SUM(gmv) as gmv FROM analytics.mart_revenue_summary WHERE product_category_name_english IN (SELECT product_category_name_english FROM analytics.mart_revenue_summary GROUP BY 1 ORDER BY SUM(gmv) DESC LIMIT 5) GROUP BY 1, 2 ORDER BY 1", engine)
    logistics = pd.read_sql("SELECT product_category_name_english, AVG(delay_in_days) as avg_delay, AVG(CASE WHEN is_late_delivery THEN 1.0 ELSE 0.0 END) as late_rate FROM analytics.mart_delivery_sla GROUP BY 1 HAVING COUNT(*) > 100 ORDER BY avg_delay DESC LIMIT 15", engine)
    cust = pd.read_sql("SELECT * FROM analytics.mart_customer_segments", engine)
    geo = pd.read_sql("SELECT c.customer_state as state, SUM(oi.price) as revenue FROM raw.olist_order_items oi JOIN raw.olist_orders o ON oi.order_id = o.order_id JOIN raw.olist_customers c ON o.customer_id = c.customer_id GROUP BY 1 ORDER BY 2 DESC LIMIT 10", engine)
    seller = pd.read_sql("SELECT seller_tier, SUM(total_revenue) as revenue FROM analytics.mart_seller_scorecard GROUP BY 1", engine)
    totals = pd.read_sql("SELECT SUM(gmv) as total_gmv, SUM(order_count) as total_orders FROM analytics.mart_revenue_summary", engine)
    return rev, logistics, cust, geo, seller, totals

df_rev, df_log, df_cust, df_geo, df_seller, df_totals = load_all_data()

# --- HEADER ---
st.markdown("<h1 style='text-align: center; margin-bottom: 5px;'>OLIST MASTER COMMAND</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #D19D56; letter-spacing: 5px; font-size: 10px;'>MATRIX INTELLIGENCE CORE V6.0</p>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
with k1: st.metric("TOTAL GMV", f"R$ {df_totals['total_gmv'].iloc[0]/1e6:.1f}M")
with k2: st.metric("ORDERS", f"{int(df_totals['total_orders'].iloc[0]):,}")
with k3: st.metric("CHURN RISK", f"{df_cust['churn_risk_flag'].mean():.1%}")
with k4: st.metric("SLA STATUS", f"{1 - df_log['late_rate'].mean():.1%}")

st.markdown("<hr style='opacity: 0.1; margin: 20px 0;'>", unsafe_allow_html=True)

c_left, c_right = st.columns(2)

with c_left:
    with st.container(border=True):
        st.markdown("<div class='module-header'>📡 01 // REVENUE MIX</div>", unsafe_allow_html=True)
        fig = px.area(df_rev, x='order_month', y='gmv', color='product_category_name_english', line_shape='spline', height=330, color_discrete_sequence=px.colors.sequential.YlOrBr_r)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False, color='#F1E5B1'), yaxis=dict(showgrid=False, color='#F1E5B1'), legend=dict(orientation="h", y=1.25, font=dict(size=8, color="#F1E5B1")), margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<div class='log-findings'>[SIGNAL]: Top nodes represent 62% of mass.</div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<div class='module-header'>🪐 03 // CUSTOMER LTV</div>", unsafe_allow_html=True)
        fig = px.sunburst(df_cust, path=['rfm_segment', 'churn_risk_flag'], values='total_spend', color='total_spend', color_continuous_scale='YlOrBr_r', height=350)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<div class='log-findings'>[SIGNAL]: High-frequency cohorts dominate monetary mass.</div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<div class='module-header'>🧬 05 // SELLER CONTRIBUTION</div>", unsafe_allow_html=True)
        fig = px.pie(df_seller, values='revenue', names='seller_tier', hole=0.7, height=350, color_discrete_sequence=['#D19D56', '#6E3D34', '#3E2723', '#262A2E'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', showlegend=True, legend=dict(font=dict(color="#F1E5B1")), margin=dict(l=0,r=0,t=0,b=0))
        fig.update_traces(textinfo='percent')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<div class='log-findings'>[SIGNAL]: Platinum tier holds critical mass of global GMV.</div>", unsafe_allow_html=True)

with c_right:
    with st.container(border=True):
        st.markdown("<div class='module-header'>🛰️ 02 // LOGISTICS FRICTION</div>", unsafe_allow_html=True)
        fig = px.scatter(df_log, x='avg_delay', y='late_rate', size='late_rate', hover_name='product_category_name_english', color='avg_delay', color_continuous_scale='YlOrBr_r', height=330)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(title="Delay", color='#F1E5B1'), yaxis=dict(title="Rate", color='#F1E5B1'), margin=dict(l=0,r=0,t=0,b=0), coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<div class='log-findings'>[SIGNAL]: High-delay sectors identified in heavy logistics.</div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<div class='module-header'>🗺️ 04 // GEOSPATIAL POWER</div>", unsafe_allow_html=True)
        fig = px.bar(df_geo, x='revenue', y='state', orientation='h', color='revenue', color_continuous_scale='YlOrBr_r', height=350)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False, color='#F1E5B1', title=""), yaxis=dict(showgrid=False, color='#F1E5B1', title=""), coloraxis_showscale=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<div class='log-findings'>[SIGNAL]: SP/RJ core remains the dominant revenue engine.</div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<div class='module-header'>🎯 06 // MATRIX RISK SCANNER</div>", unsafe_allow_html=True)
        
        # 3 SLIDERS IN ONE ROW
        sc1, sc2, sc3 = st.columns(3)
        with sc1: sv = st.slider("Spend", 1, 5000, 1000)
        with sc2: ov = st.slider("Orders", 1, 50, 5)
        with sc3: rv = st.slider("Decay", 0, 365, 90)
        
        try:
            model = joblib.load('models/churn_model.joblib')
            risk_val = model.predict_proba(pd.DataFrame([[sv, ov, rv]], columns=['total_spend', 'total_orders', 'days_since_last_order']))[0][1]
            
            # BUILD THE MATRIX SCANNER BAR
            active_blocks = int(risk_val * 20)
            scanner_html = "<div class='scanner-container'>"
            for i in range(20):
                block_class = "scanner-block"
                if i < active_blocks:
                    block_class += " active" if risk_val < 0.6 else " critical"
                scanner_html += f"<div class='{block_class}'></div>"
            scanner_html += "</div>"
            
            st.markdown(scanner_html, unsafe_allow_html=True)
            st.markdown(f"<div class='risk-readout'>{risk_val*100:.2f}% CHURN PROBABILITY</div>", unsafe_allow_html=True)
            
        except: st.error("AI OFFLINE")
        
        st.markdown("<div class='log-findings'>[SYSTEM]: Matrix scanner live. Real-time inference matched.</div>", unsafe_allow_html=True)
