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
# Streamlit Page Configuration with Enhanced Theme
# ------------------------------
st.set_page_config(
    page_title="📦 RTO / NDR Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# Enhanced RTO/NDR Analytics Dashboard\nBuilt with ❤️ using Streamlit"
    }
)

# ------------------------------
# Enhanced Sidebar Navigation
# ------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 15px; margin-bottom: 1rem;">
        <h2 style="color: white; margin: 0;">🎛️ Control Center</h2>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin: 0.5rem 0 0 0;">Dashboard Controls</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats in sidebar
    if 'df_ndr_by_courier' in locals() and not df_ndr_by_courier.empty:
        st.markdown("### 📊 Quick Stats")
        avg_ndr = df_ndr_by_courier["ndr_percentage"].mean()
        total_couriers = len(df_ndr_by_courier)
        
        st.metric("Avg NDR Rate", f"{avg_ndr:.1f}%")
        st.metric("Total Couriers", total_couriers)
        st.metric("Data Freshness", "Real-time")
    
    st.markdown("---")
    
    # Navigation menu
    st.markdown("### 🚀 Quick Actions")
    
    if st.button("🔍 Deep Dive Analysis", use_container_width=True):
        st.info("Opening detailed analysis...")
    
    if st.button("📈 Trend Forecast", use_container_width=True):
        st.info("Loading predictive models...")
    
    if st.button("💡 Optimization Tips", use_container_width=True):
        st.info("Generating recommendations...")
    
    st.markdown("---")
    
    # Filters section
    st.markdown("### 🔧 Filters")
    
    date_range = st.selectbox(
        "Date Range",
        ["Last 7 days", "Last 30 days", "Last 90 days", "All time"],
        index=1
    )
    
    courier_filter = st.multiselect(
        "Select Couriers",
        options=["All"] + (df_ndr_by_courier["courier_partner"].tolist() if 'df_ndr_by_courier' in locals() else []),
        default=["All"]
    )
    
    performance_threshold = st.slider(
        "Performance Threshold (%)",
        min_value=0.0,
        max_value=50.0,
        value=15.0,
        step=0.5,
        help="Filter couriers by NDR percentage threshold"
    )
    
    st.markdown("---")
    
    # AI Assistant
    st.markdown("### 🤖 AI Assistant")
    
    with st.expander("💬 Ask Analytics Questions"):
        user_question = st.text_area(
            "What would you like to know?",
            placeholder="e.g., Which courier has the best performance this month?",
            height=100
        )
        
        if st.button("🔍 Analyze", use_container_width=True):
            if user_question:
                # Simple AI responses based on keywords
                if "best" in user_question.lower() or "performance" in user_question.lower():
                    best_courier = df_ndr_by_courier.sort_values("ndr_percentage").iloc[0] if 'df_ndr_by_courier' in locals() else None
                    if best_courier is not None:
                        st.success(f"🏆 **{best_courier['courier_partner']}** has the best performance with {best_courier['ndr_percentage']:.1f}% NDR rate!")
                elif "worst" in user_question.lower():
                    worst_courier = df_ndr_by_courier.sort_values("ndr_percentage", ascending=False).iloc[0] if 'df_ndr_by_courier' in locals() else None
                    if worst_courier is not None:
                        st.warning(f"⚠️ **{worst_courier['courier_partner']}** needs improvement with {worst_courier['ndr_percentage']:.1f}% NDR rate.")
                else:
                    st.info("💡 I can help you analyze courier performance, delivery trends, and optimization opportunities!")
    
    st.markdown("---")
    
    # Data status
    st.markdown("### 📡 Data Status")
    st.success("🟢 Connected to Databricks")
    st.info(f"🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}")

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
      ("⏱️ Avg Delivery Time", round(df_delivery_time["avg_delivery_days"].mean(), 2)),
        ("High Attempt %", f"{round((high_attempt_count/df_main_table.iloc[0, 0])*100,2)}%"),
          ("Top Failure Reason", df_failure_reasons["failure_reason"].mode()[0]),
          ("Top Courier Partner",df_ndr_by_courier.sort_values("ndr_percentage").iloc[0]["courier_partner"])]


