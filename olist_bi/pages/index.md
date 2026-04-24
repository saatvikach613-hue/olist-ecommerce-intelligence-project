# Olist Executive Intelligence Hub

Welcome to the Olist E-Commerce Performance Dashboard. This report provides a real-time overview of revenue trends, customer segments, and logistics efficiency.

```sql revenue_summary
select * from olist.revenue_summary
```

```sql customer_insights
select * from olist.customer_insights
```

```sql delivery_sla
select * from olist.delivery_sla
```

<Grid cols=3>
    <BigValue 
        data={revenue_summary} 
        value=gmv 
        agg=sum 
        fmt=usd
        title="Total GMV"
    />
    <BigValue 
        data={revenue_summary} 
        value=order_count 
        agg=sum 
        title="Total Orders"
    />
    <BigValue 
        data={customer_insights} 
        value=predicted_churn_risk 
        agg=avg 
        fmt=pct
        title="Avg. Churn Risk"
    />
</Grid>

## 📈 Revenue & Category Performance

<AreaChart 
    data={revenue_summary} 
    x=order_month 
    y=gmv 
    title="Monthly Revenue Trend"
    yAxisTitle="GMV (BRL)"
/>

<BarChart 
    data={revenue_summary} 
    x=product_category_name_english 
    y=gmv 
    agg=sum
    title="Revenue by Category"
    swapXY=true
    sort=true
/>

---

## 👥 Customer Intelligence (ML Predictions)

<Grid cols=2>
    <BarChart 
        data={customer_insights} 
        x=rfm_segment 
        y=customer_id 
        agg=count 
        title="Customer Distribution by RFM Segment"
        swapXY=true
    />
    <ScatterChart 
        data={customer_insights} 
        x=total_orders 
        y=total_spend 
        series=rfm_segment
        title="Spend vs Frequency by Segment"
    />
</Grid>

---

## 🚚 Logistics & Delivery Excellence

<Grid cols=2>
    <BigValue 
        data={delivery_sla} 
        value=is_late_delivery 
        agg=avg 
        fmt=pct
        title="Late Delivery Rate"
    />
    <BigValue 
        data={delivery_sla} 
        value=delay_in_days 
        agg=avg 
        title="Avg. Delay (Days)"
    />
</Grid>

<BarChart 
    data={delivery_sla} 
    x=product_category_name_english 
    y=is_late_delivery 
    agg=avg
    fmt=pct
    title="Late Delivery Rate by Category"
    swapXY=true
    sort=true
/>
