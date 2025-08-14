# 📦 RTO / NDR Analytics Dashboard

![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-latest-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview

The RTO / NDR Analytics Dashboard is a comprehensive data visualization platform designed for analyzing **Return-to-Origin (RTO)** and **Non-Delivery Report (NDR)** metrics in logistics and e-commerce operations. This dashboard helps logistics teams, operations managers, and data analysts track courier performance, monitor delivery efficiency, and analyze multi-attempt orders to optimize supply chain operations.

The platform provides actionable insights into delivery failures, courier performance benchmarks, and operational bottlenecks that impact customer satisfaction and business costs.

## Key Features

- **📊 Real-time KPIs** - Track total RTOs, average NDR percentages, delivery times, and high reattempt rates
- **📈 Interactive Trend Charts** - Visualize daily RTO trends and delivery patterns using Altair
- **📚 Stacked Failure Analysis** - Analyze failure reasons by courier partner with detailed breakdowns
- **🍩 Action Distribution** - Donut charts showing order action categorization and resolution paths
- **🔍 Pincode Search** - Search and analyze courier performance by specific postal codes
- **⚡ Smart Caching** - Optimized data loading with Streamlit's built-in caching mechanisms
- **🔗 Databricks Integration** - Direct connection to Databricks SQL warehouses for real-time data
- **🌙 Dark Mode Design** - Modern, eye-friendly interface optimized for operations centers

## Architecture / Data Flow

The dashboard follows a streamlined data pipeline architecture:

**Databricks Tables** → **SQLAlchemy Engine** → **Cached Data Loaders** → **Streamlit Visual Layers**

1. **Data Source**: Pre-calculated summary tables in Databricks provide optimized query performance
2. **Connection Layer**: SQLAlchemy engine manages secure connections to Databricks SQL warehouses
3. **Caching Layer**: Streamlit's `@st.cache_data` and `@st.cache_resource` decorators minimize query overhead
4. **Visualization Layer**: Dual-engine approach using Altair for statistical charts and Plotly for interactive visualizations

## Tech Stack

- **Frontend Framework**: Streamlit
- **Data Processing**: Python, Pandas, NumPy
- **Database Connectivity**: SQLAlchemy, Databricks SQL Connector, Databricks SQLAlchemy
- **Visualization**: Plotly, Altair
- **Environment Management**: python-dotenv
- **Security**: Cryptography
- **Data Formats**: PyArrow (for optimized data transfer)

## Data Sources / Tables

The dashboard connects to the following Databricks tables and views:

| Table/View Name | Description |
|----------------|-------------|
| `summary_daily_rto` | Daily aggregated RTO counts and trends |
| `summary_ndr_by_courier` | NDR percentages grouped by courier partner |
| `summary_delivery_time` | Average delivery times by product category |
| `delivery_attempts_impact` | Analysis of delivery attempt patterns |
| `high_attempts_impact` | Orders requiring multiple delivery attempts |
| `failure_reasons` | Categorized delivery failure reasons |
| `courier_partner_failure_reason` | Failure reasons mapped to specific courier partners |
| `impact_of_delivery_attempts` | Business impact analysis of delivery attempts |
| `rto_ndr` | Main fact table containing detailed RTO/NDR records |
| `top_couriers_by_pincode` | View showing top-performing couriers by postal code |

## KPIs Explained

| KPI | Description | Calculation |
|-----|-------------|-------------|
| **📦 Total RTOs** | Total count of Return-to-Origin orders | Sum of all RTO events from daily summary |
| **🚚 Avg NDR %** | Average Non-Delivery Report percentage across all couriers | Mean of NDR percentages by courier partner |
| **⏱️ Avg Delivery Time (Days)** | Average days from dispatch to successful delivery | Mean delivery time across all product categories |
| **High Reattempt %** | Percentage of orders requiring multiple delivery attempts | (High attempt orders / Total orders) × 100 |
| **Top Failure Reason** | Most common reason for delivery failures | Mode of failure_reason field |
| **🏆 Top Courier Partner** | Courier with lowest NDR percentage | Courier partner with minimum NDR rate |

## Installation & Local Setup

### Prerequisites

- **Python 3.10+** installed on your system
- **Databricks workspace** with SQL warehouse access
- **Personal Access Token** for Databricks authentication

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/ritika577/rto-ndr-analytics-dashboard.git
   cd rto-ndr-analytics-dashboard
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   ACCESS_TOKEN=your_databricks_personal_access_token
   SERVER_HOSTNAME=your_databricks_hostname.cloud.databricks.com
   HTTP_PATH=/sql/1.0/warehouses/your_warehouse_id
   ```

5. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

The dashboard will be available at `http://localhost:8501`

## Using Streamlit Secrets

For production deployment, use Streamlit's secrets management instead of `.env` files:

Create a `.streamlit/secrets.toml` file:
```toml
[databricks]
ACCESS_TOKEN = "your_databricks_personal_access_token"
SERVER_HOSTNAME = "your_databricks_hostname.cloud.databricks.com"
HTTP_PATH = "/sql/1.0/warehouses/your_warehouse_id"
```

Or configure secrets through the Streamlit Community Cloud UI:
1. Go to your app settings
2. Navigate to "Secrets" section
3. Add the databricks configuration block

## Deployment (Streamlit Community Cloud)

1. **Connect GitHub Repository**
   - Link your GitHub repository to Streamlit Community Cloud
   - Select the main branch and `streamlit_app.py` as the entry point

2. **Configure Secrets**
   - Add your Databricks credentials in the secrets management UI
   - Use the `[databricks]` section format shown above

3. **Deploy Application**
   - Click "Deploy" to launch your application
   - Monitor the deployment logs for any issues

### Common Deployment Notes

- **Border Parameter**: Remove `border=True` parameters if using older Streamlit versions, or upgrade to Streamlit 1.28+
- **Caching**: The app uses `st.cache_resource` and `st.cache_data` decorators for optimal performance
- **Memory Management**: Large datasets are automatically cached to reduce query load

## Screenshots / UI Preview

![image1](image1)
*Dashboard Sections - Overview of KPIs, trends, and courier performance metrics*

![image2](image2)  
*Pincode Search UI - Interactive search functionality for location-based courier analysis*

## Configuration & Customization

### Color Palettes
Modify the gradient colors in the visualization sections:
```python
# For Plotly charts
gradient_colors = sample_colorscale("RdBu", [i/(len(df)-1) for i in range(len(df))])

# For Altair charts  
color=alt.Color('avg_delivery_days:Q', scale=alt.Scale(scheme='blues'))
```

### KPI Labels
Update KPI definitions in the `kpis` list:
```python
kpis = [
    ("📦 Total RTOs", df_daily_rto["rto_count"].sum()),
    ("🚚 Avg NDR %", round(df_ndr_by_courier["ndr_percentage"].mean(), 2)),
    # Add your custom KPIs here
]
```

### Adding New Charts
Follow the existing pattern for new visualizations:
```python
chart = alt.Chart(your_data).mark_bar().encode(
    x=alt.X('field:Q', title="X Label"),
    y=alt.Y('field:N', title="Y Label")
).properties(width=700, height=400)

st.altair_chart(chart, use_container_width=True)
```

## Performance Tips

- **Limit SELECT Queries**: Avoid `SELECT *` for large tables; specify required columns
- **Use Caching Effectively**: Leverage `@st.cache_data` for data loading functions
- **Subset Columns**: Load only necessary columns to reduce memory usage
- **Lazy Loading**: Implement conditional data loading based on user interactions
- **Avoid Heavy Recomputation**: Cache expensive operations and aggregations
- **Database Optimization**: Use pre-calculated summary tables instead of real-time aggregations

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `KeyError: 'ACCESS_TOKEN'` | Missing environment variables | Check `.env` file or Streamlit secrets configuration |
| `TypeError: container() got unexpected keyword 'border'` | Streamlit version compatibility | Remove `border=True` or upgrade to Streamlit 1.28+ |
| `ModuleNotFoundError` | Missing dependencies | Run `pip install -r requirements.txt` |
| Empty DataFrames | Database connection or query issues | Verify Databricks credentials and table existence |
| Connection timeout | Network or authentication issues | Check HTTP_PATH and SERVER_HOSTNAME values |

## Roadmap

Future enhancements planned for the dashboard:

- **🔐 Authentication System** - Role-based access control for different user types
- **👥 Role-based Views** - Customized dashboards for managers, analysts, and operators  
- **🚨 Alerting Thresholds** - Automated notifications for KPI anomalies
- **📊 Export Functionality** - CSV/Excel export for reports and analysis
- **🔄 Automated Data Ingestion** - Enhanced Airflow pipeline (placeholder exists: `airflow_rto_ndr_analytics.py`)
- **📱 Mobile Responsiveness** - Optimized layouts for mobile devices
- **🎯 Predictive Analytics** - ML models for delivery success prediction
- **📍 Geographic Mapping** - Location-based delivery performance visualization

## Contributing

We welcome contributions to improve the dashboard!

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and test thoroughly
4. **Commit your changes**
   ```bash
   git commit -m "Add: description of your feature"
   ```
5. **Push to your branch**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request** with a detailed description of your changes

Please ensure your code follows the existing style and includes appropriate documentation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Databricks** for providing the data platform and SQL warehouse capabilities
- **Streamlit** for the excellent dashboard framework
- **Plotly & Altair** for powerful visualization libraries
- The **open-source community** for the foundational libraries that make this project possible