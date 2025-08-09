from databricks import sql
import pandas as pd
import streamlit as st
import time
import altair as alt
from dotenv import load_dotenv
from datetime import datetime
import os
load_dotenv()

# ------------------------------
# Streamlit Page Configuration
# ------------------------------
st.set_page_config(
    page_title="📦 RTO / NDR Analytics Dashboard",
    layout="wide"
)

# ------------------------------
# Databricks Connection
# ------------------------------
conn = sql.connect(
    server_hostname=os.getenv("SERVER_HOSTNAME"),
    http_path=os.getenv("HTTP_PATH"),
    access_token=os.getenv("ACCESS_TOKEN")
)

# ------------------------------
# Load Precalculated Summary Tables
# ------------------------------
df_daily_rto = pd.read_sql("SELECT * FROM rto_ndr_analytics_db.summary_daily_rto", conn)
df_ndr_by_courier = pd.read_sql("SELECT * FROM rto_ndr_analytics_db.summary_ndr_by_courier", conn)
df_delivery_time = pd.read_sql("SELECT * FROM rto_ndr_analytics_db.summary_delivery_time", conn)
df_top_couriers_by_pincodes = pd.read_sql("SELECT * FROM rto_ndr_analytics_db.top_couriers_by_pincode where pincode like ", conn)

conn.close()

# ------------------------------
# Check for Empty Data
# ------------------------------
if df_daily_rto.empty or df_ndr_by_courier.empty or df_delivery_time.empty:
    st.error("🚨 One or more summary tables are empty. Please verify your data in Databricks.")

else:
    # ------------------------------
    # Dashboard Title and Overview
    # ------------------------------
    st.title("📦 RTO / NDR Analytics Dashboard")
    st.markdown("""
    Analyze **Return-to-Origin (RTO)** and **Non-Delivery Reports (NDR)** trends, track courier performance,
    and explore delivery efficiency by category. Useful for logistics teams, ops managers, and data analysts.
    """)

    # ------------------------------
    # KPIs
    # ------------------------------
    col1, col2, col3 = st.columns(3)
    with col1:
        start_time = time.time()
        st.metric("📦 Total RTOs", df_daily_rto["rto_count"].sum())
    with col2:
        start_time = time.time()
        st.metric("🚚 Avg NDR %", round(df_ndr_by_courier["ndr_percentage"].mean(), 2))
    with col3:
        st.metric("⏱️ Avg Delivery Time", round(df_delivery_time["avg_delivery_days"].mean(), 2))

    
    # ------------------------------
    # Top 3 Performing Courier Partners (Lowest NDR %)
    # ------------------------------
    st.markdown("### 🏆 Top 3 Performing Courier Partners (Lowest NDR%)")
    
    top_couriers = df_ndr_by_courier.sort_values("ndr_percentage").head(3)

    for idx, row in top_couriers.iterrows():
        st.write(f" **{row['courier_partner']}** – {row['ndr_percentage']}% NDR")
        st.markdown("---")

    # ------------------------------
    # Daily RTO Trend Chart
    # ------------------------------
    st.subheader("📊 Daily RTO Trend")

    chart_rto = alt.Chart(df_daily_rto).mark_line(point=True).encode(
        x=alt.X('date:T', title="Date"),
        y=alt.Y('rto_count:Q', title="RTO Count"),
        tooltip=['date:T', 'rto_count:Q']
    ).properties(
        width=900,
        height=400
    ).interactive()

    st.altair_chart(chart_rto, use_container_width=True)

    # ------------------------------
    # NDR % by Courier Partner
    # ------------------------------
    st.subheader("🚚 NDR % by Courier Partner")

    sorted_ndr = df_ndr_by_courier.sort_values("ndr_percentage", ascending=False)

    chart_ndr = alt.Chart(sorted_ndr).mark_bar().encode(
        x=alt.X('ndr_percentage:Q', title="NDR %"),
        y=alt.Y('courier_partner:N', sort='-x', title="Courier Partner"),
        color=alt.Color('ndr_percentage:Q', scale=alt.Scale(scheme='reds')),
        tooltip=['courier_partner:N', 'ndr_percentage:Q']
    ).properties(
        width=700,
        height=350
    )

    # Convert PySpark DataFrame to Pandas
   # Best practice also we need to add duckdb in future 
    # pdf = df_top_couriers_by_pincodes.toPandas()

    # Optional: Add selectbox for filtering
    selected_pincode = st.selectbox("Select Pincode", sorted(df_top_couriers_by_pincodes["pincode"].unique()))

    filtered_df = df_top_couriers_by_pincodes[df_top_couriers_by_pincodes["pincode"] == selected_pincode]

    st.dataframe(filtered_df)

    st.altair_chart(chart_ndr, use_container_width=True)

    # ------------------------------
    # Avg Delivery Time by Product Category
    # ------------------------------
    st.subheader("⏱️ Average Delivery Time by Product Category")

    sorted_time = df_delivery_time.sort_values("avg_delivery_days", ascending=False)

    chart_delivery = alt.Chart(sorted_time).mark_bar().encode(
        x=alt.X('avg_delivery_days:Q', title="Average Days"),
        y=alt.Y('product_category:N', sort='-x', title="Product Category"),
        color=alt.Color('avg_delivery_days:Q', scale=alt.Scale(scheme='blues')),
        tooltip=['product_category:N', 'avg_delivery_days:Q']
    ).properties(
        width=700,
        height=350
    )

    st.altair_chart(chart_delivery, use_container_width=True)

    # ------------------------------
    # Raw Data Preview
    # ------------------------------
    with st.expander("🔍 Preview Summary Tables"):

        st.markdown("🚚 **NDR by Courier Table**")
        df_ndr_by_courier.sort_values("ndr_percentage",ascending=False, inplace=True)
        st.dataframe(df_ndr_by_courier)

        st.markdown("📦 **Delivery Time Table**")
        df_delivery_time.sort_values("avg_delivery_days",ascending=False, inplace=True)
        st.dataframe(df_delivery_time)


