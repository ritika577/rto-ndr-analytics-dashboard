from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
import streamlit as st
import pandas as pd
import math
import plotly.express as px
import time
import altair as alt
from dotenv import load_dotenv
from datetime import datetime
from plotly.express.colors import sample_colorscale
import os
from itertools import islice, cycle
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
kpis=[("📦 Total RTOs", df_daily_rto["rto_count"].sum()),
      ( "🚚 Avg NDR %", round(df_ndr_by_courier["ndr_percentage"].mean(), 2)), 
      ("⏱️ Avg Delivery Time (In Days)", round(df_delivery_time["avg_delivery_days"].mean(), 2)),
        ("High Reattempt %", f"{round((high_attempt_count/df_main_table.iloc[0, 0])*100,2)}%"),
          ("Top Failure Reason", df_failure_reasons["failure_reason"].mode()[0]),
          ("Top Courier Partner",df_ndr_by_courier.sort_values("ndr_percentage").iloc[0]["courier_partner"])]


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
        render_kpis(kpis[3:5], per_row=per_row) 
    with st.container(border=True):
        st.markdown("### 🏆 Top Performing Courier Partner (Lowest NDR%)")
        render_kpis(kpis[5:], per_row=per_row)  # last 3 KPIs
    
    # ------------------------------
    # Top 3 Performing Courier Partners (Lowest NDR %)
    # ------------------------------
    # st.markdown("### 🏆 Top 3 Performing Courier Partners (Lowest NDR%)")
    
    # top_couriers = df_ndr_by_courier.sort_values("ndr_percentage").head(3)

    # for idx, row in top_couriers.iterrows():
    #     st.write(f" **{row['courier_partner']}** – {row['ndr_percentage']}% NDR")
    #     st.markdown("---")

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
    # --- Pincode Search ---
    st.markdown("### 🔎Pincode Courier Stats")
    # Optional one‑line description (remove if you don't want it)
    # st.caption("Enter a pincode to see the top courier partner and total orders.")

    selected_pincode = st.text_input(" ", placeholder="Enter pincode").strip()
    if selected_pincode:
        # Ensure pincode is numeric and has 6 digits
        if not selected_pincode.isdigit():
            st.error("Please enter a valid pincode.")
        else:
            # Convert to integer for SQL query
            selected_pincode = int(selected_pincode)

        st.markdown(f"**🔍 Search results for:** {selected_pincode if selected_pincode else '_(none yet)_'}")
        df_top_couriers_by_pincodes = pd.read_sql(f"SELECT * FROM rto_ndr_analytics_db.top_couriers_by_pincode where pincode like '%{selected_pincode}%';" , conn)

        df_top_couriers_by_pincodes["Pincode"]=df_top_couriers_by_pincodes["pincode"]
        df_top_couriers_by_pincodes.drop(columns=["pincode"], inplace=True)
        df_top_couriers_by_pincodes["Top Courier Partner"]= df_top_couriers_by_pincodes["courier_partner"]
        df_top_couriers_by_pincodes.drop(columns=["courier_partner"], inplace=True)
        df_top_couriers_by_pincodes["Total Orders"]= df_top_couriers_by_pincodes["total_orders"]
        df_top_couriers_by_pincodes.drop(columns=["total_orders"], inplace=True)

        st.dataframe(df_top_couriers_by_pincodes)

    

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

    df_courier_partner_failure_reasons["courier_partner"] = df_courier_partner_failure_reasons["courier_partner"].astype(str)
    df_courier_partner_failure_reasons["failure_reason"] = df_courier_partner_failure_reasons["failure_reason"].astype(str)
    df_courier_partner_failure_reasons["count"] = pd.to_numeric(df_courier_partner_failure_reasons["count"], errors="coerce").fillna(0)

    # 2) Aggregate to one row per (courier, reason)
    agg = (
        df_courier_partner_failure_reasons.groupby(["courier_partner", "failure_reason"], as_index=False)["count"]
        .sum()
    )

    # 3) Order couriers by total volume (optional but makes stacks feel right)
    courier_order = (
        agg.groupby("courier_partner")["count"].sum()
        .sort_values(ascending=False).index.tolist()
    )
    # stacked bar chart

    # Single hue (indigo) with lightness ramp
    palette_C = [
        "#F2F5FB",  # NEW extra light
        "#E3E8F6", "#CFD8EE", "#BAC8E6", "#A6B9DE", "#91A9D6",
        "#7D99CE", "#688AC6", "#547ABE", "#3F6BB6", "#2B5BAE",
        "#164CA6", "#0E3E8F", "#082F78",
        "#061F52"   # NEW deepest
        ]

    reasons = df_courier_partner_failure_reasons["failure_reason"].unique().tolist()
    # Use your existing reason_order list or derive it:
    reason_order = (
        df_courier_partner_failure_reasons.groupby("failure_reason", as_index=False)["count"]
        .sum()
        .sort_values("count", ascending=False)["failure_reason"]
        .tolist()
    )
    palette = palette_C[:len(reason_order)]  # trim to number of reasons
    color_map = dict(zip(reason_order, palette))
    if len(reasons) > len(palette):
        extended = list(islice(cycle(palette), len(reasons)))
        color_map = dict(zip(reasons, extended))

    fig = px.bar(
        df_courier_partner_failure_reasons,
        x="courier_partner",
        y="count",
        color="failure_reason",
        title="High-Attempt Orders by Courier (Stacked)",
        category_orders={"failure_reason": reason_order},
        color_discrete_map=color_map,
        hover_data=["courier_partner", "failure_reason", "count"]
    )

    fig.update_layout(
        barmode="stack",
        title_font=dict(size=26, family="Arial Black", color="white"),
        legend_title_text="Failure Reason",
        legend=dict(font=dict(color="white"), bgcolor="rgba(0,0,0,0)"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            title="Courier",
            tickfont=dict(color="white"),
            titlefont=dict(color="white"),
            gridcolor="rgba(255,255,255,0.06)"
        ),
        yaxis=dict(
            title="Orders",
            tickfont=dict(color="white"),
            titlefont=dict(color="white"),
            gridcolor="rgba(255,255,255,0.10)"
        ),
        margin=dict(t=80, r=40, l=60, b=60)
    )
    fig.update_traces(marker_line_width=0.4, marker_line_color="rgba(0,0,0,0.25)")
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
    # Colors you’ll reuse everywhere
    color_map = {
        "RTO": "#E53935",     # red
        "Cancel": "#FB8C00",  # amber
        "Review": "#3949AB",  # indigo
    }
    df_clean = (
        df_impact_of_delivery_attempts
        .dropna(subset=["failure_reason"])
        .assign(failure_reason=lambda d: d.failure_reason.str.strip())
        .query("failure_reason != ''")
        .copy()
    )
    df_clean["action"] = df_clean["failure_reason"].map(action_map).fillna("Review")
    df_donut = (df_clean.groupby("action", as_index=False)
                .size().rename(columns={"size": "count"})
                .sort_values("action"))

    total_orders = int(df_donut["count"].sum())



    gradient_colors = sample_colorscale("RdBu", [i/(len(df_donut)-1 or 1) for i in range(len(df_donut))])

    fig = px.pie(
        df_donut,
        names="action",
        values="count",
        hole=0.6,
        color="action",
        color_discrete_sequence=gradient_colors
    )
    fig.update_traces(textinfo="label+percent", textposition="inside", marker=dict(line=dict(width=0)))
    fig.update_layout(
        title="Order Actions Distribution",
        title_font=dict(size=24, color="white"),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=60, b=20, l=20, r=20),
        font=dict(color="white")
    )
    st.plotly_chart(fig, use_container_width=True)