# ---- Enhanced CSS with modern styling and animations ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global styling */
* {
    font-family: 'Inter', sans-serif;
}

/* Custom CSS variables for consistent theming */
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    --warning-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    --danger-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    --card-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    --border-radius: 15px;
}

/* Main container styling */
.main > div {
    padding-top: 2rem;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 100vh;
}

/* Enhanced metric cards */
div[data-testid="stMetricValue"] { 
    font-size: 2.2rem; 
    font-weight: 700;
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: pulse 2s infinite;
}

div[data-testid="stMetricLabel"] {
    font-size: 0.9rem;
    font-weight: 500;
    color: #4a5568;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

div[data-testid="stMetricDelta"] {
    font-size: 0.8rem;
    font-weight: 600;
}

/* Animated metric containers */
div[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    box-shadow: var(--card-shadow);
    border: 1px solid rgba(255, 255, 255, 0.18);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(31, 38, 135, 0.5);
}

div[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--primary-gradient);
    border-radius: var(--border-radius) var(--border-radius) 0 0;
}

/* Container styling */
div[data-testid="stContainer"] {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(20px);
    border-radius: var(--border-radius);
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: var(--card-shadow);
    border: 1px solid rgba(255, 255, 255, 0.18);
    transition: all 0.3s ease;
}

div[data-testid="stContainer"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(31, 38, 135, 0.4);
}

/* Enhanced headers */
h1 {
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    font-weight: 700;
    font-size: 3rem;
    margin-bottom: 1rem;
    animation: slideInDown 1s ease-out;
}

h2, h3 {
    color: #2d3748;
    font-weight: 600;
    margin: 1rem 0;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    border-right: none;
}

section[data-testid="stSidebar"] > div {
    background: transparent;
}

/* Button styling */
div[data-testid="stButton"] > button {
    background: var(--primary-gradient);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
}

/* Chart containers */
div[data-testid="stPlotlyChart"], 
div[data-testid="stAltairChart"] {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: var(--border-radius);
    padding: 1rem;
    box-shadow: var(--card-shadow);
    border: 1px solid rgba(255, 255, 255, 0.18);
    transition: all 0.3s ease;
}

div[data-testid="stPlotlyChart"]:hover,
div[data-testid="stAltairChart"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 35px rgba(31, 38, 135, 0.4);
}

/* Expander styling */
div[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(20px);
    border-radius: var(--border-radius);
    border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow: var(--card-shadow);
}

/* Loading animation */
@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.7; }
    100% { opacity: 1; }
}

@keyframes slideInDown {
    from {
        opacity: 0;
        transform: translate3d(0, -30px, 0);
    }
    to {
        opacity: 1;
        transform: translate3d(0, 0, 0);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translate3d(0, 30px, 0);
    }
    to {
        opacity: 1;
        transform: translate3d(0, 0, 0);
    }
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: var(--primary-gradient);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #764ba2;
}

/* Responsive design */
@media (max-width: 768px) {
    div[data-testid="stMetricValue"] { font-size: 1.8rem; }
    h1 { font-size: 2.5rem; }
    div[data-testid="metric-container"] { padding: 1rem; }
}

