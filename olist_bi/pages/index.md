# 📊 Olist E-Commerce: Executive Performance Brief
> **Confidential** | Prepared for the Operations & Marketing Teams

This briefing provides a comprehensive analysis of the Olist ecosystem, combining historical sales data with **Machine Learning-driven customer churn predictions**.

```sql revenue_summary
select * from olist.revenue_summary
```

```sql customer_insights
select * from olist.customer_insights
```

```sql delivery_sla
select * from olist.delivery_sla
```

---

## 💎 Executive Summary (Last 12 Months)
*The platform has processed over 100k orders. Key focus remains on high-value customer retention and logistics SLA compliance.*

<Grid cols=4>
    <BigValue 
        data={revenue_summary} 
        value=gmv 
        agg=sum 
        fmt=usd
        title="Gross Merchandise Value"
    />
    <BigValue 
        data={revenue_summary} 
        value=order_count 
        agg=sum 
        title="Total Transaction Volume"
    />
    <BigValue 
        data={customer_insights} 
        value=predicted_churn_risk 
        agg=avg 
        fmt=pct
        title="Avg. Churn Probability"
    />
    <BigValue 
        data={delivery_sla} 
        value=is_late_delivery 
        agg=avg 
        fmt=pct
        title="Late Delivery Rate"
    />
</Grid>

---

## 📈 Revenue & Market Share Analysis
*Revenue shows seasonal peaks, with specific categories driving the majority of the GMV.*

<AreaChart 
    data={revenue_summary} 
    x=order_month 
    y=gmv 
    title="GMV Growth Trend"
    yAxisTitle="GMV (BRL)"
    fillColor="#2563eb"
/>

### Top Product Categories by Revenue
<BarChart 
    data={revenue_summary} 
    x=product_category_name_english 
    y=gmv 
    agg=sum
    title="Revenue Contribution by Category"
    swapXY=true
    sort=true
    fillColor="#3b82f6"
/>

---

## 👥 Customer Intelligence (RFM + ML)
*By segmenting customers into RFM (Recency, Frequency, Monetary) groups, we can target high-risk "At-Risk" segments before they churn.*

<Grid cols=2>
    <BarChart 
        data={customer_insights} 
        x=rfm_segment 
        y=customer_id 
        agg=count 
        title="Customer Base by Segment"
        swapXY=true
        fillColor="#c2410c"
    />
    <ScatterPlot 
        data={customer_insights} 
        x=total_orders 
        y=total_spend 
        series=rfm_segment
        title="Spend vs Frequency Matrix"
        xAxisTitle="Number of Orders"
        yAxisTitle="Total Spend (BRL)"
    />
</Grid>

### Churn Risk Analysis
<DataTable data={customer_insights} search=true pagination=true>
    <Column id=customer_id title="Customer ID"/>
    <Column id=rfm_segment title="RFM Segment"/>
    <Column id=total_spend title="Total Spend" fmt=brl/>
    <Column id=predicted_churn_risk title="Churn Risk Score" fmt=pct/>
</DataTable>

---

## 🚚 Logistics & Operational Excellence
*Logistics efficiency is the #1 driver of customer reviews. We are currently seeing a correlation between delivery delays and lower ratings.*

<Grid cols=2>
    <BarChart 
        data={delivery_sla} 
        x=product_category_name_english 
        y=is_late_delivery 
        agg=avg
        fmt=pct
        title="Late Delivery % by Category"
        swapXY=true
        sort=true
        fillColor="#dc2626"
    />
    <AreaChart 
        data={delivery_sla} 
        x=delay_in_days 
        y=is_late_delivery 
        agg=count
        title="Volume of Orders by Delay Days"
        fillColor="#f87171"
    />
</Grid>

---
*End of Brief. Data refreshed directly from AWS RDS Production Instance.*
