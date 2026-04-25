"""
OLIST INTELLIGENCE COMMAND CENTER v2
Blue-Purple Tactical Theme
Author: Saatvika Chokkapu | MS Business Analytics, UTD
"""

import os
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="OLIST INTELLIGENCE",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: #03010a !important;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(100, 50, 255, 0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(0, 120, 255, 0.06) 0%, transparent 50%),
        linear-gradient(rgba(100, 50, 255, 0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(100, 50, 255, 0.015) 1px, transparent 1px);
    background-size: auto, auto, 50px 50px, 50px 50px;
    font-family: 'Rajdhani', sans-serif;
    color: #c8c8e8;
}

#MainMenu, footer, header, .stDeployButton { visibility: hidden; display: none; }
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-thumb { background: #6432ff; border-radius: 2px; }

/* ── HEADER ── */
.cmd-header {
    background: linear-gradient(135deg, #03010a 0%, #0a0518 50%, #03010a 100%);
    border: 1px solid rgba(100, 50, 255, 0.4);
    border-top: 2px solid #7b4fff;
    border-bottom: 2px solid #0078ff;
    padding: 22px 32px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.cmd-header::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 60%; height: 1px;
    background: linear-gradient(90deg, transparent, #7b4fff, #0078ff, transparent);
    animation: scan 4s linear infinite;
}
@keyframes scan { to { left: 200%; } }

.cmd-title {
    font-family: 'Orbitron', monospace;
    font-size: 26px;
    font-weight: 900;
    background: linear-gradient(135deg, #7b4fff, #0078ff, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 5px;
    text-transform: uppercase;
}
.cmd-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    color: rgba(123, 79, 255, 0.5);
    letter-spacing: 3px;
    margin-top: 5px;
}
.badge {
    display: inline-block;
    background: rgba(123, 79, 255, 0.12);
    border: 1px solid rgba(123, 79, 255, 0.35);
    color: #9b6fff;
    font-family: 'Share Tech Mono', monospace;
    font-size: 9px;
    padding: 3px 10px;
    letter-spacing: 2px;
    margin-right: 6px;
    margin-top: 10px;
}
.badge-blue {
    background: rgba(0, 120, 255, 0.12);
    border-color: rgba(0, 120, 255, 0.35);
    color: #4499ff;
}

/* ── KPI CARDS ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 10px;
    margin-bottom: 28px;
}
.kpi {
    background: linear-gradient(135deg, #06021a 0%, #0a0520 100%);
    border: 1px solid rgba(123, 79, 255, 0.25);
    border-top: 2px solid;
    padding: 16px 14px;
    position: relative;
    min-height: 110px;
}
.kpi::before {
    content: '';
    position: absolute;
    top: 5px; left: 5px;
    width: 7px; height: 7px;
    border-top: 1px solid;
    border-left: 1px solid;
    border-color: inherit;
    opacity: 0.6;
}
.kpi::after {
    content: '';
    position: absolute;
    bottom: 5px; right: 5px;
    width: 7px; height: 7px;
    border-bottom: 1px solid;
    border-right: 1px solid;
    border-color: inherit;
    opacity: 0.6;
}
.kpi-purple { border-top-color: #7b4fff; border-color: rgba(123,79,255,0.25); }
.kpi-blue   { border-top-color: #0078ff; border-color: rgba(0,120,255,0.25); }
.kpi-cyan   { border-top-color: #00d4ff; border-color: rgba(0,212,255,0.25); }
.kpi-red    { border-top-color: #ff3b6b; border-color: rgba(255,59,107,0.25); }
.kpi-amber  { border-top-color: #ffaa00; border-color: rgba(255,170,0,0.25); }

.kpi-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 9px;
    color: rgba(180, 160, 255, 0.5);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.kpi-val {
    font-family: 'Orbitron', monospace;
    font-size: 22px;
    font-weight: 700;
    line-height: 1;
}
.kpi-note {
    font-family: 'Share Tech Mono', monospace;
    font-size: 9px;
    margin-top: 6px;
    opacity: 0.6;
}

/* ── SECTION TITLE ── */
.sec {
    font-family: 'Orbitron', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    padding: 8px 0 6px;
    border-bottom: 1px solid rgba(123, 79, 255, 0.2);
    margin-bottom: 14px;
    background: linear-gradient(90deg, #7b4fff, #0078ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ── CHART POD ── */
.pod {
    background: #06021a;
    border: 1px solid rgba(123, 79, 255, 0.18);
    padding: 14px;
    position: relative;
    margin-bottom: 14px;
}
.pod::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 18px; height: 18px;
    border-top: 2px solid #7b4fff;
    border-left: 2px solid #7b4fff;
}
.pod::after {
    content: '';
    position: absolute;
    bottom: 0; right: 0;
    width: 18px; height: 18px;
    border-bottom: 2px solid #0078ff;
    border-right: 2px solid #0078ff;
}
.pod-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    color: rgba(123, 79, 255, 0.6);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
    padding-left: 22px;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #03010a;
    border-bottom: 1px solid rgba(123,79,255,0.2);
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    color: rgba(123,79,255,0.4);
    background: transparent;
    border: none;
    padding: 10px 20px;
    text-transform: uppercase;
}
.stTabs [aria-selected="true"] {
    color: #9b6fff !important;
    border-bottom: 2px solid #7b4fff !important;
    background: rgba(123,79,255,0.06) !important;
}

/* ── VERDICT ── */
.verdict {
    border: 1px solid;
    padding: 24px;
    text-align: center;
    font-family: 'Orbitron', monospace;
    position: relative;
    overflow: hidden;
}
.verdict::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--vc), transparent);
}
.v-nom  { --vc: #7b4fff; border-color: rgba(123,79,255,0.6); background: radial-gradient(ellipse at center, rgba(123,79,255,0.1), #03010a); }
.v-warn { --vc: #ffaa00; border-color: rgba(255,170,0,0.6);  background: radial-gradient(ellipse at center, rgba(255,170,0,0.1),  #03010a); animation: pulse-warn 2s infinite; }
.v-crit { --vc: #ff3b6b; border-color: rgba(255,59,107,0.6); background: radial-gradient(ellipse at center, rgba(255,59,107,0.12), #03010a); animation: pulse-crit 1.2s infinite; }
@keyframes pulse-warn { 0%,100%{box-shadow:0 0 8px rgba(255,170,0,0.2)} 50%{box-shadow:0 0 22px rgba(255,170,0,0.5)} }
@keyframes pulse-crit { 0%,100%{box-shadow:0 0 8px rgba(255,59,107,0.3)} 50%{box-shadow:0 0 28px rgba(255,59,107,0.7)} }

/* ── DIVIDER ── */
.div {
    border: none;
    border-top: 1px solid rgba(123,79,255,0.12);
    margin: 20px 0;
}

/* ── FOOTER ── */
.footer {
    border-top: 1px solid rgba(123,79,255,0.15);
    margin-top: 36px;
    padding: 14px 0;
    display: flex;
    justify-content: space-between;
    font-family: 'Share Tech Mono', monospace;
    font-size: 9px;
    color: rgba(123,79,255,0.3);
    letter-spacing: 2px;
}
</style>
""", unsafe_allow_html=True)

# ── Colours ───────────────────────────────────────────────────────
PURPLE = "#7b4fff"
BLUE   = "#0078ff"
CYAN   = "#00d4ff"
RED    = "#ff3b6b"
AMBER  = "#ffaa00"
PINK   = "#ff44cc"

PLOTLY = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Share Tech Mono, monospace", color="#665588", size=10),
    margin=dict(l=8, r=8, t=32, b=8),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#776699", size=10)),
    xaxis=dict(gridcolor="rgba(123,79,255,0.06)", color="#554477", showline=False, tickfont=dict(size=10)),
    yaxis=dict(gridcolor="rgba(123,79,255,0.06)", color="#554477", showline=False, tickfont=dict(size=10)),
)

def title_style(color=PURPLE):
    return dict(text="", font=dict(family="Share Tech Mono", color=color, size=10), x=0.01, y=0.98)

# ── DB ────────────────────────────────────────────────────────────
@st.cache_resource
def get_engine():
    url = os.getenv("DATABASE_URL", "")
    if not url:
        h = os.getenv("DB_HOST","localhost"); p = os.getenv("DB_PORT","5432")
        d = os.getenv("DB_NAME","olist_dw");  u = os.getenv("DB_USER","postgres")
        pw= os.getenv("DB_PASSWORD","")
        url = f"postgresql+psycopg2://{u}:{pw}@{h}:{p}/{d}"
    kwargs = {"connect_args":{"sslmode":"require"}} if "rds.amazonaws.com" in url else {}
    return create_engine(url, **kwargs)

@st.cache_data(ttl=300)
def q(_eng, sql):
    with _eng.connect() as c:
        return pd.read_sql(text(sql), c)

@st.cache_resource
def load_model():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models","churn_model.joblib")
    return joblib.load(p) if os.path.exists(p) else None

def fc(v):
    if v>=1e6: return f"R${v/1e6:.1f}M"
    if v>=1e3: return f"R${v/1e3:.1f}K"
    return f"R${v:.0f}"

def kpi(label, val, note="", color=PURPLE):
    cls = {PURPLE:"kpi kpi-purple", BLUE:"kpi kpi-blue", CYAN:"kpi kpi-cyan", RED:"kpi kpi-red", AMBER:"kpi kpi-amber"}.get(color,"kpi kpi-purple")
    n = "<div class=\"kpi-note\" style=\"color:" + color + "\">" + note + "</div>" if note else ""
    return "<div class=\"" + cls + "\"><div class=\"kpi-label\">" + label + "</div><div class=\"kpi-val\" style=\"color:" + color + "\">" + str(val) + "</div>" + n + "</div>"

# ── Load data ─────────────────────────────────────────────────────
try:
    eng     = get_engine()
    rev_df  = q(eng, "SELECT * FROM analytics.mart_revenue_summary")
    cust_df = q(eng, "SELECT * FROM analytics.mart_customer_segments")
    sell_df = q(eng, "SELECT * FROM analytics.mart_seller_scorecard")
    sla_df  = q(eng, "SELECT * FROM analytics.mart_delivery_sla")
    try:    churn_df = q(eng, "SELECT * FROM analytics.ml_churn_predictions")
    except: churn_df = pd.DataFrame()
    DB_OK = True
except Exception as e:
    DB_OK = False
    np.random.seed(42)
    months = pd.date_range("2016-09","2018-08",freq="MS")
    rev_df = pd.DataFrame({"order_month":months,
        "gmv":np.abs(np.random.normal(500000,120000,len(months))).cumsum()/np.arange(1,len(months)+1)*500000/500000,
        "total_orders":np.random.randint(3000,8000,len(months)),
        "aov":np.random.normal(120,20,len(months)).clip(60),
        "product_category_name_english":np.random.choice(["Electronics","Fashion","Home","Sports","Beauty"],len(months)),
        "customer_state":np.random.choice(["SP","RJ","MG","RS","PR"],len(months)),
        "freight_value":np.random.normal(40000,8000,len(months)).clip(10000),
    })
    # realistic GMV growth
    rev_df["gmv"] = np.linspace(50000,1500000,len(months)) + np.random.normal(0,80000,len(months))
    rev_df["gmv"] = rev_df["gmv"].clip(0)
    n=10000
    segs = ["Champions","Loyal","At-Risk","Lost","New"]
    cust_df = pd.DataFrame({"customer_id":[f"C{i:05d}" for i in range(n)],
        "rfm_segment":np.random.choice(segs,n,p=[0.15,0.25,0.20,0.15,0.25]),
        "total_spend":np.random.exponential(300,n).clip(10,5000),
        "total_orders":np.random.randint(1,15,n),
        "days_since_last_order":np.random.randint(1,365,n),
        "churn_label":np.random.binomial(1,0.35,n),
        "churn_probability":np.random.beta(2,5,n),
        "customer_state":np.random.choice(["SP","RJ","MG","RS","PR"],n),
    })
    sell_df = pd.DataFrame({"seller_id":[f"S{i:04d}" for i in range(500)],
        "total_revenue":np.random.exponential(15000,500).clip(500),
        "total_orders":np.random.randint(10,500,500),
        "late_delivery_rate":np.random.beta(2,8,500),
        "avg_review_score":np.random.normal(4.0,0.6,500).clip(1,5),
        "seller_tier":np.random.choice(["Platinum","Gold","Silver","Bronze"],500),
        "seller_state":np.random.choice(["SP","RJ","MG","RS","PR"],500),
    })
    sla_df = pd.DataFrame({"order_id":[f"O{i:06d}" for i in range(50000)],
        "is_late_delivery":np.random.binomial(1,0.08,50000).astype(bool),
        "days_to_deliver":np.random.normal(12,5,50000).clip(1,60),
        "review_score":np.random.choice([1,2,3,4,5],50000,p=[0.05,0.08,0.12,0.30,0.45]),
        "product_category_name_english":np.random.choice(["Electronics","Fashion","Home","Sports","Beauty","Garden","Toys","Books","Tools","Health"],50000),
        "seller_state":np.random.choice(["SP","RJ","MG","RS","PR","SC","BA","GO","PE","CE"],50000),
        "freight_value":np.random.exponential(20,50000).clip(2),
        "payment_value":np.random.exponential(150,50000).clip(10),
    })
    churn_df = cust_df[["customer_id","churn_probability","churn_label"]].copy()

# ── KPIs ──────────────────────────────────────────────────────────
total_gmv    = rev_df["gmv"].sum() if "gmv" in rev_df.columns else 0
total_orders = int(rev_df["order_count"].sum()) if "order_count" in rev_df.columns else len(sla_df)
aov          = total_gmv / max(total_orders,1)
late_pct     = sla_df["is_late_delivery"].mean()*100 if "is_late_delivery" in sla_df.columns else 8.2
churn_rate   = cust_df["churn_risk_flag"].astype(float).mean()*100 if "churn_risk_flag" in cust_df.columns else 35.0
repeat_rate  = (cust_df["total_orders"]>1).mean()*100 if "total_orders" in cust_df.columns else 0
at_risk_rev  = cust_df.loc[cust_df.get("rfm_segment","")=="At-Risk","total_spend"].sum() if "rfm_segment" in cust_df.columns else 0

# ── HEADER ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="cmd-header">
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <div>
      <div class="cmd-title">⬡ OLIST INTELLIGENCE</div>
      <div class="cmd-sub">EXECUTIVE COMMAND CENTER — BRAZILIAN E-COMMERCE ANALYTICS</div>
      <div style="margin-top:6px;">
        <span class="badge">▶ {'LIVE · AWS RDS' if DB_OK else 'DEMO MODE'}</span>
        <span class="badge">dbt 11 MODELS</span>
        <span class="badge badge-blue">RANDOM FOREST ML</span>
        <span class="badge badge-blue">100K+ ORDERS</span>
      </div>
    </div>
    <div style="text-align:right;font-family:'Share Tech Mono',monospace;font-size:9px;color:rgba(123,79,255,0.35);line-height:1.8;letter-spacing:2px;">
      <div>DATASET · OLIST ECOMMERCE</div>
      <div>COVERAGE · 2016 – 2018</div>
      <div>PIPELINE · CSV → dbt → ML → STREAMLIT</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI STRIP ─────────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-grid">
  {kpi("TOTAL GMV",      fc(total_gmv),       "gross merchandise value", PURPLE)}
  {kpi("TOTAL ORDERS",   f"{int(total_orders):,}", "all time",           BLUE)}
  {kpi("AVG ORDER",      fc(aov),             "per transaction",         CYAN)}
  {kpi("LATE DELIVERY",  f"{late_pct:.1f}%",  "SLA breach rate",        RED if late_pct>10 else AMBER)}
  {kpi("CHURN RATE",     f"{churn_rate:.1f}%","customer attrition",      RED if churn_rate>40 else AMBER)}
  {kpi("REPEAT BUYERS",  f"{repeat_rate:.1f}%","2+ orders",              PURPLE)}
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────
t1,t2,t3,t4,t5 = st.tabs(["◈  EXECUTIVE","◈  CUSTOMERS","◈  SELLERS","◈  LOGISTICS","◈  AI ENGINE"])

# ══ TAB 1 — EXECUTIVE ════════════════════════════════════════════
with t1:
    st.markdown('<div class="sec">▸ REVENUE COMMAND</div>', unsafe_allow_html=True)
    c1,c2 = st.columns([3,1])
    with c1:
        if "order_month" in rev_df.columns and "gmv" in rev_df.columns:
            m = rev_df.groupby("order_month")["gmv"].sum().reset_index().sort_values("order_month")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=m["order_month"].astype(str), y=m["gmv"],
                mode="lines", line=dict(color=PURPLE,width=2.5,shape="spline"),
                fill="tozeroy", fillcolor="rgba(123,79,255,0.07)", name="GMV",
                hovertemplate="<b>%{x}</b><br>GMV: R$%{y:,.0f}<extra></extra>"
            ))
            fig.update_layout(**PLOTLY, height=240,
                title=dict(text="MONTHLY GMV TRAJECTORY", font=dict(family="Share Tech Mono",color=PURPLE,size=10), x=0.01))
            st.plotly_chart(fig, width='stretch')

    with c2:
        if "product_category_name_english" in rev_df.columns and "gmv" in rev_df.columns:
            cat = rev_df.groupby("product_category_name_english")["gmv"].sum().nlargest(6).reset_index()
            fig = go.Figure(go.Bar(
                x=cat["gmv"], y=cat["product_category_name_english"], orientation="h",
                marker=dict(color=[PURPLE,BLUE,CYAN,"#aa66ff","#0099ff",PINK][:len(cat)]),
                text=[fc(v) for v in cat["gmv"]],
                textfont=dict(family="Share Tech Mono",size=9,color="#fff"),
                hovertemplate="<b>%{y}</b><br>R$%{x:,.0f}<extra></extra>"
            ))
            fig.update_layout(**PLOTLY, height=240,
                title=dict(text="TOP CATEGORIES", font=dict(family="Share Tech Mono",color=BLUE,size=10), x=0.01))
            st.plotly_chart(fig, width='stretch')

    st.markdown('<hr class="div">', unsafe_allow_html=True)
    c3,c4 = st.columns(2)

    with c3:
        st.markdown('<div class="sec">▸ REVENUE BY STATE</div>', unsafe_allow_html=True)
        if "customer_state" in rev_df.columns and "gmv" in rev_df.columns:
            sr = rev_df.groupby("customer_state")["gmv"].sum().reset_index().nlargest(10,"gmv")
            fig = go.Figure(go.Bar(
                x=sr["customer_state"], y=sr["gmv"],
                marker=dict(color=sr["gmv"],
                    colorscale=[[0,"#0d0030"],[0.4,PURPLE],[1,CYAN]],
                    line=dict(color="rgba(123,79,255,0.4)",width=0.5)),
                text=[fc(v) for v in sr["gmv"]], textposition="outside",
                textfont=dict(family="Share Tech Mono",size=9,color=CYAN),
            ))
            fig.update_layout(**PLOTLY, height=230)
            st.plotly_chart(fig, width='stretch')

    with c4:
        st.markdown('<div class="sec">▸ REVIEW SCORE DISTRIBUTION</div>', unsafe_allow_html=True)
        rd = sla_df["review_score"].value_counts().sort_index()
        fig = go.Figure(go.Bar(
            x=[str(i) for i in rd.index], y=rd.values,
            marker=dict(color=[RED,AMBER,"#886699",BLUE,PURPLE][:len(rd)]),
            text=rd.values,
            textfont=dict(family="Share Tech Mono",size=10,color="#fff"),
        ))
        fig.update_layout(**PLOTLY, height=230,
            title=dict(text="CUSTOMER SATISFACTION SCORES", font=dict(family="Share Tech Mono",color=PURPLE,size=10), x=0.01))
        st.plotly_chart(fig, width='stretch')

# ══ TAB 2 — CUSTOMERS ════════════════════════════════════════════
with t2:
    st.markdown('<div class="sec">▸ RFM SEGMENTATION MATRIX</div>', unsafe_allow_html=True)
    sc = cust_df["rfm_segment"].value_counts() if "rfm_segment" in cust_df.columns else pd.Series()
    c1,c2,c3,c4,c5 = st.columns(5)
    for col,seg,color in [(c1,"Champions",PURPLE),(c2,"Loyal",BLUE),(c3,"New",CYAN),(c4,"At-Risk",AMBER),(c5,"Lost",RED)]:
        col.markdown(kpi(seg.upper(), f"{sc.get(seg,0):,}", "customers", color), unsafe_allow_html=True)

    st.markdown('<hr class="div">', unsafe_allow_html=True)
    c1,c2 = st.columns([1,2])

    with c1:
        if "rfm_segment" in cust_df.columns:
            seg_c = cust_df["rfm_segment"].value_counts().reset_index()
            seg_c.columns = ["segment","count"]
            fig = go.Figure(go.Pie(
                labels=seg_c["segment"], values=seg_c["count"],
                hole=0.62,
                marker=dict(colors=[PURPLE,BLUE,CYAN,AMBER,RED,PINK]),
                textfont=dict(family="Share Tech Mono",size=10),
                hovertemplate="<b>%{label}</b><br>%{value:,} customers<extra></extra>"
            ))
            fig.add_annotation(text=f"{len(cust_df):,}<br><span style='font-size:8px'>TOTAL</span>",
                font=dict(family="Orbitron",size=14,color=PURPLE), showarrow=False)
            fig.update_layout(**PLOTLY, height=280,
                title=dict(text="SEGMENT SPLIT", font=dict(family="Share Tech Mono",color=PURPLE,size=10), x=0.01))
            st.plotly_chart(fig, width='stretch')

    with c2:
        if "rfm_segment" in cust_df.columns and "total_spend" in cust_df.columns:
            sr = cust_df.groupby("rfm_segment")["total_spend"].agg(["sum","mean","count"]).reset_index()
            sr.columns = ["segment","total","avg","count"]
            sr = sr.sort_values("total", ascending=False)
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Total Revenue",x=sr["segment"],y=sr["total"],
                marker_color=PURPLE, yaxis="y",
                text=[fc(v) for v in sr["total"]],
                textfont=dict(family="Share Tech Mono",size=9,color="#fff")))
            fig.add_trace(go.Scatter(name="Avg Spend",x=sr["segment"],y=sr["avg"],
                mode="lines+markers",marker=dict(color=CYAN,size=8),
                line=dict(color=CYAN,width=2), yaxis="y2"))
            _layout = {k:v for k,v in PLOTLY.items() if k != "yaxis"}
            fig.update_layout(**_layout, height=280,
                yaxis=dict(title="Total Revenue",gridcolor="rgba(123,79,255,0.06)",color="#554477"),
                yaxis2=dict(title="Avg Spend",overlaying="y",side="right",color=CYAN,showgrid=False),
                title=dict(text="REVENUE vs AVG SPEND BY SEGMENT", font=dict(family="Share Tech Mono",color=PURPLE,size=10), x=0.01))
            st.plotly_chart(fig, width='stretch')

    st.markdown('<div class="sec">▸ CHURN RISK DISTRIBUTION</div>', unsafe_allow_html=True)
    if "churn_probability" in cust_df.columns:
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=cust_df["churn_probability"], nbinsx=50,
            marker=dict(color=RED, opacity=0.75,
                colorscale=[[0,PURPLE],[0.5,BLUE],[1,RED]],
                line=dict(color="#03010a",width=0.3)),
        ))
        fig.add_vline(x=0.5, line_dash="dash", line_color=AMBER, line_width=1,
                      annotation_text="50% THRESHOLD",
                      annotation_font=dict(family="Share Tech Mono",color=AMBER,size=9))
        fig.add_vline(x=cust_df["churn_probability"].mean(), line_dash="dot", line_color=CYAN, line_width=1,
                      annotation_text=f"AVG {cust_df['churn_probability'].mean():.2f}",
                      annotation_font=dict(family="Share Tech Mono",color=CYAN,size=9))
        fig.update_layout(**PLOTLY, height=200,
            title=dict(text="CHURN PROBABILITY DISTRIBUTION ACROSS ALL CUSTOMERS", font=dict(family="Share Tech Mono",color=RED,size=10), x=0.01),
            xaxis_title="Churn Probability Score", yaxis_title="Customer Count")
        st.plotly_chart(fig, width='stretch')

# ══ TAB 3 — SELLERS ══════════════════════════════════════════════
with t3:
    st.markdown('<div class="sec">▸ SELLER PERFORMANCE COMMAND</div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    total_sell  = len(sell_df)
    breach      = (sell_df["late_delivery_rate"]>0.2).mean()*100 if "late_delivery_rate" in sell_df.columns else 0
    avg_rev_s   = sell_df["average_review_score"].mean() if "average_review_score" in sell_df.columns else 0
    top_rev     = sell_df["total_revenue"].max() if "total_revenue" in sell_df.columns else 0
    for col,l,v,c in [(c1,"TOTAL SELLERS",f"{total_sell:,}",BLUE),(c2,"SLA BREACH",f"{breach:.1f}%",RED),(c3,"AVG REVIEW",f"{avg_rev_s:.2f}★",PURPLE if avg_rev_s>=4 else AMBER),(c4,"TOP SELLER",fc(top_rev),CYAN)]:
        col.markdown(kpi(l,v,"",c), unsafe_allow_html=True)

    st.markdown('<hr class="div">', unsafe_allow_html=True)
    c1,c2 = st.columns(2)

    with c1:
        if "total_revenue" in sell_df.columns and "late_delivery_rate" in sell_df.columns:
            fig = px.scatter(sell_df.sample(min(300,len(sell_df))),
                x="late_delivery_rate", y="total_revenue",
                color="seller_tier" if "seller_tier" in sell_df.columns else None,
                size="total_order_count" if "total_order_count" in sell_df.columns else None,
                size_max=18, opacity=0.75,
                color_discrete_map={"Platinum":CYAN,"Gold":AMBER,"Silver":BLUE,"Bronze":RED},
                labels={"late_delivery_rate":"Late Delivery Rate","total_revenue":"Revenue (R$)"},
            )
            fig.update_layout(**PLOTLY, height=280,
                title=dict(text="REVENUE vs SLA BREACH RATE", font=dict(family="Share Tech Mono",color=PURPLE,size=10), x=0.01))
            st.plotly_chart(fig, width='stretch')

    with c2:
        if "seller_tier" in sell_df.columns and "total_revenue" in sell_df.columns:
            tr = sell_df.groupby("seller_tier")["total_revenue"].sum().reset_index()
            fig = go.Figure(go.Pie(
                labels=tr["seller_tier"], values=tr["total_revenue"],
                hole=0.58,
                marker=dict(colors=[CYAN,AMBER,BLUE,RED]),
                textfont=dict(family="Share Tech Mono",size=10),
            ))
            fig.update_layout(**PLOTLY, height=280,
                title=dict(text="REVENUE CONCENTRATION BY TIER", font=dict(family="Share Tech Mono",color=BLUE,size=10), x=0.01))
            st.plotly_chart(fig, width='stretch')

    st.markdown('<div class="sec">▸ TOP 20 SELLER SCORECARD</div>', unsafe_allow_html=True)
    if not sell_df.empty:
        cols = [c for c in ["seller_id","total_revenue","total_order_count","late_delivery_rate","average_review_score","seller_tier"] if c in sell_df]
        top20 = sell_df.nlargest(20,"total_revenue")[cols].copy()
        if "total_revenue" in top20.columns: top20["total_revenue"] = top20["total_revenue"].apply(fc)
        if "late_delivery_rate" in top20.columns: top20["late_delivery_rate"] = (top20["late_delivery_rate"]*100).round(1).astype(str)+"%"
        if "average_review_score" in top20.columns: top20["average_review_score"] = top20["average_review_score"].round(2)
        st.dataframe(top20, width='stretch', height=260)

# ══ TAB 4 — LOGISTICS ════════════════════════════════════════════
with t4:
    st.markdown('<div class="sec">▸ DELIVERY OPERATIONS COMMAND</div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    avg_d  = sla_df["days_to_deliver"].mean() if "days_to_deliver" in sla_df.columns else 0
    lp     = sla_df["is_late_delivery"].mean()*100 if "is_late_delivery" in sla_df.columns else 0
    ar     = sla_df["review_score"].mean() if "review_score" in sla_df.columns else 0
    fr     = (rev_df["freight_value"].sum()/max(rev_df["gmv"].sum(),1)*100) if "freight_value" in rev_df.columns else 0
    for col,l,v,c in [(c1,"AVG DELIVERY",f"{avg_d:.1f} days",AMBER),(c2,"LATE RATE",f"{lp:.1f}%",RED if lp>10 else AMBER),(c3,"AVG REVIEW",f"{ar:.2f}★",PURPLE if ar>=4 else AMBER),(c4,"FREIGHT RATE",f"{fr:.1f}%",BLUE)]:
        col.markdown(kpi(l,v,"",c), unsafe_allow_html=True)

    st.markdown('<hr class="div">', unsafe_allow_html=True)
    c1,c2 = st.columns(2)

    with c1:
        if "product_category_name_english" in sla_df.columns and "is_late_delivery" in sla_df.columns:
            cl = sla_df.groupby("product_category_name_english")["is_late_delivery"].mean().sort_values(ascending=False).reset_index()
            cl["pct"] = (cl["is_late_delivery"]*100).round(1)
            fig = go.Figure(go.Bar(
                x=cl["pct"], y=cl["product_category_name_english"], orientation="h",
                marker=dict(color=cl["pct"],
                    colorscale=[[0,PURPLE],[0.4,BLUE],[0.7,AMBER],[1,RED]],
                    line=dict(color="rgba(0,0,0,0.3)",width=0.3)),
                text=[f"{v}%" for v in cl["pct"]],
                textfont=dict(family="Share Tech Mono",size=9,color="#fff"),
            ))
            fig.update_layout(**PLOTLY, height=300,
                title=dict(text="LATE DELIVERY RATE BY CATEGORY", font=dict(family="Share Tech Mono",color=RED,size=10), x=0.01),
                xaxis_title="Late %")
            st.plotly_chart(fig, width='stretch')

    with c2:
        if "days_to_deliver" in sla_df.columns:
            fig = go.Figure(go.Histogram(
                x=sla_df["days_to_deliver"].clip(0,60), nbinsx=35,
                marker=dict(color=BLUE, opacity=0.8,
                    line=dict(color="#03010a",width=0.3)),
            ))
            fig.add_vline(x=avg_d, line_dash="dash", line_color=CYAN, line_width=1.5,
                          annotation_text=f"  AVG {avg_d:.1f}d",
                          annotation_font=dict(family="Share Tech Mono",color=CYAN,size=9))
            fig.update_layout(**PLOTLY, height=300,
                title=dict(text="DELIVERY TIME DISTRIBUTION", font=dict(family="Share Tech Mono",color=BLUE,size=10), x=0.01),
                xaxis_title="Days to Deliver", yaxis_title="Order Count")
            st.plotly_chart(fig, width='stretch')

    if "seller_state" in sla_df.columns:
        sl = sla_df.groupby("seller_state")["is_late_delivery"].mean().sort_values(ascending=False).head(10).reset_index()
        sl["pct"] = (sl["is_late_delivery"]*100).round(1)
        fig = go.Figure(go.Bar(
            x=sl["seller_state"], y=sl["pct"],
            marker=dict(color=sl["pct"], colorscale=[[0,PURPLE],[0.5,AMBER],[1,RED]]),
            text=[f"{v}%" for v in sl["pct"]],
            textfont=dict(family="Share Tech Mono",size=9,color="#fff"),
        ))
        fig.update_layout(**PLOTLY, height=200,
            title=dict(text="LATE DELIVERY RATE BY SELLER STATE", font=dict(family="Share Tech Mono",color=RED,size=10), x=0.01))
        st.plotly_chart(fig, width='stretch')

# ══ TAB 5 — AI ENGINE ════════════════════════════════════════════
with t5:
    st.markdown('<div class="sec">▸ CHURN PREDICTION ENGINE — LIVE INFERENCE</div>', unsafe_allow_html=True)
    model = load_model()

    c1,c2 = st.columns([1,1])
    with c1:
        st.markdown('<p style="font-family:Share Tech Mono,monospace;font-size:10px;color:rgba(123,79,255,0.5);letter-spacing:2px;margin-bottom:12px;">CUSTOMER PROFILE — ADJUST PARAMETERS</p>', unsafe_allow_html=True)
        days_since   = st.slider("DAYS SINCE LAST ORDER",   0, 365, 90)
        total_orders = st.slider("TOTAL ORDERS",            1,  30,  3)
        total_spend  = st.slider("TOTAL SPEND (R$)",       10,5000,300)
        avg_review   = st.slider("AVG REVIEW SCORE GIVEN", 1.0,5.0,4.0,0.1)
        avg_deliver  = st.slider("AVG DELIVERY DAYS",       1, 60, 12)

    with c2:
        if model is not None:
            try: cp = model.predict_proba([[days_since,total_orders,total_spend,avg_review,avg_deliver]])[0][1]
            except: cp = days_since/365*0.8
        else:
            cp = min((days_since/365*0.5)+(1/max(total_orders,1)*0.3)+((1-avg_review/5)*0.2),0.99)

        if cp < 0.3:   vc,vt,vs = "v-nom", "NOMINAL",  "CUSTOMER STABLE — LOW CHURN RISK"
        elif cp < 0.6: vc,vt,vs = "v-warn","CAUTION",  "MONITOR — MODERATE RISK DETECTED"
        else:          vc,vt,vs = "v-crit","CRITICAL",  "IMMEDIATE INTERVENTION REQUIRED"

        color_map = {"v-nom":PURPLE,"v-warn":AMBER,"v-crit":RED}
        vc_color  = color_map[vc]

        st.markdown(f"""
        <div class="verdict {vc}">
            <div style="font-size:9px;letter-spacing:3px;color:rgba(255,255,255,0.3);margin-bottom:10px;">TACTICAL VERDICT</div>
            <div style="font-size:34px;font-weight:900;color:{vc_color};letter-spacing:6px;text-shadow:0 0 20px {vc_color};">{vt}</div>
            <div style="font-size:9px;letter-spacing:2px;color:{vc_color};margin-top:8px;opacity:0.7;">{vs}</div>
            <div style="font-size:52px;font-weight:900;color:{vc_color};margin:12px 0;text-shadow:0 0 30px {vc_color};font-family:'Orbitron',monospace;">{cp*100:.1f}%</div>
            <div style="font-size:9px;color:rgba(255,255,255,0.25);letter-spacing:2px;">CHURN PROBABILITY SCORE</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="div">', unsafe_allow_html=True)
    st.markdown('<div class="sec">▸ POPULATION RISK ANALYSIS</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)

    with c1:
        if "churn_probability" in cust_df.columns and "rfm_segment" in cust_df.columns:
            sc2 = cust_df.groupby("rfm_segment")["churn_probability"].mean().sort_values(ascending=False).reset_index()
            fig = go.Figure(go.Bar(
                x=sc2["rfm_segment"], y=(sc2["churn_probability"]*100).round(1),
                marker=dict(color=[RED,AMBER,BLUE,PURPLE,CYAN][:len(sc2)]),
                text=[f"{v:.1f}%" for v in sc2["churn_probability"]*100],
                textfont=dict(family="Share Tech Mono",size=10,color="#fff"),
            ))
            fig.update_layout(**PLOTLY, height=250,
                title=dict(text="AVG CHURN RISK BY SEGMENT", font=dict(family="Share Tech Mono",color=RED,size=10), x=0.01),
                yaxis_title="Churn %")
            st.plotly_chart(fig, width='stretch')

    with c2:
        if "churn_probability" in cust_df.columns and "total_spend" in cust_df.columns:
            hr = cust_df[cust_df["churn_probability"]>0.6]["total_spend"].sum()
            sr2 = cust_df["total_spend"].sum() - hr
            fig = go.Figure(go.Pie(
                labels=["Revenue at Risk","Stable Revenue"],
                values=[hr, sr2], hole=0.62,
                marker=dict(colors=[RED, PURPLE]),
                textfont=dict(family="Share Tech Mono",size=10),
            ))
            fig.add_annotation(text=fc(hr), font=dict(family="Orbitron",size=14,color=RED), showarrow=False)
            fig.update_layout(**PLOTLY, height=250,
                title=dict(text="REVENUE AT RISK (churn >60%)", font=dict(family="Share Tech Mono",color=RED,size=10), x=0.01))
            st.plotly_chart(fig, width='stretch')

# ── FOOTER ────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <span>⬡ OLIST INTELLIGENCE PLATFORM · SAATVIKA CHOKKAPU · MS BUSINESS ANALYTICS UTD 2026</span>
    <span>dbt 11 MODELS · AWS RDS · RANDOM FOREST ML · STREAMLIT</span>
</div>
""", unsafe_allow_html=True)
