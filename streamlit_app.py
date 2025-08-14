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
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/ritika577/rto-ndr-analytics-dashboard',
        'Report a bug': 'https://github.com/ritika577/rto-ndr-analytics-dashboard/issues',
        'About': """
        # RTO/NDR Analytics Dashboard
        
        A modern, professional analytics dashboard for logistics teams.
        
        Built with ❤️ using Streamlit, Plotly, and Altair.
        """
    }
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


# ---- Modern CSS Styling for Enhanced Dashboard ----
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --danger-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --dark-gradient: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        --light-bg: rgba(255, 255, 255, 0.95);
        --card-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        --hover-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        --border-radius: 16px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Global app styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main container improvements */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Enhanced metric cards */
    div[data-testid="stMetricValue"] { 
        font-size: 2.2rem !important; 
        font-weight: 700 !important;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    div[data-testid="metric-container"] {
        background: var(--light-bg);
        border: none !important;
        border-radius: var(--border-radius) !important;
        padding: 1.5rem !important;
        box-shadow: var(--card-shadow) !important;
        transition: var(--transition) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: var(--hover-shadow) !important;
    }
    
    /* Container styling */
    div[data-testid="stContainer"] {
        background: var(--light-bg) !important;
        border: none !important;
        border-radius: var(--border-radius) !important;
        box-shadow: var(--card-shadow) !important;
        backdrop-filter: blur(10px) !important;
        padding: 2rem !important;
        margin: 1rem 0 !important;
        transition: var(--transition) !important;
    }
    
    div[data-testid="stContainer"]:hover {
        box-shadow: var(--hover-shadow) !important;
    }
    
    /* Enhanced titles and headers */
    h1 {
        background: var(--primary-gradient) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        text-align: center !important;
    }
    
    h2, h3 {
        color: #1e293b !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        font-size: 1.4rem !important;
        background: var(--secondary-gradient) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    
    /* Enhanced buttons and inputs */
    .stTextInput > div > div > input {
        border-radius: var(--border-radius) !important;
        border: 2px solid transparent !important;
        background: var(--light-bg) !important;
        box-shadow: var(--card-shadow) !important;
        transition: var(--transition) !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.75rem 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border: 2px solid #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    /* Chart container styling */
    div[data-testid="stPlotlyChart"], 
    div[data-testid="stVegaLiteChart"] {
        background: var(--light-bg) !important;
        border-radius: var(--border-radius) !important;
        box-shadow: var(--card-shadow) !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
        transition: var(--transition) !important;
    }
    
    div[data-testid="stPlotlyChart"]:hover,
    div[data-testid="stVegaLiteChart"]:hover {
        box-shadow: var(--hover-shadow) !important;
    }
    
    /* Enhanced dataframes */
    div[data-testid="stDataFrame"] {
        background: var(--light-bg) !important;
        border-radius: var(--border-radius) !important;
        box-shadow: var(--card-shadow) !important;
        overflow: hidden !important;
    }
    
    /* Expander styling */
    div[data-testid="stExpander"] {
        background: var(--light-bg) !important;
        border: none !important;
        border-radius: var(--border-radius) !important;
        box-shadow: var(--card-shadow) !important;
        margin: 1rem 0 !important;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
    
    /* Hover effects for interactive elements */
    .stMarkdown, .stWrite {
        transition: var(--transition) !important;
    }
    
    /* Custom gradient backgrounds for sections */
    .kpi-section {
        background: var(--success-gradient) !important;
        border-radius: var(--border-radius) !important;
        padding: 2rem !important;
        margin: 1rem 0 !important;
    }
    
    .chart-section {
        background: var(--light-bg) !important;
        border-radius: var(--border-radius) !important;
        padding: 2rem !important;
        margin: 1rem 0 !important;
        box-shadow: var(--card-shadow) !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        div[data-testid="metric-container"] {
            margin-bottom: 1rem !important;
        }
        
        h1 {
            font-size: 1.8rem !important;
        }
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: var(--dark-gradient) !important;
        border-right: none !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    
    /* Enhanced text styling */
    .stMarkdown p {
        color: #475569 !important;
        line-height: 1.6 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Animation for page load */
    .stApp > div {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)   
    # ---- Enhanced KPI rendering with visual improvements ----
def render_kpis(items, per_row=3, title=None):
    if title:
        st.subheader(title)
    for i in range(0, len(items), per_row):
        cols = st.columns(per_row, gap="medium")
        for j, col in enumerate(cols):
            k = i + j
            if k < len(items):
                label, value = items[k]
                with col:
                    # Add custom styling for each metric card
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,248,255,0.95) 100%);
                        padding: 1.5rem;
                        border-radius: 16px;
                        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                        border: 1px solid rgba(255,255,255,0.2);
                        backdrop-filter: blur(10px);
                        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                        margin-bottom: 1rem;
                    ">
                        <div style="
                            font-size: 0.85rem;
                            font-weight: 500;
                            color: #64748b;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                            margin-bottom: 0.5rem;
                        ">{label}</div>
                        <div style="
                            font-size: 2rem;
                            font-weight: 700;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            -webkit-background-clip: text;
                            -webkit-text-fill-color: transparent;
                            background-clip: text;
                        ">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)

# ------------------------------
# Check for Empty Data
# ------------------------------
if df_daily_rto.empty or df_ndr_by_courier.empty or df_delivery_time.empty:
    st.error("🚨 One or more summary tables are empty. Please verify your data in Databricks.")

else:
    # ------------------------------
    # Enhanced Dashboard Title and Overview
    # ------------------------------
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
        <h1 style="
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
            font-family: 'Inter', sans-serif;
        ">📦 RTO / NDR Analytics Dashboard</h1>
        <p style="
            font-size: 1.2rem;
            color: #64748b;
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.6;
            font-family: 'Inter', sans-serif;
        ">
            Analyze <strong>Return-to-Origin (RTO)</strong> and <strong>Non-Delivery Reports (NDR)</strong> trends, 
            track courier performance, and explore delivery efficiency by category. 
            <br><em>Built for logistics teams, ops managers, and data analysts.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ------------------------------
    # Enhanced KPI Sections
    # ------------------------------
    
    # Delivery Risk Overview Section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(139, 195, 74, 0.1) 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(76, 175, 80, 0.2);
    ">
        <h3 style="
            color: #2e7d32;
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-align: center;
        ">📊 Delivery Risk — Overview</h3>
    </div>
    """, unsafe_allow_html=True)
    
    render_kpis(kpis[:3], per_row=per_row)
    
    # Ops & Quality Section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.1) 0%, rgba(3, 169, 244, 0.1) 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(33, 150, 243, 0.2);
    ">
        <h3 style="
            color: #1976d2;
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-align: center;
        ">⚙️ Ops & Quality</h3>
    </div>
    """, unsafe_allow_html=True)
    
    render_kpis(kpis[3:], per_row=per_row) 
    # # KPIs
    # # ------------------------------
    
    # ------------------------------
    # Enhanced Top Performing Courier Partners Section
    # ------------------------------
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.1) 0%, rgba(255, 152, 0, 0.1) 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(255, 193, 7, 0.3);
    ">
        <h3 style="
            color: #f57c00;
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-align: center;
        ">🏆 Top 3 Performing Courier Partners (Lowest NDR%)</h3>
    """, unsafe_allow_html=True)
    
    top_couriers = df_ndr_by_courier.sort_values("ndr_percentage").head(3)
    
    # Create columns for the top couriers
    cols = st.columns(3, gap="medium")
    for idx, (_, row) in enumerate(top_couriers.iterrows()):
        with cols[idx]:
            # Medal emojis for ranking
            medals = ["🥇", "🥈", "🥉"]
            medal = medals[idx] if idx < len(medals) else "🏅"
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.95) 100%);
                border-radius: 16px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                border: 1px solid rgba(255,255,255,0.2);
                backdrop-filter: blur(10px);
                transition: transform 0.3s ease;
                margin-bottom: 1rem;
            " onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{medal}</div>
                <div style="
                    font-size: 1.1rem;
                    font-weight: 600;
                    color: #1e293b;
                    margin-bottom: 0.5rem;
                ">{row['courier_partner']}</div>
                <div style="
                    font-size: 1.8rem;
                    font-weight: 700;
                    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                ">{row['ndr_percentage']}%</div>
                <div style="
                    font-size: 0.8rem;
                    color: #64748b;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                ">NDR Rate</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------
    # Enhanced Daily RTO Trend Chart
    # ------------------------------
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(168, 85, 247, 0.05) 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(99, 102, 241, 0.1);
    ">
        <h3 style="
            color: #6366f1;
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-align: center;
        ">📊 Daily RTO Trend</h3>
    """, unsafe_allow_html=True)

    # Enhanced chart with custom styling
    chart_rto = alt.Chart(df_daily_rto).mark_line(
        point=alt.OverlayMarkDef(
            color='#6366f1',
            size=80,
            filled=True
        ),
        color='#6366f1',
        strokeWidth=3
    ).encode(
        x=alt.X('date:T', 
                title="Date",
                axis=alt.Axis(labelAngle=-45, labelColor='#64748b', titleColor='#1e293b')),
        y=alt.Y('rto_count:Q', 
                title="RTO Count",
                axis=alt.Axis(labelColor='#64748b', titleColor='#1e293b')),
        tooltip=['date:T', 'rto_count:Q']
    ).properties(
        width='container',
        height=400,
        background='rgba(255,255,255,0.8)'
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        grid=True,
        gridColor='rgba(148, 163, 184, 0.2)',
        domain=False
    ).interactive()

    st.altair_chart(chart_rto, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------
    # Enhanced Search UI
    # ------------------------------
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(5, 150, 105, 0.05) 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(16, 185, 129, 0.1);
    ">
        <h3 style="
            color: #059669;
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-align: center;
        ">🔍 Search Courier Performance by Pincode</h3>
    """, unsafe_allow_html=True)
    
    # Enhanced search input
    selected_pincode = st.text_input(
        "Enter Pincode",
        placeholder="e.g. 110001",
        help="Search for courier performance data by pincode"
    ).strip()
    
    if selected_pincode:
        st.markdown(f"""
        <div style="
            background: rgba(16, 185, 129, 0.1);
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            border-left: 4px solid #10b981;
        ">
            <strong>🔍 Search results for pincode: {selected_pincode}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        df_top_couriers_by_pincodes = pd.read_sql(f"SELECT * FROM rto_ndr_analytics_db.top_couriers_by_pincode where pincode like '%{selected_pincode}%';" , conn)
        
        filtered_df = df_top_couriers_by_pincodes[df_top_couriers_by_pincodes["pincode"] == selected_pincode]
        
        if not filtered_df.empty:
            # Clean up column names
            filtered_df = filtered_df.copy()
            filtered_df["Pincode"] = filtered_df["pincode"]
            filtered_df["Top Courier Partner"] = filtered_df["courier_partner"]
            filtered_df["Total Orders"] = filtered_df["total_orders"]
            filtered_df = filtered_df[["Pincode", "Top Courier Partner", "Total Orders"]]
            
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning(f"No data found for pincode: {selected_pincode}")
    
    st.markdown("</div>", unsafe_allow_html=True)

    

    # ------------------------------
    # Enhanced NDR % by Courier Partner Chart
    # ------------------------------
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, rgba(220, 38, 38, 0.05) 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(239, 68, 68, 0.1);
    ">
        <h3 style="
            color: #dc2626;
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-align: center;
        ">🚚 NDR % by Courier Partner</h3>
    """, unsafe_allow_html=True)

    sorted_ndr = df_ndr_by_courier.sort_values("ndr_percentage", ascending=False)

    # Enhanced bar chart with gradient colors
    chart_ndr = alt.Chart(sorted_ndr).mark_bar(
        cornerRadiusTopRight=8,
        cornerRadiusBottomRight=8
    ).encode(
        x=alt.X('ndr_percentage:Q', 
                title="NDR %",
                axis=alt.Axis(labelColor='#64748b', titleColor='#1e293b')),
        y=alt.Y('courier_partner:N', 
                sort='-x', 
                title="Courier Partner",
                axis=alt.Axis(labelColor='#64748b', titleColor='#1e293b')),
        color=alt.Color(
            'ndr_percentage:Q', 
            scale=alt.Scale(
                range=['#fef2f2', '#fecaca', '#f87171', '#ef4444', '#dc2626', '#b91c1c']
            ),
            legend=None
        ),
        tooltip=['courier_partner:N', 'ndr_percentage:Q']
    ).properties(
        width='container',
        height=400,
        background='rgba(255,255,255,0.8)'
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        grid=True,
        gridColor='rgba(148, 163, 184, 0.2)',
        domain=False
    )

    st.altair_chart(chart_ndr, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------
    # Enhanced Avg Delivery Time by Product Category Chart
    # ------------------------------
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(37, 99, 235, 0.05) 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(59, 130, 246, 0.1);
    ">
        <h3 style="
            color: #2563eb;
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-align: center;
        ">⏱️ Average Delivery Time by Product Category</h3>
    """, unsafe_allow_html=True)

    sorted_time = df_delivery_time.sort_values("avg_delivery_days", ascending=False)

    # Enhanced bar chart with blue gradient
    chart_delivery = alt.Chart(sorted_time).mark_bar(
        cornerRadiusTopRight=8,
        cornerRadiusBottomRight=8
    ).encode(
        x=alt.X('avg_delivery_days:Q', 
                title="Average Days",
                axis=alt.Axis(labelColor='#64748b', titleColor='#1e293b')),
        y=alt.Y('product_category:N', 
                sort='-x', 
                title="Product Category",
                axis=alt.Axis(labelColor='#64748b', titleColor='#1e293b')),
        color=alt.Color(
            'avg_delivery_days:Q', 
            scale=alt.Scale(
                range=['#dbeafe', '#bfdbfe', '#93c5fd', '#60a5fa', '#3b82f6', '#2563eb']
            ),
            legend=None
        ),
        tooltip=['product_category:N', 'avg_delivery_days:Q']
    ).properties(
        width='container',
        height=400,
        background='rgba(255,255,255,0.8)'
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        grid=True,
        gridColor='rgba(148, 163, 184, 0.2)',
        domain=False
    )

    st.altair_chart(chart_delivery, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------
    # Enhanced Raw Data Preview
    # ------------------------------
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(107, 114, 128, 0.05) 0%, rgba(75, 85, 99, 0.05) 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(107, 114, 128, 0.1);
    ">
        <h3 style="
            color: #374151;
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-align: center;
        ">🔍 Summary Tables Preview</h3>
    """, unsafe_allow_html=True)
    
    with st.expander("📊 View Detailed Data Tables", expanded=False):
        st.markdown("### 🚚 NDR by Courier Table")
        df_ndr_by_courier_display = df_ndr_by_courier.copy()
        df_ndr_by_courier_display.sort_values("ndr_percentage", ascending=False, inplace=True)
        st.dataframe(df_ndr_by_courier_display, use_container_width=True, hide_index=True)

        st.markdown("### 📦 Delivery Time Table")
        df_delivery_time_display = df_delivery_time.copy()
        df_delivery_time_display.sort_values("avg_delivery_days", ascending=False, inplace=True)
        st.dataframe(df_delivery_time_display, use_container_width=True, hide_index=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------
    # Enhanced Plotly Charts
    # ------------------------------
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.05) 0%, rgba(124, 58, 237, 0.05) 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(139, 92, 246, 0.1);
    ">
        <h3 style="
            color: #7c3aed;
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-align: center;
        ">📈 High-Attempt Orders Analysis</h3>
    """, unsafe_allow_html=True)
    
    # Enhanced stacked bar chart with custom theme
    fig = px.bar(
        df_courier_partner_failure_reasons,
        x="courier_partner",
        y="count",
        color="failure_reason",
        title="High-Attempt Orders by Courier Partner",
        hover_data=["courier_partner", "failure_reason", "count"],
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # Apply modern styling to the chart
    fig.update_layout(
        barmode="stack",
        xaxis_title="Courier Partner",
        yaxis_title="Order Count",
        font=dict(family="Inter, sans-serif", size=12),
        plot_bgcolor='rgba(255,255,255,0.8)',
        paper_bgcolor='rgba(255,255,255,0)',
        title_font_size=16,
        title_font_color='#374151',
        showlegend=True,
        legend=dict(
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(229, 231, 235, 0.8)',
            borderwidth=1
        ),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    fig.update_xaxes(
        gridcolor='rgba(229, 231, 235, 0.2)',
        tickfont=dict(color='#64748b')
    )
    fig.update_yaxes(
        gridcolor='rgba(229, 231, 235, 0.2)',
        tickfont=dict(color='#64748b')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------
    # Enhanced Action Recommendation Chart Section
    # ------------------------------
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(245, 101, 101, 0.05) 0%, rgba(251, 113, 133, 0.05) 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(245, 101, 101, 0.1);
    ">
        <h3 style="
            color: #ef4444;
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-align: center;
        ">🎯 Recommended Actions for High-Attempt Orders</h3>
    """, unsafe_allow_html=True)



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
    # Enhanced donut chart
    fig_donut = px.pie(
        df_donut,
        names="action",
        values="count",
        hole=0.6,
        title="Distribution of Recommended Actions",
        color_discrete_sequence=['#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']
    )
    
    fig_donut.update_layout(
        font=dict(family="Inter, sans-serif", size=12),
        plot_bgcolor='rgba(255,255,255,0.8)',
        paper_bgcolor='rgba(255,255,255,0)',
        title_font_size=16,
        title_font_color='#374151',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(229, 231, 235, 0.8)',
            borderwidth=1
        ),
        margin=dict(l=20, r=20, t=60, b=80)
    )
    
    fig_donut.update_traces(
        textposition="inside", 
        textinfo="percent+label",
        textfont=dict(color='white', size=11),
        marker=dict(line=dict(color='white', width=2))
    )
    
    fig_donut.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add professional footer
    st.markdown("""
    <div style="
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        color: #64748b;
        font-size: 0.9rem;
        border-top: 1px solid rgba(229, 231, 235, 0.5);
    ">
        <p>🚀 <strong>RTO/NDR Analytics Dashboard</strong> | Built with ❤️ for Logistics Excellence</p>
        <p>Empowering data-driven decisions for better delivery performance</p>
    </div>
    """, unsafe_allow_html=True)


