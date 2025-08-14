# 📦 Enhanced RTO/NDR Analytics Dashboard

A highly interactive, modern analytics dashboard for Return-to-Origin (RTO) and Non-Delivery Reports (NDR) analysis with real-time features, gamification elements, and AI-powered insights.

## 🚀 Key Features

### 🎯 Real-Time Features
- **Auto-refresh functionality** with customizable countdown timer for live data updates
- **Real-time counter animations** for KPI metrics with pulse effects
- **Smart alerts system** with color-coded notifications for critical thresholds
- **Live notification panel** with performance status indicators

### 🎮 Gamification Elements
- **Performance badges system** with achievement tracking (Elite, Gold, Silver, Bronze)
- **Interactive leaderboard** for courier partners with ranking animations
- **Progress rings** for performance score visualization
- **Achievement displays** with animated progress bars

### 📊 Advanced Visualizations
- **Interactive charts** with multiple view options (Line, Area, Bar)
- **Enhanced racing bar charts** showing courier performance competitions
- **3D donut charts** for failure pattern analysis with pull effects
- **Heatmap visualizations** for delivery performance by category
- **Progress column charts** in data tables

### 🎨 Enhanced UI/UX
- **Modern gradient color schemes** with professional styling
- **Animated KPI cards** with hover effects and custom icons
- **Smart control center** with interactive filters and quick actions
- **Mobile-responsive design** with touch-friendly controls
- **Custom CSS animations** for smooth transitions and loading states

### 🤖 AI & Predictive Features
- **AI-powered insights panel** with smart analytics
- **Performance scoring** with confidence indicators
- **Automated recommendations** with actionable insights
- **Interactive chatbot assistant** for analytics queries in sidebar

### 📱 Interactive Components
- **Enhanced sidebar navigation** with gradient styling and controls
- **Quick action buttons** with loading states and feedback
- **Smart search functionality** with enhanced pincode analytics
- **Data export capabilities** with multiple format options
- **Tabbed data explorer** with enhanced table views

## 🛠️ Technical Stack

- **Frontend**: Streamlit with custom HTML/CSS
- **Visualization**: Plotly, Altair with interactive features
- **Data Processing**: Pandas with enhanced analytics
- **Database**: Databricks connection via SQLAlchemy
- **Styling**: Modern CSS with gradients, animations, and responsive design

## 📋 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ritika577/rto-ndr-analytics-dashboard.git
   cd rto-ndr-analytics-dashboard
   ```

2. **Install dependencies**:
   ```bash
   pip install streamlit plotly altair pandas sqlalchemy python-dotenv
   ```

3. **Set up environment variables**:
   Create a `.env` file based on `.env.example`:
   ```bash
   ACCESS_TOKEN=your_databricks_access_token
   SERVER_HOSTNAME=your_server_hostname
   HTTP_PATH=your_http_path
   ```

4. **Run the dashboard**:
   ```bash
   streamlit run streamlit_app.py
   ```

## 🎯 Dashboard Sections

### 1. **Real-Time Overview**
- Live performance metrics with animated counters
- Critical alerts and status indicators
- Auto-refresh controls and data freshness status

### 2. **Enhanced KPI Cards**
- Animated metrics with gradient effects
- Delta indicators with trend analysis
- Performance badges and achievement tracking

### 3. **Interactive Leaderboard**
- Courier ranking with progress bars
- Performance scores and badges
- Real-time competition tracking

### 4. **Advanced Charts**
- Multi-style trend analysis (Line, Area, Bar)
- Interactive controls for time range and filters
- Enhanced tooltips and hover effects

### 5. **Smart Search & Analytics**
- Pincode-based delivery analytics
- Enhanced search results with summary metrics
- Geographic performance insights

### 6. **Courier Performance Dashboard**
- Multiple visualization styles
- Racing bar charts with animations
- Performance comparison tools

### 7. **AI-Powered Insights**
- Automated performance analysis
- Smart recommendations and alerts
- Predictive insights with confidence scores

### 8. **Data Explorer**
- Tabbed interface for different data views
- Enhanced tables with progress columns
- Interactive filtering and sorting

## 🎨 Design Features

### Color Palette
- **Primary Gradient**: `#667eea → #764ba2`
- **Success Gradient**: `#4facfe → #00f2fe`
- **Warning Gradient**: `#43e97b → #38f9d7`
- **Danger Gradient**: `#fa709a → #fee140`

### Animations & Effects
- Smooth CSS transitions with cubic-bezier timing
- Pulse animations for real-time indicators
- Hover effects with transform scaling
- 3D effects on charts with pull animations

### Responsive Design
- Mobile-first approach with breakpoints
- Touch-friendly controls and spacing
- Scalable typography and components

## 🔧 Configuration Options

### Auto-Refresh Settings
- Customizable refresh intervals (30s, 1m, 5m, 10m)
- Enable/disable auto-refresh toggle
- Real-time countdown display

### Performance Thresholds
- Configurable NDR percentage alerts
- Custom performance badge criteria
- Adjustable scoring algorithms

### Visual Preferences
- Multiple chart style options
- Customizable color schemes
- Layout density controls

## 📊 Performance Metrics

- **Dashboard Load Time**: < 3 seconds
- **Real-time Updates**: Every 30-600 seconds (configurable)
- **Mobile Responsiveness**: Optimized for 320px+ screens
- **Data Accuracy**: Real-time connection to Databricks

## 🚀 Recent Enhancements

### Version 2.0 Features
- ✅ Real-time auto-refresh with countdown timer
- ✅ Interactive leaderboard with progress tracking
- ✅ AI-powered insights and recommendations
- ✅ Enhanced sidebar with smart controls
- ✅ Multiple chart visualization styles
- ✅ Performance badges and gamification
- ✅ 3D donut charts with enhanced styling
- ✅ Mobile-responsive design improvements
- ✅ Smart search with pincode analytics
- ✅ Interactive data tables with progress columns

## 🔮 Future Roadmap

- [ ] Advanced predictive analytics with ML models
- [ ] Real-time geographical maps with delivery routes
- [ ] Advanced export features (PDF, Excel, PowerBI)
- [ ] Custom dashboard themes and branding
- [ ] Advanced filtering and drill-down capabilities
- [ ] Integration with external APIs for enhanced data
- [ ] Multi-language support
- [ ] Advanced user authentication and permissions

## 📞 Support & Feedback

For issues, suggestions, or contributions, please:
- Create an issue on GitHub
- Use the feedback button in the dashboard
- Contact the development team

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ using Streamlit and modern web technologies**