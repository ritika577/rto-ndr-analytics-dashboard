from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
import streamlit as st
import pandas as pd
import plotly.express as px
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


conn = create_engine(
    "databricks://"
    f"token:{os.environ['ACCESS_TOKEN']}@{os.environ['SERVER_HOSTNAME']}"
    f"?http_path={os.environ['HTTP_PATH']}"
)

# ------------------------------
# Load Precalculated Summary Tables
# ------------------------------
df_daily_rto = pd.read_sql("SELECT * FROM rto_ndr_analytics_db.summary_daily_rto", conn)
df_ndr_by_courier = pd.read_sql("SELECT * FROM rto_ndr_analytics_db.summary_ndr_by_courier", conn)
df_delivery_time = pd.read_sql("SELECT * FROM rto_ndr_analytics_db.summary_delivery_time", conn)
df_delivery_attempts_impact = pd.read_sql("SELECT * FROM rto_ndr_analytics_db.delivery_attempts_impact", conn)
df_high_attempts_impact = pd.read_sql("SELECT * FROM rto_ndr_analytics_db.high_attempts_impact", conn)
df_failure_reasons = pd.read_sql("SELECT * FROM rto_ndr_analytics_db.failure_reasons", conn)
df_main_table = pd.read_sql("SELECT count(*) FROM rto_ndr_analytics_db.rto_ndr", conn)
df_courier_partner_failure_reasons = pd.read_sql("SELECT * FROM rto_ndr_analytics_db.courier_partner_failure_reason", conn)
df_impact_of_delivery_attempts = pd.read_sql("SELECT * FROM rto_ndr_analytics_db.impact_of_delivery_attempts", conn)
high_attempt_count= df_high_attempts_impact["attempts"].count()


per_row=3
kpis=[("📦 Total RTOs", df_daily_rto["rto_count"].sum()),( "🚚 Avg NDR %", round(df_ndr_by_courier["ndr_percentage"].mean(), 2)), ("⏱️ Avg Delivery Time", round(df_delivery_time["avg_delivery_days"].mean(), 2)), ("High Attempt %", f"{round((high_attempt_count/df_main_table.iloc[0, 0])*100,2)}%"), ("Top Failure Reason", df_failure_reasons["failure_reason"].mode()[0])]


# ---- optional tiny CSS polish ----
st.markdown("""
<style>
/* Slightly larger metric numbers */
div[data-testid="stMetricValue"] { font-size: 1.6rem; }
/* Reduce left/right padding so cards sit tighter */
section[data-testid="stSidebar"] + section.main > div { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)   
    # ---- helper to render KPIs in rows ----
def render_kpis(items, per_row=3, title=None):
    if title:
        st.subheader(title)
    for i in range(0, len(items), per_row):
        cols = st.columns(per_row, gap="small")
        for j, col in enumerate(cols):
            k = i + j
            if k < len(items):
                label, value= items[k]
                with col:
                    st.metric(label=label, value=value)

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

    with st.container(border=True):
        st.markdown("### Delivery Risk — Overview")
        render_kpis(kpis[:3], per_row=per_row)  # first 5 KPIs

    with st.container(border=True):
        st.markdown("### Ops & Quality")
        render_kpis(kpis[3:], per_row=per_row) 
    # # KPIs
    # # ------------------------------
    
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

        # Optional: Add selectbox for filtering
    # 🔎 Search UI
    selected_pincode = st.text_input("Search", placeholder="pincode").strip()
    st.text("🔍 Search results for: " + selected_pincode)
    df_top_couriers_by_pincodes = pd.read_sql(f"SELECT * FROM rto_ndr_analytics_db.top_couriers_by_pincode where pincode like '%{selected_pincode}%';" , conn)

    filtered_df = df_top_couriers_by_pincodes[df_top_couriers_by_pincodes["pincode"] == selected_pincode]
    filtered_df["Pincode"]=filtered_df["pincode"]
    filtered_df.drop(columns=["pincode"], inplace=True)
    filtered_df["Top Courier Partner"]= filtered_df["courier_partner"]
    filtered_df.drop(columns=["courier_partner"], inplace=True)
    filtered_df["Total Orders"]= filtered_df["total_orders"]
    filtered_df.drop(columns=["total_orders"], inplace=True)

    st.dataframe(filtered_df)

    

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

    # stacked bar chart
    fig = px.bar(
        df_courier_partner_failure_reasons,
        x="courier_partner",
        y="count",
        color="failure_reason",
        title="**High-Attempt Orders by Courier (Stacked)**",
        hover_data=["courier_partner", "failure_reason", "count"]
    )
    fig.update_layout(barmode="stack", xaxis_title="Courier", yaxis_title="Orders")
    st.plotly_chart(fig, use_container_width=True)



action_map = {
    "Address Not Found": "RTO",
    "COD Refused": "Cancel",
    "Customer Unavailable": "RTO",
    "Delivery Rescheduled": "Review",
    "Incorrect Address": "RTO",
    "Contact Number Not Reachable": "Review",
    "Customer Asked to Cancel": "Cancel",
    "Building Locked": "RTO",
    "Security Refused Entry": "RTO",
    "Weather Delay": "Review",
    "Vehicle Breakdown": "Review",
    "Highway Closed": "Review",
    "Customer Shifted": "RTO",
    "Fake Order Suspected": "Cancel",
    "Courier Partner Delay": "Review"
}

# Map to actions
df_impact_of_delivery_attempts["action"] = df_impact_of_delivery_attempts["failure_reason"].map(action_map).fillna("Review")
# 3) Aggregate for donut
df_donut = df_impact_of_delivery_attempts.groupby("action", as_index=False).size().rename(columns={"size": "count"})
fig = px.pie(
    df_donut,
    names="action",
    values="count",
    hole=0.55,  # <- donut!
    title="High-Attempt Orders — Recommended Action Split"
)
fig.update_traces(textposition="inside", textinfo="percent+label")
st.plotly_chart(fig, use_container_width=True)


