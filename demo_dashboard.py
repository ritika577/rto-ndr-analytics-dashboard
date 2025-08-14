"""
Demo version of Enhanced RTO/NDR Analytics Dashboard
Shows UI enhancements without database dependency
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import time
import altair as alt
from datetime import datetime
import numpy as np

# ------------------------------
# Streamlit Page Configuration with Enhanced Theme
# ------------------------------
st.set_page_config(
    page_title="📦 RTO / NDR Analytics Dashboard - DEMO",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# Enhanced RTO/NDR Analytics Dashboard\nBuilt with ❤️ using Streamlit"
    }
)

# Enhanced CSS (same as main file)
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

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    border-right: none;
}

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

# Create mock data
@st.cache_data
def create_mock_data():
    """Create mock data for demonstration"""
    
    # Mock daily RTO data
    dates = pd.date_range(start='2024-01-01', end='2024-01-30', freq='D')
    df_daily_rto = pd.DataFrame({
        'date': dates,
        'rto_count': np.random.randint(50, 200, len(dates))
    })
    
    # Mock courier data
    couriers = ['FastEx', 'QuickShip', 'RapidPost', 'SpeedyGo', 'SwiftCargo', 'UltraDelivery']
    df_ndr_by_courier = pd.DataFrame({
        'courier_partner': couriers,
        'ndr_percentage': [8.5, 12.3, 15.7, 9.2, 18.9, 6.1]
    })
    
    # Mock delivery time data
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 'Beauty']
    df_delivery_time = pd.DataFrame({
        'product_category': categories,
        'avg_delivery_days': [3.2, 2.8, 2.1, 4.5, 3.8, 2.9]
    })
    
    # Mock failure reasons
    df_failure_reasons = pd.DataFrame({
        'failure_reason': ['Address Not Found', 'Customer Unavailable', 'COD Refused'],
        'count': [150, 120, 80]
    })
    
    # Mock courier failure data
    df_courier_failure = pd.DataFrame({
        'courier_partner': ['FastEx', 'QuickShip', 'RapidPost'] * 3,
        'failure_reason': ['Address Not Found'] * 3 + ['Customer Unavailable'] * 3 + ['COD Refused'] * 3,
        'count': [45, 35, 40, 30, 25, 35, 20, 15, 25]
    })
    
    return df_daily_rto, df_ndr_by_courier, df_delivery_time, df_failure_reasons, df_courier_failure

# Load mock data
df_daily_rto, df_ndr_by_courier, df_delivery_time, df_failure_reasons, df_courier_failure = create_mock_data()

# Helper functions
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
                    icon = get_kpi_icon(label)
                    st.metric(
                        label=f"{icon} {label}",
                        value=value,
                        delta="+2.3%" if "NDR" in label else "-1.2%" if "Time" in label else None
                    )

# Enhanced Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 15px; margin-bottom: 1rem;">
        <h2 style="color: white; margin: 0;">🎛️ Control Center</h2>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin: 0.5rem 0 0 0;">Dashboard Controls</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Quick Stats")
    avg_ndr = df_ndr_by_courier["ndr_percentage"].mean()
    total_couriers = len(df_ndr_by_courier)
    
    st.metric("Avg NDR Rate", f"{avg_ndr:.1f}%")
    st.metric("Total Couriers", total_couriers)
    st.metric("Data Freshness", "Real-time")
    
    st.markdown("---")
    
    # Auto-refresh settings
    st.markdown("### 🔄 Auto-Refresh Settings")
    auto_refresh = st.checkbox("Enable Auto-Refresh", value=True)
    refresh_interval = st.selectbox(
        "Refresh Interval",
        [30, 60, 300, 600],
        index=1,
        format_func=lambda x: f"{x} seconds" if x < 60 else f"{x//60} minutes"
    )
    
    st.markdown("---")
    st.markdown("### 🤖 AI Assistant")
    st.info("💡 Demo mode - AI assistant ready for queries!")

# Main Dashboard
st.title("📦 RTO / NDR Analytics Dashboard - DEMO")

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem; padding: 1rem; background: rgba(255,255,255,0.9); border-radius: 15px; box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);">
    <h3 style="color: #4a5568; margin: 0;">🎉 Enhanced Analytics Platform - Demo Version</h3>
    <p style="color: #718096; margin: 0.5rem 0;">Experience the new interactive features and modern design!</p>
    <p style="color: #a0aec0; font-size: 0.9rem; margin: 0;">🎯 Demo with mock data showcasing all enhancements</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh indicator
if auto_refresh:
    st.markdown(f"""
    <div class="refresh-indicator">
        🔄 Auto-refresh: {refresh_interval}s
    </div>
    """, unsafe_allow_html=True)

st.success("✅ All metrics within normal ranges - Demo Mode Active")

# KPIs
kpis = [
    ("📦 Total RTOs", f"{df_daily_rto['rto_count'].sum():,}"),
    ("🚚 Avg NDR %", f"{avg_ndr:.1f}%"),
    ("⏱️ Avg Delivery Time", f"{df_delivery_time['avg_delivery_days'].mean():.1f} days"),
    ("🔄 High Attempt %", "8.3%"),
    ("⚠️ Top Failure Reason", df_failure_reasons.iloc[0]['failure_reason']),
    ("🏆 Top Courier Partner", df_ndr_by_courier.sort_values("ndr_percentage").iloc[0]["courier_partner"])
]

with st.container(border=True):
    st.markdown("### 📊 Delivery Risk — Overview")
    render_kpis(kpis[:3], per_row=3)

with st.container(border=True):
    st.markdown("### ⚙️ Ops & Quality Metrics")
    render_kpis(kpis[3:5], per_row=2)
    
with st.container(border=True):
    st.markdown("### 🏆 Top Performing Courier Partner")
    render_kpis(kpis[5:], per_row=1)
    
    # Performance badge
    top_courier_ndr = df_ndr_by_courier.sort_values("ndr_percentage").iloc[0]["ndr_percentage"]
    badge = get_performance_badge(top_courier_ndr)
    st.markdown(f"**Achievement Badge:** {badge}")

# Interactive Leaderboard
st.markdown("### 🏁 Courier Performance Leaderboard")

with st.container(border=True):
    leaderboard_df = df_ndr_by_courier.sort_values("ndr_percentage").head(5).copy()
    leaderboard_df["Rank"] = range(1, len(leaderboard_df) + 1)
    leaderboard_df["Badge"] = leaderboard_df["ndr_percentage"].apply(get_performance_badge)
    leaderboard_df["Performance Score"] = (100 - leaderboard_df["ndr_percentage"]).round(1)
    
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

# Enhanced Charts
st.markdown("### 📈 Interactive Daily RTO Trend")

with st.container(border=True):
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        chart_type = st.selectbox("Chart Type", ["Line", "Area", "Bar"], index=0)
    with col2:
        show_trend = st.checkbox("Show Trend Line", value=True)
    with col3:
        time_range = st.selectbox("Time Range", ["All", "Last 7 days", "Last 30 days"], index=0)
    
    # Create chart based on selection
    if chart_type == "Line":
        chart_rto = alt.Chart(df_daily_rto).mark_line(
            point=True, 
            strokeWidth=3,
            color='#667eea'
        ).encode(
            x=alt.X('date:T', title="Date"),
            y=alt.Y('rto_count:Q', title="RTO Count"),
            tooltip=['date:T', 'rto_count:Q']
        ).properties(
            width=900,
            height=400,
            title="Daily RTO Trend - Interactive Demo"
        )
    elif chart_type == "Area":
        chart_rto = alt.Chart(df_daily_rto).mark_area(
            opacity=0.7,
            color='#667eea'
        ).encode(
            x=alt.X('date:T', title="Date"),
            y=alt.Y('rto_count:Q', title="RTO Count"),
            tooltip=['date:T', 'rto_count:Q']
        ).properties(
            width=900,
            height=400,
            title="Daily RTO Trend - Area Demo"
        )
    else:
        chart_rto = alt.Chart(df_daily_rto).mark_bar(
            color='#667eea'
        ).encode(
            x=alt.X('date:T', title="Date"),
            y=alt.Y('rto_count:Q', title="RTO Count"),
            tooltip=['date:T', 'rto_count:Q']
        ).properties(
            width=900,
            height=400,
            title="Daily RTO Trend - Bar Demo"
        )
    
    chart_rto = chart_rto.interactive()
    st.altair_chart(chart_rto, use_container_width=True)

# Enhanced Courier Performance
st.markdown("### 🚚 Enhanced Courier Performance Dashboard")

with st.container(border=True):
    col1, col2 = st.columns([1, 1])
    
    with col1:
        chart_style = st.selectbox("Visualization Style", ["Modern Bar", "Racing Bar"], index=0)
    with col2:
        sort_order = st.selectbox("Sort Order", ["Best First", "Worst First"], index=0)
    
    sorted_ndr = df_ndr_by_courier.sort_values(
        "ndr_percentage", 
        ascending=(sort_order == "Best First")
    )
    
    if chart_style == "Racing Bar":
        fig = px.bar(
            sorted_ndr,
            x='ndr_percentage',
            y='courier_partner',
            orientation='h',
            color='ndr_percentage',
            color_continuous_scale='RdYlGn_r',
            title="Courier Performance Racing Chart - Demo",
            labels={'ndr_percentage': 'NDR Percentage (%)', 'courier_partner': 'Courier Partner'}
        )
        fig.update_layout(
            height=400,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif")
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        chart_ndr = alt.Chart(sorted_ndr).mark_bar(
            cornerRadius=5,
            opacity=0.8
        ).encode(
            x=alt.X('ndr_percentage:Q', title="NDR Percentage (%)"),
            y=alt.Y('courier_partner:N', sort='-x' if sort_order == "Worst First" else 'x', title="Courier Partner"),
            color=alt.Color('ndr_percentage:Q', scale=alt.Scale(scheme='viridis', reverse=True)),
            tooltip=['courier_partner:N', 'ndr_percentage:Q']
        ).properties(
            width=700,
            height=400,
            title="Enhanced Courier Performance - Demo"
        )
        
        st.altair_chart(chart_ndr, use_container_width=True)

# AI Insights Panel
st.markdown("### 🤖 AI-Powered Insights & Predictions")

with st.container(border=True):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📊 Smart Analytics - Demo")
        
        insights = [
            f"💡 **Performance Gap**: {df_ndr_by_courier['ndr_percentage'].max() - df_ndr_by_courier['ndr_percentage'].min():.1f}% difference between best and worst courier",
            f"🎯 **Optimization Target**: Reducing average NDR to {avg_ndr * 0.8:.1f}% could save significant costs",
            f"⚡ **Quick Win**: Focus on improving {df_ndr_by_courier.sort_values('ndr_percentage', ascending=False).iloc[0]['courier_partner']} performance",
            f"📈 **Trend Alert**: Monitor delivery times for categories exceeding 4+ days"
        ]
        
        for insight in insights:
            st.markdown(insight)
    
    with col2:
        st.markdown("#### 🎯 Performance Score")
        
        performance_score = max(0, 100 - avg_ndr * 2)
        
        st.metric(
            "Overall Score",
            f"{performance_score:.1f}/100",
            delta=f"{performance_score - 75:.1f}"
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

# Control Center
st.markdown("### 🎛️ Smart Control Center")

with st.container(border=True):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Export Report", type="secondary"):
            st.success("📄 Demo: Report export feature ready!")
    
    with col2:
        if st.button("🔄 Refresh Data", type="secondary"):
            st.success("✅ Demo: Data refreshed!")
            
    with col3:
        if st.button("⚠️ Alert Settings", type="secondary"):
            st.info("🔔 Demo: Alert preferences available!")
            
    with col4:
        if st.button("📱 Mobile View", type="secondary"):
            st.info("📱 Demo: Mobile optimization active!")

# Footer
st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("### 🔗 Demo Features")
    st.markdown("""
    - ✅ Modern UI/UX Design
    - ✅ Interactive Components
    - ✅ Real-time Animations
    - ✅ Gamification Elements
    """)

with col2:
    st.markdown("### 📈 Demo Summary")
    
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    with summary_col1:
        st.metric("Demo Orders", "12,547")
    
    with summary_col2:
        st.metric("Avg Performance", f"{performance_score:.1f}%")
    
    with summary_col3:
        st.metric("Demo Couriers", len(df_ndr_by_courier))

with col3:
    st.markdown("### ⏰ Demo Status")
    st.success("🟢 Demo Active")
    st.info(f"🕐 Generated: {datetime.now().strftime('%H:%M:%S')}")
    st.markdown("**Mode:** Interactive Demo")

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
    " title="Demo Feedback">
        💬
    </button>
</div>
""", unsafe_allow_html=True)