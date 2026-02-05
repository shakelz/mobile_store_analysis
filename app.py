import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Data Load & Basic Cleaning
@st.cache_data
def load_data():
    # Aapka cleaned data yahan load hoga
    # Agar aapne file save ki hai toh wo path dein
    df = pd.read_csv('merged_sales_data.csv') # File name check karlo ustaad
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df = df.dropna(how='all')
    df = df[df['Order Date'] != 'Order Date']
    df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'])
    df['Price Each'] = pd.to_numeric(df['Price Each'])
    df['Sales'] = df['Quantity Ordered'] * df['Price Each']
    df['hour'] = df['Order Date'].dt.hour
    df['month'] = df['Order Date'].dt.month
    df['year'] = df['Order Date'].dt.year
    return df

df = load_data()

st.title("📱 Mobile & Electronics Store Analytics")
st.markdown("This dashboard summarizes our EDA and Visualization findings.")

# --- 3 INTERACTIVE WIDGETS ---
st.sidebar.header("Filters")
year_filter = st.sidebar.selectbox("Select Year", df['year'].unique())
month_filter = st.sidebar.slider("Select Month Range", 1, 12, (1, 12))
product_filter = st.sidebar.multiselect("Select Products", df['Product'].unique()[:10], default=df['Product'].unique()[0])

# Filtered Data
filtered_df = df[(df['year'] == year_filter) & 
                 (df['month'] >= month_filter[0]) & 
                 (df['month'] <= month_filter[1])]

# --- 4-6 PLOTS ---

# 1. Total Sales by Month (Line Chart)
st.subheader("Monthly Sales Trend")
monthly_sales = filtered_df.groupby('month')['Sales'].sum().reset_index()
fig1 = px.line(monthly_sales, x='month', y='Sales', markers=True, title=f"Sales Trend for {year_filter}")
st.plotly_chart(fig1)

# 2. Sales by Hour (Peak Times)
st.subheader("Peak Sales Hours")
hourly_sales = filtered_df.groupby('hour')['Sales'].mean().reset_index()
fig2 = px.bar(hourly_sales, x='hour', y='Sales', title="Average Sales by Hour")
st.plotly_chart(fig2)

# 3. Correlation Heatmap (Simplified for Dashboard)
st.subheader("Price vs Quantity Correlation")
fig3 = px.scatter(filtered_df.sample(500), x="Price Each", y="Quantity Ordered", color="Sales", trendline="ols")
st.plotly_chart(fig3)

# 4. Product Wise Sales
st.subheader("Top Selling Products")
prod_sales = filtered_df.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
fig4 = px.pie(prod_sales, values='Sales', names='Product', hole=0.3)
st.plotly_chart(fig4)

st.write("Ustaad, Dashboard is Ready!")