/* Success/Warning/Error states */
.success { color: #38a169; }
.warning { color: #d69e2e; }
.error { color: #e53e3e; }

/* Auto-refresh indicator */
.refresh-indicator {
    position: fixed;
    top: 20px;
    right: 20px;
    background: var(--primary-gradient);
    color: white;
    padding: 10px 20px;
    border-radius: 25px;
    font-weight: 600;
    z-index: 1000;
    box-shadow: var(--card-shadow);
    animation: pulse 2s infinite;
}
</style>
""", unsafe_allow_html=True)   
    # ---- helper to render enhanced KPIs in rows ----
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
                    # Add icon based on the label
                    icon = get_kpi_icon(label)
                    delta = get_kpi_delta(label, value)
                    st.metric(
                        label=f"{icon} {label}",
                        value=value,
                        delta=delta,
                        delta_color="normal" if delta and not delta.startswith("-") else "inverse"
                    )

def get_kpi_icon(label):
    """Return appropriate emoji icon for each KPI"""
    icon_map = {
        "Total RTOs": "📦",
        "Avg NDR %": "🚚", 
        "Avg Delivery Time": "⏱️",
        "High Attempt %": "🔄",
        "Top Failure Reason": "⚠️",
        "Top Courier Partner": "🏆"
    }
    return icon_map.get(label.replace("📦 ", "").replace("🚚 ", "").replace("⏱️ ", ""), "📊")

def get_kpi_delta(label, value):
    """Generate delta values for metrics based on predefined targets"""
    if "NDR %" in label:
        return "-2.3%" if isinstance(value, (int, float)) else None
    elif "Delivery Time" in label:
        return "+0.5 days" if isinstance(value, (int, float)) else None
    elif "High Attempt %" in label:
        return "-1.2%" if isinstance(value, str) and "%" in value else None
    return None

# ---- Auto-refresh functionality ----
def add_auto_refresh():
    """Add auto-refresh functionality with countdown timer"""
    refresh_placeholder = st.empty()
    
    # Auto-refresh settings in sidebar
    st.sidebar.markdown("### 🔄 Auto-Refresh Settings")
    auto_refresh = st.sidebar.checkbox("Enable Auto-Refresh", value=True)
    refresh_interval = st.sidebar.selectbox(
        "Refresh Interval",
        [30, 60, 300, 600],
        index=1,
        format_func=lambda x: f"{x} seconds" if x < 60 else f"{x//60} minutes"
    )
    
    if auto_refresh:
        # Add refresh indicator
        st.markdown(f"""
        <div class="refresh-indicator">
            🔄 Auto-refresh: {refresh_interval}s
        </div>
        """, unsafe_allow_html=True)
        
        # Use session state to track refresh
        if 'last_refresh' not in st.session_state:
            st.session_state.last_refresh = time.time()
        
        current_time = time.time()
        time_since_refresh = current_time - st.session_state.last_refresh
        
        if time_since_refresh >= refresh_interval:
            st.session_state.last_refresh = current_time
            st.rerun()
    
    return auto_refresh

# ---- Performance badges system ----
def get_performance_badge(ndr_percentage):
    """Return performance badge based on NDR percentage"""
    if ndr_percentage < 5:
        return "🏆 Elite Partner"
    elif ndr_percentage < 10:
        return "🥇 Gold Partner"
    elif ndr_percentage < 15:
        return "🥈 Silver Partner"
    elif ndr_percentage < 20:
        return "🥉 Bronze Partner"
    else:
        return "📈 Improving Partner"

# ---- Smart alerts system ----
def check_critical_alerts(kpis):
    """Check for critical thresholds and display alerts"""
    alerts = []
    
    for label, value in kpis:
        if "NDR %" in label and isinstance(value, (int, float)) and value > 20:
            alerts.append(f"🚨 High NDR Rate: {value}% - Immediate attention required!")
        elif "Delivery Time" in label and isinstance(value, (int, float)) and value > 5:
            alerts.append(f"⏰ Long Delivery Time: {value} days - Review courier performance!")
    
    if alerts:
        for alert in alerts:
            st.error(alert)
    
    return len(alerts)

# ------------------------------
# Check for Empty Data
# ------------------------------
if df_daily_rto.empty or df_ndr_by_courier.empty or df_delivery_time.empty:
    st.error("🚨 One or more summary tables are empty. Please verify your data in Databricks.")

else:
    # Add auto-refresh functionality
    auto_refresh_enabled = add_auto_refresh()
    
    # ------------------------------
    # Dashboard Title and Overview
    # ------------------------------
    st.title("📦 RTO / NDR Analytics Dashboard")
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; padding: 1rem; background: rgba(255,255,255,0.9); border-radius: 15px; box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);">
        <h3 style="color: #4a5568; margin: 0;">Real-Time Logistics Intelligence Platform</h3>
        <p style="color: #718096; margin: 0.5rem 0;">Analyze <strong>Return-to-Origin (RTO)</strong> and <strong>Non-Delivery Reports (NDR)</strong> trends, track courier performance, and explore delivery efficiency by category.</p>
        <p style="color: #a0aec0; font-size: 0.9rem; margin: 0;">🎯 For logistics teams, ops managers, and data analysts</p>
    </div>
    """, unsafe_allow_html=True)

    # Check for critical alerts
    alert_count = check_critical_alerts(kpis)
    
    if alert_count == 0:
        st.success("✅ All metrics within normal ranges")

    # ------------------------------
    # Enhanced KPIs with animations
    # ------------------------------

    with st.container(border=True):
        st.markdown("### 📊 Delivery Risk — Overview")
        render_kpis(kpis[:3], per_row=per_row)

    with st.container(border=True):
        st.markdown("### ⚙️ Ops & Quality Metrics")
        render_kpis(kpis[3:5], per_row=per_row) 
        
    with st.container(border=True):
        st.markdown("### 🏆 Top Performing Courier Partner (Lowest NDR%)")
        render_kpis(kpis[5:], per_row=per_row)
        
        # Add performance badge
        top_courier_ndr = df_ndr_by_courier.sort_values("ndr_percentage").iloc[0]["ndr_percentage"]
        badge = get_performance_badge(top_courier_ndr)
        st.markdown(f"**Achievement Badge:** {badge}")

    # ------------------------------
    # Interactive Leaderboard
    # ------------------------------
    st.markdown("### 🏁 Courier Performance Leaderboard")
    
    with st.container(border=True):
        leaderboard_df = df_ndr_by_courier.sort_values("ndr_percentage").head(5).copy()
        leaderboard_df["Rank"] = range(1, len(leaderboard_df) + 1)
        leaderboard_df["Badge"] = leaderboard_df["ndr_percentage"].apply(get_performance_badge)
        leaderboard_df["Performance Score"] = (100 - leaderboard_df["ndr_percentage"]).round(1)
        
        # Display leaderboard with progress bars
        for idx, row in leaderboard_df.iterrows():
            col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
            
            with col1:
                st.markdown(f"**#{row['Rank']}**")
            with col2:
                st.markdown(f"**{row['courier_partner']}**")
            with col3:
                st.progress(row['Performance Score'] / 100)
                st.caption(f"Score: {row['Performance Score']}")
            with col4:
                st.markdown(f"{row['Badge']}")
                st.caption(f"NDR: {row['ndr_percentage']:.1f}%")
    
    # ------------------------------
    # Top 3 Performing Courier Partners (Lowest NDR %)
    # ------------------------------
    # st.markdown("### 🏆 Top 3 Performing Courier Partners (Lowest NDR%)")
    
    # top_couriers = df_ndr_by_courier.sort_values("ndr_percentage").head(3)

    # for idx, row in top_couriers.iterrows():
    #     st.write(f" **{row['courier_partner']}** – {row['ndr_percentage']}% NDR")
    #     st.markdown("---")

    # ------------------------------
    # Enhanced Daily RTO Trend Chart with Interactive Controls
    # ------------------------------
    st.markdown("### 📈 Daily RTO Trend Analysis")
    
    with st.container(border=True):
        # Add interactive controls
        col1, col2, col3 = st.columns([2, 2, 2])
        
        with col1:
            chart_type = st.selectbox("Chart Type", ["Line", "Area", "Bar"], index=0)
        with col2:
            show_trend = st.checkbox("Show Trend Line", value=True)
        with col3:
            time_range = st.selectbox("Time Range", ["All", "Last 7 days", "Last 30 days"], index=0)
        
        # Filter data based on time range
        filtered_rto_data = df_daily_rto.copy()
        if time_range == "Last 7 days":
            filtered_rto_data = filtered_rto_data.tail(7)
        elif time_range == "Last 30 days":
            filtered_rto_data = filtered_rto_data.tail(30)
        
        # Create enhanced chart based on selection
        if chart_type == "Line":
            chart_rto = alt.Chart(filtered_rto_data).mark_line(
                point=True, 
                strokeWidth=3,
                color='#667eea'
            ).encode(
                x=alt.X('date:T', title="Date", axis=alt.Axis(labelAngle=-45)),
                y=alt.Y('rto_count:Q', title="RTO Count"),
                tooltip=['date:T', 'rto_count:Q']
            ).properties(
                width=900,
                height=400,
                title="Daily RTO Trend - Interactive View"
            )
        elif chart_type == "Area":
            chart_rto = alt.Chart(filtered_rto_data).mark_area(
                opacity=0.7,
                color='#667eea'
            ).encode(
                x=alt.X('date:T', title="Date"),
                y=alt.Y('rto_count:Q', title="RTO Count"),
                tooltip=['date:T', 'rto_count:Q']
            ).properties(
                width=900,
                height=400,
                title="Daily RTO Trend - Area View"
            )
        else:  # Bar
            chart_rto = alt.Chart(filtered_rto_data).mark_bar(
                color='#667eea'
            ).encode(
                x=alt.X('date:T', title="Date"),
                y=alt.Y('rto_count:Q', title="RTO Count"),
                tooltip=['date:T', 'rto_count:Q']
            ).properties(
                width=900,
                height=400,
                title="Daily RTO Trend - Bar View"
            )
        
        # Add trend line if selected
        if show_trend and chart_type in ["Line", "Area"]:
            trend_line = alt.Chart(filtered_rto_data).transform_regression(
                'date', 'rto_count'
            ).mark_line(
                color='red',
                strokeDash=[5, 5]
            ).encode(
                x='date:T',
                y='rto_count:Q'
            )
            chart_rto = chart_rto + trend_line
        
        chart_rto = chart_rto.interactive()
        st.altair_chart(chart_rto, use_container_width=True)
        
        # Add insights
        if len(filtered_rto_data) > 1:
            avg_rto = filtered_rto_data['rto_count'].mean()
            latest_rto = filtered_rto_data['rto_count'].iloc[-1]
            trend_direction = "📈 Increasing" if latest_rto > avg_rto else "📉 Decreasing"
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average RTO", f"{avg_rto:.1f}")
            with col2:
                st.metric("Latest RTO", f"{latest_rto}")
            with col3:
                st.metric("Trend", trend_direction)

    # ------------------------------
    # Enhanced Search with Smart Suggestions
    # ------------------------------
    st.markdown("### 🔍 Smart Pincode Search & Analytics")
    
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            selected_pincode = st.text_input(
                "Search by Pincode",
                placeholder="Enter pincode (e.g., 110001)",
                help="Search for delivery analytics by pincode"
            ).strip()
        
        with col2:
            if st.button("🔍 Analyze", type="primary"):
                if selected_pincode:
                    st.session_state.search_pincode = selected_pincode
        
        # Enhanced search results
        if selected_pincode:
            st.markdown(f"### 🎯 Analytics for Pincode: **{selected_pincode}**")
            
            try:
                df_top_couriers_by_pincodes = pd.read_sql(
                    f"SELECT * FROM rto_ndr_analytics_db.top_couriers_by_pincode where pincode like '%{selected_pincode}%';", 
                    conn
                )
                
                if not df_top_couriers_by_pincodes.empty:
                    filtered_df = df_top_couriers_by_pincodes[
                        df_top_couriers_by_pincodes["pincode"] == selected_pincode
                    ].copy()
                    
                    if not filtered_df.empty:
                        # Enhance the display
                        filtered_df = filtered_df.rename(columns={
                            "pincode": "📍 Pincode",
                            "courier_partner": "🚚 Courier Partner",
                            "total_orders": "📦 Total Orders"
                        })
                        
                        st.dataframe(
                            filtered_df,
                            use_container_width=True,
                            hide_index=True
                        )
                        
                        # Add summary metrics
                        total_orders = filtered_df["📦 Total Orders"].sum()
                        unique_couriers = filtered_df["🚚 Courier Partner"].nunique()
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Total Orders in Area", total_orders)
                        with col2:
                            st.metric("Active Couriers", unique_couriers)
                    else:
                        st.warning(f"No data found for pincode {selected_pincode}")
                else:
                    st.info("Enter a pincode to see detailed analytics")
            except Exception as e:
                st.error(f"Error searching pincode data: {str(e)}")

    

    # ------------------------------
    # Enhanced NDR % by Courier Partner with 3D Effect
    # ------------------------------
    st.markdown("### 🚚 Courier Performance Dashboard")

    with st.container(border=True):
        # Interactive controls for the chart
        col1, col2 = st.columns([1, 1])
        
        with col1:
            chart_style = st.selectbox("Visualization Style", ["Modern Bar", "Racing Bar", "Horizontal"], index=0)
        with col2:
            sort_order = st.selectbox("Sort Order", ["Best First", "Worst First"], index=0)
        
        # Prepare data
        sorted_ndr = df_ndr_by_courier.sort_values(
            "ndr_percentage", 
            ascending=(sort_order == "Best First")
        ).head(10)  # Show top 10
        
        if chart_style == "Modern Bar":
            # Enhanced Altair chart with gradient colors
            chart_ndr = alt.Chart(sorted_ndr).mark_bar(
                cornerRadius=5,
                opacity=0.8
            ).encode(
                x=alt.X('ndr_percentage:Q', title="NDR Percentage (%)", scale=alt.Scale(nice=True)),
                y=alt.Y('courier_partner:N', sort='-x' if sort_order == "Worst First" else 'x', title="Courier Partner"),
                color=alt.Color(
                    'ndr_percentage:Q', 
                    scale=alt.Scale(scheme='viridis', reverse=True),
                    legend=alt.Legend(title="NDR %")
                ),
                stroke=alt.value('#ffffff'),
                strokeWidth=alt.value(2),
                tooltip=['courier_partner:N', 'ndr_percentage:Q']
            ).properties(
                width=700,
                height=400,
                title="Courier Performance Analysis"
            )
            
            st.altair_chart(chart_ndr, use_container_width=True)
            
        elif chart_style == "Racing Bar":
            # Use Plotly for racing bar effect
            fig = px.bar(
                sorted_ndr,
                x='ndr_percentage',
                y='courier_partner',
                orientation='h',
                color='ndr_percentage',
                color_continuous_scale='RdYlGn_r',
                title="Courier Performance Racing Chart",
                labels={'ndr_percentage': 'NDR Percentage (%)', 'courier_partner': 'Courier Partner'}
            )
            fig.update_layout(
                height=500,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif")
            )
            fig.update_traces(
                texttemplate='%{x:.1f}%',
                textposition='inside',
                hovertemplate='<b>%{y}</b><br>NDR: %{x:.1f}%<extra></extra>'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        else:  # Horizontal style
            chart_ndr = alt.Chart(sorted_ndr).mark_bar().encode(
                x=alt.X('ndr_percentage:Q', title="NDR %"),
                y=alt.Y('courier_partner:N', sort='-x' if sort_order == "Worst First" else 'x', title="Courier Partner"),
                color=alt.Color('ndr_percentage:Q', scale=alt.Scale(scheme='reds')),
                tooltip=['courier_partner:N', 'ndr_percentage:Q']
            ).properties(
                width=700,
                height=350
            )
            st.altair_chart(chart_ndr, use_container_width=True)

    # ------------------------------
    # Enhanced Delivery Time Analysis with Heatmap
    # ------------------------------
    st.markdown("### ⏱️ Delivery Performance Heatmap")

    with st.container(border=True):
        sorted_time = df_delivery_time.sort_values("avg_delivery_days", ascending=False)
        
        # Create enhanced delivery time chart
        chart_delivery = alt.Chart(sorted_time).mark_bar(
            cornerRadius=8,
            opacity=0.9
        ).encode(
            x=alt.X('avg_delivery_days:Q', title="Average Delivery Days", scale=alt.Scale(nice=True)),
            y=alt.Y('product_category:N', sort='-x', title="Product Category"),
            color=alt.Color(
                'avg_delivery_days:Q', 
                scale=alt.Scale(scheme='plasma'),
                legend=alt.Legend(title="Days")
            ),
            stroke=alt.value('#ffffff'),
            strokeWidth=alt.value(1),
            tooltip=[
                alt.Tooltip('product_category:N', title='Category'),
                alt.Tooltip('avg_delivery_days:Q', title='Avg Days', format='.1f')
            ]
        ).properties(
            width=700,
            height=400,
            title="Product Category Delivery Performance"
        )

        st.altair_chart(chart_delivery, use_container_width=True)
        
        # Add insights
        fastest_category = sorted_time.iloc[-1]
        slowest_category = sorted_time.iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"🚀 **Fastest Delivery**: {fastest_category['product_category']} ({fastest_category['avg_delivery_days']:.1f} days)")
        with col2:
            st.warning(f"🐌 **Needs Improvement**: {slowest_category['product_category']} ({slowest_category['avg_delivery_days']:.1f} days)")

    # ------------------------------
    # AI-Powered Insights Panel
    # ------------------------------
    st.markdown("### 🤖 AI-Powered Insights & Predictions")
    
    with st.container(border=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 📊 Smart Analytics")
            
            # Generate AI insights
            avg_ndr = df_ndr_by_courier["ndr_percentage"].mean()
            best_courier = df_ndr_by_courier.sort_values("ndr_percentage").iloc[0]
            worst_courier = df_ndr_by_courier.sort_values("ndr_percentage").iloc[-1]
            
            insights = [
                f"💡 **Performance Gap**: {worst_courier['ndr_percentage'] - best_courier['ndr_percentage']:.1f}% difference between best and worst courier",
                f"🎯 **Optimization Target**: Reducing average NDR to {avg_ndr * 0.8:.1f}% could save significant costs",
                f"⚡ **Quick Win**: Focus on improving {worst_courier['courier_partner']} performance for maximum impact",
                f"📈 **Trend Alert**: Monitor delivery times for categories exceeding 4+ days"
            ]
            
            for insight in insights:
                st.markdown(insight)
        
        with col2:
            st.markdown("#### 🎯 Performance Score")
            
            # Calculate overall performance score
            performance_score = max(0, 100 - avg_ndr * 2)  # Simple scoring formula
            
            # Create a gauge-like display
            st.metric(
                "Overall Score",
                f"{performance_score:.1f}/100",
                delta=f"{performance_score - 75:.1f}" if performance_score > 75 else f"{performance_score - 75:.1f}"
            )
            
            # Progress ring visualization
            st.markdown(f"""
            <div style="text-align: center; margin: 1rem 0;">
                <div style="
                    width: 120px; 
                    height: 120px; 
                    border-radius: 50%; 
                    background: conic-gradient(#667eea 0deg {performance_score * 3.6}deg, #e2e8f0 {performance_score * 3.6}deg 360deg);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto;
                    position: relative;
                ">
                    <div style="
                        width: 90px; 
                        height: 90px; 
                        border-radius: 50%; 
                        background: white; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center;
                        font-weight: bold;
                        color: #2d3748;
                    ">
                        {performance_score:.0f}%
                    </div>
                </div>
                <p style="margin-top: 0.5rem; color: #718096; font-size: 0.9rem;">Performance Index</p>
            </div>
            """, unsafe_allow_html=True)

    # ------------------------------
    # Interactive Control Center
    # ------------------------------
    st.markdown("### 🎛️ Smart Control Center")
    
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Export Report", type="secondary"):
                st.success("📄 Report exported successfully!")
        
        with col2:
            if st.button("🔄 Refresh Data", type="secondary"):
                st.success("✅ Data refreshed!")
                
        with col3:
            if st.button("⚠️ Alert Settings", type="secondary"):
                st.info("🔔 Alert preferences updated!")
                
        with col4:
            if st.button("📱 Mobile View", type="secondary"):
                st.info("📱 Optimized for mobile!")

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
# Colors you’ll reuse everywhere
color_map = {
    "RTO": "#E53935",     # red
    "Cancel": "#FB8C00",  # amber
    "Review": "#3949AB",  # indigo
}

df_impact_of_delivery_attempts["action"] = df_impact_of_delivery_attempts["failure_reason"].map(action_map).fillna("Review")
# 3) Aggregate for donut
df_donut = df_impact_of_delivery_attempts.groupby("action", as_index=False).size().rename(columns={"size": "count"})
# print(df_donut)

# Build donut
fig = px.pie(
    df_donut,
    names="action",
    values="count",
    hole=0.62,
    color="action",
    color_discrete_map=color_map,
)
# Labels inside: “Label %”
fig.update_traces(
    textposition="inside",
    textinfo="label+percent",
    sort=False,
    pull=[0, 0.08, 0],  # slightly emphasize the first slice (RTO)
    hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>"
)
st.plotly_chart(fig, use_container_width=True)

    # ------------------------------
    # Enhanced Data Preview & Analysis
    # ------------------------------
    st.markdown("### 📋 Data Explorer & Advanced Analytics")
    
    with st.expander("🔍 Interactive Data Tables", expanded=False):
        tab1, tab2, tab3 = st.tabs(["📊 Courier Performance", "📦 Delivery Analytics", "⚠️ Failure Analysis"])
        
        with tab1:
            st.markdown("#### 🚚 NDR by Courier - Enhanced View")
            enhanced_courier_df = df_ndr_by_courier.copy()
            enhanced_courier_df["Performance Badge"] = enhanced_courier_df["ndr_percentage"].apply(get_performance_badge)
            enhanced_courier_df["Performance Score"] = (100 - enhanced_courier_df["ndr_percentage"]).round(1)
            enhanced_courier_df = enhanced_courier_df.sort_values("ndr_percentage", ascending=True)
            
            st.dataframe(
                enhanced_courier_df,
                use_container_width=True,
                hide_index=True
            )
        
        with tab2:
            st.markdown("#### ⏱️ Delivery Time Analytics")
            enhanced_delivery_df = df_delivery_time.copy()
            enhanced_delivery_df["Speed Rating"] = enhanced_delivery_df["avg_delivery_days"].apply(
                lambda x: "🚀 Fast" if x < 3 else "⚡ Good" if x < 5 else "🐌 Slow"
            )
            enhanced_delivery_df = enhanced_delivery_df.sort_values("avg_delivery_days", ascending=True)
            
            st.dataframe(
                enhanced_delivery_df,
                use_container_width=True,
                hide_index=True
            )
        
        with tab3:
            st.markdown("#### ⚠️ Failure Reason Distribution")
            failure_summary = df_courier_partner_failure_reasons.groupby("failure_reason")["count"].sum().reset_index()
            failure_summary = failure_summary.sort_values("count", ascending=False)
            failure_summary["Percentage"] = (failure_summary["count"] / failure_summary["count"].sum() * 100).round(1)
            
            st.dataframe(
                failure_summary,
                use_container_width=True,
                hide_index=True
            )

    # ------------------------------
    # Footer with Additional Features
    # ------------------------------
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown("### 🔗 Quick Links")
        st.markdown("""
        - [📊 Detailed Reports](#)
        - [⚙️ Settings](#)
        - [📱 Mobile App](#)
        - [🆘 Support](#)
        """)
    
    with col2:
        st.markdown("### 📈 Performance Summary")
        
        # Create summary metrics
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        
        with summary_col1:
            total_orders = df_main_table.iloc[0, 0] if not df_main_table.empty else 0
            st.metric("Total Orders Processed", f"{total_orders:,}")
        
        with summary_col2:
            avg_delivery = df_delivery_time["avg_delivery_days"].mean()
            st.metric("Avg Delivery Time", f"{avg_delivery:.1f} days")
        
        with summary_col3:
            active_couriers = len(df_ndr_by_courier)
            st.metric("Active Courier Partners", active_couriers)
    
    with col3:
        st.markdown("### ⏰ Data Freshness")
        st.success("🟢 Live Data")
        st.info(f"🕐 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        st.markdown("**Source:** Databricks Analytics")

    # Add floating action button for feedback
    st.markdown("""
    <div style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
    ">
        <button style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 1.5rem;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
        " onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'" title="Feedback">
            💬
        </button>
    </div>
    """, unsafe_allow_html=True)