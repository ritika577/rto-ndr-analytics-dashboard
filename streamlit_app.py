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


# ---- Enhanced CSS Styling ----
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Root Variables for Consistent Theming */
:root {
    --primary-color: #1f2937;
    --secondary-color: #3b82f6;
    --accent-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
    --success-color: #22c55e;
    --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --card-background: rgba(255, 255, 255, 0.95);
    --text-primary: #1f2937;
    --text-secondary: #6b7280;
    --border-radius: 12px;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* Global Styling */
.main {
    font-family: 'Inter', sans-serif;
    background: var(--background-gradient);
    min-height: 100vh;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main container styling */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 100% !important;
}

/* Enhanced KPI Cards */
div[data-testid="metric-container"] {
    background: var(--card-background);
    border: none !important;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    padding: 1.5rem !important;
    margin: 0.5rem 0;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

div[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--secondary-color), var(--accent-color));
}

/* Metric values styling */
div[data-testid="stMetricValue"] {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    color: var(--primary-color) !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

div[data-testid="stMetricLabel"] {
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Container styling */
div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] {
    background: var(--card-background);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    padding: 1.5rem;
    margin: 1rem 0;
    backdrop-filter: blur(10px);
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1f2937 0%, #374151 100%);
    padding-top: 2rem;
}

section[data-testid="stSidebar"] > div {
    background: transparent;
}

/* Sidebar content styling */
.sidebar-content {
    color: white;
}

/* Title styling */
h1 {
    background: linear-gradient(135deg, var(--secondary-color), var(--accent-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700 !important;
    text-align: center;
    margin-bottom: 2rem !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Section headers */
h2, h3 {
    color: var(--primary-color) !important;
    font-weight: 600 !important;
    margin-bottom: 1rem !important;
}

/* Search input styling */
div[data-testid="stTextInput"] > div > div > input {
    border: 2px solid #e5e7eb;
    border-radius: var(--border-radius);
    padding: 0.75rem 1rem;
    font-size: 1rem;
    transition: all 0.3s ease;
    background: white;
    box-shadow: var(--shadow);
}

div[data-testid="stTextInput"] > div > div > input:focus {
    border-color: var(--secondary-color);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    outline: none;
}

/* Dataframe styling */
div[data-testid="stDataFrame"] {
    border-radius: var(--border-radius);
    overflow: hidden;
    box-shadow: var(--shadow);
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, var(--secondary-color), var(--accent-color));
    color: white;
    border: none;
    border-radius: var(--border-radius);
    padding: 0.75rem 1.5rem;
    font-weight: 500;
    transition: all 0.3s ease;
    box-shadow: var(--shadow);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

/* Loading animation */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.loading {
    animation: pulse 2s infinite;
}

/* Chart containers */
div[data-testid="stPlotlyChart"], 
div[data-testid="stVegaLiteChart"] {
    background: var(--card-background);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    padding: 1rem;
    margin: 1rem 0;
    backdrop-filter: blur(10px);
}

/* Expander styling */
div[data-testid="stExpander"] {
    background: var(--card-background);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    margin: 1rem 0;
    backdrop-filter: blur(10px);
}

/* Responsive design */
@media (max-width: 768px) {
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
    }
    
    div[data-testid="metric-container"] {
        padding: 1rem !important;
    }
    
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
}

/* Success/warning/error colors for specific metrics */
.metric-success { border-left: 4px solid var(--success-color) !important; }
.metric-warning { border-left: 4px solid var(--warning-color) !important; }
.metric-danger { border-left: 4px solid var(--danger-color) !important; }
</style>
""", unsafe_allow_html=True)   
    # ---- Enhanced KPI renderer with icons and animations ----
def render_kpis(items, per_row=3, title=None):
    """Render KPIs with enhanced styling, icons, and animations"""
    if title:
        st.subheader(title)
    
    # Enhanced KPI icons mapping
    icon_map = {
        "📦 Total RTOs": "📦",
        "🚚 Avg NDR %": "🚚", 
        "⏱️ Avg Delivery Time": "⏱️",
        "High Attempt %": "⚠️",
        "Top Failure Reason": "💡"
    }
    
    for i in range(0, len(items), per_row):
        cols = st.columns(per_row, gap="small")
        for j, col in enumerate(cols):
            k = i + j
            if k < len(items):
                label, value = items[k]
                icon = icon_map.get(label, "📊")
                
                with col:
                    # Create enhanced metric card with custom HTML
                    metric_html = f"""
                    <div style="
                        background: rgba(255, 255, 255, 0.95);
                        border-radius: 12px;
                        padding: 1.5rem;
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                        backdrop-filter: blur(10px);
                        transition: all 0.3s ease;
                        border-top: 4px solid #3b82f6;
                        margin-bottom: 1rem;
                    " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 20px 25px -5px rgba(0, 0, 0, 0.1)'" 
                       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 6px -1px rgba(0, 0, 0, 0.1)'">
                        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                            <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
                            <span style="font-size: 0.85rem; font-weight: 500; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">{label.replace(icon, '').strip()}</span>
                        </div>
                        <div style="font-size: 2.5rem; font-weight: 700; color: #1f2937; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">{value}</div>
                    </div>
                    """
                    st.markdown(metric_html, unsafe_allow_html=True)

# ------------------------------
# Check for Empty Data
# ------------------------------
if df_daily_rto.empty or df_ndr_by_courier.empty or df_delivery_time.empty:
    st.error("🚨 One or more summary tables are empty. Please verify your data in Databricks.")

else:
    # ------------------------------
    # Sidebar Navigation and Filters
    # ------------------------------
    with st.sidebar:
        # Logo and branding area
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 2rem;">
            <h1 style="color: white; font-size: 1.5rem; margin: 0; background: none; -webkit-text-fill-color: white;">
                📦 RTO/NDR Analytics
            </h1>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0.5rem 0 0 0;">
                Logistics Intelligence Dashboard
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        st.markdown("### 📊 Dashboard Sections")
        nav_options = [
            "📈 Overview",
            "🏆 Top Performers", 
            "📊 Trends Analysis",
            "🔍 Search & Filter",
            "📋 Data Tables"
        ]
        
        selected_section = st.selectbox("Navigate to:", nav_options, index=0)
        
        st.markdown("---")
        
        # Filters section
        st.markdown("### 🔧 Filters & Settings")
        
        # Date range filter (placeholder for future enhancement)
        st.markdown("**📅 Date Range**")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From", value=pd.Timestamp.now() - pd.Timedelta(days=30))
        with col2:
            end_date = st.date_input("To", value=pd.Timestamp.now())
        
        # Courier filter
        st.markdown("**🚚 Courier Partners**")
        available_couriers = ["All"] + list(df_ndr_by_courier["courier_partner"].unique())
        selected_couriers = st.multiselect(
            "Select couriers:",
            available_couriers,
            default=["All"]
        )
        
        # Product category filter
        st.markdown("**📦 Product Categories**")
        available_categories = ["All"] + list(df_delivery_time["product_category"].unique())
        selected_categories = st.multiselect(
            "Select categories:",
            available_categories,
            default=["All"]
        )
        
        st.markdown("---")
        
        # Quick stats in sidebar
        st.markdown("### ⚡ Quick Stats")
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
            <div style="color: white; font-size: 0.85rem;">
                <strong>📊 Total Records:</strong><br>
                {df_main_table.iloc[0, 0]:,} orders
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
            <div style="color: white; font-size: 0.85rem;">
                <strong>🚚 Courier Partners:</strong><br>
                {len(df_ndr_by_courier)} active partners
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
            <div style="color: white; font-size: 0.85rem;">
                <strong>📦 Product Categories:</strong><br>
                {len(df_delivery_time)} categories
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ------------------------------
    # Main Dashboard Content
    # ------------------------------
    # Dashboard Title and Overview
    # ------------------------------
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0 3rem 0;">
        <h1 style="font-size: 3rem; margin-bottom: 1rem;">📦 RTO / NDR Analytics Dashboard</h1>
        <p style="font-size: 1.2rem; color: var(--text-secondary); max-width: 800px; margin: 0 auto; line-height: 1.6;">
            Analyze <strong>Return-to-Origin (RTO)</strong> and <strong>Non-Delivery Reports (NDR)</strong> trends, track courier performance,
            and explore delivery efficiency by category. Built for logistics teams, ops managers, and data analysts.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ------------------------------
    # Enhanced KPI Sections
    # ------------------------------
    
    # Overview KPIs with loading state
    with st.container():
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.95); border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); backdrop-filter: blur(10px);">
            <h3 style="color: var(--primary-color); margin-bottom: 1.5rem; display: flex; align-items: center;">
                🎯 <span style="margin-left: 0.5rem;">Delivery Risk — Overview</span>
            </h3>
        """, unsafe_allow_html=True)
        render_kpis(kpis[:3], per_row=per_row)
        st.markdown("</div>", unsafe_allow_html=True)

    # Operations KPIs
    with st.container():
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.95); border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); backdrop-filter: blur(10px);">
            <h3 style="color: var(--primary-color); margin-bottom: 1.5rem; display: flex; align-items: center;">
                ⚙️ <span style="margin-left: 0.5rem;">Operations & Quality</span>
            </h3>
        """, unsafe_allow_html=True)
        render_kpis(kpis[3:], per_row=per_row)
        st.markdown("</div>", unsafe_allow_html=True) 
    # ------------------------------
    # Enhanced Top Performers Section
    # ------------------------------
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.95); border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); backdrop-filter: blur(10px);">
        <h3 style="color: var(--primary-color); margin-bottom: 1.5rem; display: flex; align-items: center;">
            🏆 <span style="margin-left: 0.5rem;">Top 3 Performing Courier Partners (Lowest NDR%)</span>
        </h3>
    """, unsafe_allow_html=True)
    
    top_couriers = df_ndr_by_courier.sort_values("ndr_percentage").head(3)
    
    # Create three columns for top performers
    cols = st.columns(3)
    for idx, (_, row) in enumerate(top_couriers.iterrows()):
        with cols[idx]:
            # Determine medal and color based on ranking
            medals = ["🥇", "🥈", "🥉"]
            colors = ["#FFD700", "#C0C0C0", "#CD7F32"]
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {colors[idx]}20, white);
                border: 2px solid {colors[idx]}40;
                border-radius: 12px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease;
            " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">{medals[idx]}</div>
                <div style="font-size: 1.1rem; font-weight: 600; color: var(--primary-color); margin-bottom: 0.5rem;">
                    {row['courier_partner']}
                </div>
                <div style="font-size: 2rem; font-weight: 700; color: {colors[idx]};">
                    {row['ndr_percentage']}%
                </div>
                <div style="font-size: 0.9rem; color: var(--text-secondary);">
                    NDR Rate
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------
    # Enhanced Daily RTO Trend Chart
    # ------------------------------
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.95); border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); backdrop-filter: blur(10px);">
        <h3 style="color: var(--primary-color); margin-bottom: 1.5rem; display: flex; align-items: center;">
            📊 <span style="margin-left: 0.5rem;">Daily RTO Trend Analysis</span>
        </h3>
    """, unsafe_allow_html=True)

    # Enhanced chart with custom styling
    chart_rto = alt.Chart(df_daily_rto).mark_line(
        point=alt.OverlayMarkDef(
            filled=True,
            size=100,
            color='#3b82f6'
        ),
        strokeWidth=3,
        color='#3b82f6'
    ).encode(
        x=alt.X('date:T', 
                title="Date",
                axis=alt.Axis(
                    labelAngle=-45,
                    labelFontSize=12,
                    titleFontSize=14,
                    grid=True,
                    gridColor='#f1f5f9'
                )),
        y=alt.Y('rto_count:Q', 
                title="RTO Count",
                axis=alt.Axis(
                    labelFontSize=12,
                    titleFontSize=14,
                    grid=True,
                    gridColor='#f1f5f9'
                )),
        tooltip=[
            alt.Tooltip('date:T', title='Date'),
            alt.Tooltip('rto_count:Q', title='RTO Count')
        ]
    ).properties(
        width='container',
        height=400,
        background='transparent'
    ).configure_view(
        strokeOpacity=0
    ).configure_axis(
        domain=False,
        tickColor='#e2e8f0'
    ).interactive()

    st.altair_chart(chart_rto, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------
    # Enhanced Search Functionality
    # ------------------------------
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.95); border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); backdrop-filter: blur(10px);">
        <h3 style="color: var(--primary-color); margin-bottom: 1.5rem; display: flex; align-items: center;">
            🔍 <span style="margin-left: 0.5rem;">Pincode Search & Analysis</span>
        </h3>
    """, unsafe_allow_html=True)
    
    # Enhanced search interface
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_pincode = st.text_input(
            "",
            placeholder="🔍 Enter pincode to search (e.g., 110001)",
            help="Search for courier performance by specific pincode"
        ).strip()
    
    with col2:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    if selected_pincode:
        with st.spinner("🔄 Searching for pincode data..."):
            df_top_couriers_by_pincodes = pd.read_sql(
                f"SELECT * FROM rto_ndr_analytics_db.top_couriers_by_pincode where pincode like '%{selected_pincode}%';" , 
                conn
            )

            filtered_df = df_top_couriers_by_pincodes[df_top_couriers_by_pincodes["pincode"] == selected_pincode]
            
            if not filtered_df.empty:
                # Clean and format the data
                filtered_df = filtered_df.copy()
                filtered_df["Pincode"] = filtered_df["pincode"]
                filtered_df["Top Courier Partner"] = filtered_df["courier_partner"]
                filtered_df["Total Orders"] = filtered_df["total_orders"]
                filtered_df = filtered_df[["Pincode", "Top Courier Partner", "Total Orders"]]
                
                st.success(f"✅ Found {len(filtered_df)} result(s) for pincode: **{selected_pincode}**")
                
                # Display results in an enhanced table
                st.markdown("#### 📋 Search Results")
                st.dataframe(
                    filtered_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Additional insights
                if len(filtered_df) > 0:
                    st.info(f"💡 **Insight**: Top courier for pincode {selected_pincode} is **{filtered_df.iloc[0]['Top Courier Partner']}** with **{filtered_df.iloc[0]['Total Orders']}** total orders.")
            else:
                st.warning(f"⚠️ No data found for pincode: **{selected_pincode}**. Please try a different pincode.")
    else:
        st.info("💡 Enter a pincode above to see courier performance data for that area.")
    
    st.markdown("</div>", unsafe_allow_html=True)

    

    # ------------------------------
    # Enhanced NDR % by Courier Partner Chart
    # ------------------------------
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.95); border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); backdrop-filter: blur(10px);">
        <h3 style="color: var(--primary-color); margin-bottom: 1.5rem; display: flex; align-items: center;">
            🚚 <span style="margin-left: 0.5rem;">NDR % by Courier Partner</span>
        </h3>
    """, unsafe_allow_html=True)

    sorted_ndr = df_ndr_by_courier.sort_values("ndr_percentage", ascending=False)

    chart_ndr = alt.Chart(sorted_ndr).mark_bar(
        cornerRadiusTopRight=4,
        cornerRadiusBottomRight=4
    ).encode(
        x=alt.X('ndr_percentage:Q', 
                title="NDR %",
                axis=alt.Axis(
                    labelFontSize=12,
                    titleFontSize=14,
                    grid=True,
                    gridColor='#f1f5f9'
                )),
        y=alt.Y('courier_partner:N', 
                sort='-x', 
                title="Courier Partner",
                axis=alt.Axis(
                    labelFontSize=12,
                    titleFontSize=14,
                    labelLimit=150
                )),
        color=alt.Color(
            'ndr_percentage:Q',
            scale=alt.Scale(
                scheme='redyellowblue',
                reverse=True
            ),
            legend=alt.Legend(title="NDR %")
        ),
        tooltip=[
            alt.Tooltip('courier_partner:N', title='Courier Partner'),
            alt.Tooltip('ndr_percentage:Q', title='NDR %', format='.2f')
        ]
    ).properties(
        width='container',
        height=400,
        background='transparent'
    ).configure_view(
        strokeOpacity=0
    ).configure_axis(
        domain=False,
        tickColor='#e2e8f0'
    )

    st.altair_chart(chart_ndr, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------
    # Enhanced Avg Delivery Time by Product Category
    # ------------------------------
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.95); border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); backdrop-filter: blur(10px);">
        <h3 style="color: var(--primary-color); margin-bottom: 1.5rem; display: flex; align-items: center;">
            ⏱️ <span style="margin-left: 0.5rem;">Average Delivery Time by Product Category</span>
        </h3>
    """, unsafe_allow_html=True)

    sorted_time = df_delivery_time.sort_values("avg_delivery_days", ascending=False)

    chart_delivery = alt.Chart(sorted_time).mark_bar(
        cornerRadiusTopRight=4,
        cornerRadiusBottomRight=4
    ).encode(
        x=alt.X('avg_delivery_days:Q', 
                title="Average Days",
                axis=alt.Axis(
                    labelFontSize=12,
                    titleFontSize=14,
                    grid=True,
                    gridColor='#f1f5f9'
                )),
        y=alt.Y('product_category:N', 
                sort='-x', 
                title="Product Category",
                axis=alt.Axis(
                    labelFontSize=12,
                    titleFontSize=14,
                    labelLimit=150
                )),
        color=alt.Color(
            'avg_delivery_days:Q',
            scale=alt.Scale(
                scheme='blues',
                reverse=False
            ),
            legend=alt.Legend(title="Avg Days")
        ),
        tooltip=[
            alt.Tooltip('product_category:N', title='Product Category'),
            alt.Tooltip('avg_delivery_days:Q', title='Average Days', format='.1f')
        ]
    ).properties(
        width='container',
        height=400,
        background='transparent'
    ).configure_view(
        strokeOpacity=0
    ).configure_axis(
        domain=False,
        tickColor='#e2e8f0'
    )

    st.altair_chart(chart_delivery, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------
    # Enhanced Data Tables Section
    # ------------------------------
    with st.expander("📋 📊 Detailed Data Tables & Additional Charts", expanded=False):
        # Enhanced data tables with better styling
        st.markdown("#### 🚚 NDR Performance by Courier")
        df_ndr_display = df_ndr_by_courier.sort_values("ndr_percentage", ascending=False).copy()
        df_ndr_display["NDR %"] = df_ndr_display["ndr_percentage"].round(2)
        df_ndr_display["Courier Partner"] = df_ndr_display["courier_partner"]
        st.dataframe(
            df_ndr_display[["Courier Partner", "NDR %"]],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("#### 📦 Delivery Time by Product Category")
        df_delivery_display = df_delivery_time.sort_values("avg_delivery_days", ascending=False).copy()
        df_delivery_display["Average Days"] = df_delivery_display["avg_delivery_days"].round(1)
        df_delivery_display["Product Category"] = df_delivery_display["product_category"]
        st.dataframe(
            df_delivery_display[["Product Category", "Average Days"]],
            use_container_width=True,
            hide_index=True
        )

        # Enhanced stacked bar chart
        st.markdown("#### 📊 High-Attempt Orders by Courier (Breakdown)")
        fig = px.bar(
            df_courier_partner_failure_reasons,
            x="courier_partner",
            y="count",
            color="failure_reason",
            title="High-Attempt Orders by Courier Partner",
            hover_data=["courier_partner", "failure_reason", "count"],
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(
            barmode="stack",
            xaxis_title="Courier Partner",
            yaxis_title="Number of Orders",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=12),
            title_font_size=16,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        fig.update_xaxes(gridcolor='#f1f5f9', gridwidth=1)
        fig.update_yaxes(gridcolor='#f1f5f9', gridwidth=1)
        st.plotly_chart(fig, use_container_width=True)



# Enhanced Action Mapping and Donut Chart
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

# Process action mapping
df_impact_of_delivery_attempts["action"] = df_impact_of_delivery_attempts["failure_reason"].map(action_map).fillna("Review")
df_donut = df_impact_of_delivery_attempts.groupby("action", as_index=False).size().rename(columns={"size": "count"})

# Enhanced donut chart
st.markdown("""
<div style="background: rgba(255, 255, 255, 0.95); border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); backdrop-filter: blur(10px);">
    <h3 style="color: var(--primary-color); margin-bottom: 1.5rem; display: flex; align-items: center;">
        🎯 <span style="margin-left: 0.5rem;">Recommended Action Split for High-Attempt Orders</span>
    </h3>
""", unsafe_allow_html=True)

fig = px.pie(
    df_donut,
    names="action",
    values="count",
    hole=0.6,
    title="",
    color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
)
fig.update_traces(
    textposition="outside",
    textinfo="percent+label",
    textfont_size=12,
    marker=dict(line=dict(color='white', width=2))
)
fig.update_layout(
    showlegend=True,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter", size=12),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.1,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=0, r=0, t=20, b=60)
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Add footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: var(--text-secondary); font-size: 0.9rem;">
    <hr style="border: 1px solid #e5e7eb; margin: 2rem 0;">
    📊 <strong>RTO/NDR Analytics Dashboard</strong> | Built with Streamlit | 
    Data refreshed automatically from Databricks
</div>
""", unsafe_allow_html=True)


