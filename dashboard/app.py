"""
🏆 ULTIMATE PREMIUM DASHBOARD - ENHANCED
Executive-Level Sales Command Center with Interactive Cards
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM CSS - ULTRA PREMIUM ============
st.markdown("""
    <style>
    /* ===== FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    /* ===== BACKGROUND ===== */
    .stApp {
        background: #070b14;
    }
    
    /* ===== MAIN CONTAINER ===== */
    .main-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    /* ===== HEADER ===== */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.2rem 0 1.5rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.04);
        margin-bottom: 1.8rem;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .header-icon {
        font-size: 2.5rem;
    }
    
    .header-title {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
    }
    
    .header-title span {
        background: linear-gradient(135deg, #818cf8, #a78bfa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.3);
        font-size: 0.85rem;
        font-weight: 400;
        letter-spacing: 1px;
        margin: 0;
    }
    
    .header-right {
        text-align: right;
    }
    
    .header-time {
        color: rgba(255,255,255,0.25);
        font-size: 0.85rem;
        letter-spacing: 1px;
    }
    
    /* ===== PREMIUM METRIC CARDS ===== */
    .premium-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        height: 100%;
        min-height: 130px;
        cursor: pointer;
    }
    
    .premium-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.03), transparent);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-6px);
        border-color: rgba(255,255,255,0.15);
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }
    
    .premium-card:hover::before {
        opacity: 1;
    }
    
    .premium-card .card-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }
    
    .premium-card .card-icon {
        font-size: 1.8rem;
        opacity: 0.6;
    }
    
    .premium-card .card-badge {
        font-size: 0.65rem;
        font-weight: 600;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-up {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
    }
    
    .badge-down {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
    }
    
    .badge-neutral {
        background: rgba(255,255,255,0.05);
        color: rgba(255,255,255,0.3);
    }
    
    .premium-card .card-label {
        color: rgba(255,255,255,0.4);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .premium-card .card-value {
        color: #ffffff;
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0.2rem 0;
    }
    
    .premium-card .card-sub {
        color: rgba(255,255,255,0.3);
        font-size: 0.85rem;
    }
    
    .premium-card .card-change {
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .change-up { color: #34d399; }
    .change-down { color: #f87171; }
    
    /* Card Accent Colors */
    .card-purple { border-top: 3px solid #818cf8; }
    .card-pink { border-top: 3px solid #f472b6; }
    .card-blue { border-top: 3px solid #60a5fa; }
    .card-green { border-top: 3px solid #34d399; }
    .card-orange { border-top: 3px solid #fbbf24; }
    .card-cyan { border-top: 3px solid #22d3ee; }
    .card-red { border-top: 3px solid #f87171; }
    .card-indigo { border-top: 3px solid #a78bfa; }
    
    /* Click Hint */
    .click-hint {
        color: rgba(255,255,255,0.1);
        font-size: 0.55rem;
        text-align: center;
        margin-top: 0.3rem;
        letter-spacing: 0.5px;
    }
    
    /* ===== SECTION HEADERS ===== */
    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.2rem 0 0.8rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.04);
        margin-bottom: 1rem;
    }
    
    .section-title {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 700;
        letter-spacing: -0.3px;
        margin: 0;
    }
    
    .section-title span {
        background: linear-gradient(135deg, #818cf8, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* ===== CHART CONTAINERS ===== */
    .chart-container {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 16px;
        padding: 1.5rem 1.2rem 1rem 1.2rem;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .chart-container:hover {
        border-color: rgba(255,255,255,0.08);
    }
    
    /* ===== STATS BOX ===== */
    .stats-box {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        height: 100%;
        transition: all 0.3s ease;
    }
    
    .stats-box:hover {
        border-color: rgba(255,255,255,0.08);
    }
    
    .stats-box .stat-header {
        color: rgba(255,255,255,0.3);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
    
    .stats-box .stat-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.02);
    }
    
    .stats-box .stat-item:last-child {
        border-bottom: none;
    }
    
    .stats-box .stat-label {
        color: rgba(255,255,255,0.5);
        font-size: 0.9rem;
    }
    
    .stats-box .stat-value {
        color: #ffffff;
        font-size: 1rem;
        font-weight: 600;
    }
    
    .stat-highlight { color: #818cf8; }
    .stat-green { color: #34d399; }
    .stat-pink { color: #f472b6; }
    .stat-orange { color: #fbbf24; }
    
    /* ===== PROGRESS BARS ===== */
    .progress-bar {
        background: rgba(255,255,255,0.05);
        border-radius: 4px;
        height: 5px;
        margin-top: 0.3rem;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 1s ease;
    }
    
    /* ===== DATA TABLE ===== */
    .dataframe {
        border-radius: 16px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255,255,255,0.04) !important;
    }
    
    .dataframe thead tr th {
        background: rgba(255,255,255,0.03) !important;
        color: rgba(255,255,255,0.4) !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        border: none !important;
        padding: 1rem 1.2rem !important;
    }
    
    .dataframe tbody tr td {
        color: rgba(255,255,255,0.7) !important;
        border: none !important;
        padding: 0.8rem 1.2rem !important;
        font-size: 0.9rem !important;
    }
    
    .dataframe tbody tr:hover {
        background: rgba(255,255,255,0.02) !important;
    }
    
    /* ===== SIDEBAR ===== */
    .css-1d391kg {
        background: rgba(7, 11, 20, 0.98) !important;
        border-right: 1px solid rgba(255,255,255,0.04) !important;
    }
    
    .sidebar-label {
        color: rgba(255,255,255,0.25);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.05);
        font-size: 0.7rem;
        padding: 2rem 0 0.5rem 0;
        border-top: 1px solid rgba(255,255,255,0.02);
        margin-top: 2rem;
        letter-spacing: 1px;
    }
    
    /* ===== MODAL / SUMMARY POPUP ===== */
    .summary-popup {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin: 0.5rem 0 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .summary-popup .summary-title {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .summary-popup .summary-text {
        color: rgba(255,255,255,0.7);
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .summary-popup .summary-highlight {
        color: #818cf8;
        font-weight: 600;
    }
    
    .summary-popup .summary-green {
        color: #34d399;
        font-weight: 600;
    }
    
    .summary-popup .summary-pink {
        color: #f472b6;
        font-weight: 600;
    }
    
    .summary-popup .summary-orange {
        color: #fbbf24;
        font-weight: 600;
    }
    
    /* Close button */
    .close-btn {
        color: rgba(255,255,255,0.2);
        float: right;
        cursor: pointer;
        font-size: 1.2rem;
        transition: color 0.3s ease;
    }
    
    .close-btn:hover {
        color: rgba(255,255,255,0.5);
    }
    </style>
""", unsafe_allow_html=True)

# ============ LOAD DATA ============
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/forecasts/90_day_forecast.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except:
        return None

df = load_data()

if df is None:
    st.error("❌ Data not found. Please run the pipeline first.")
    st.stop()

# ============ SESSION STATE FOR POPUPS ============
if 'show_summary' not in st.session_state:
    st.session_state.show_summary = None

# ============ SIDEBAR ============
with st.sidebar:
    st.markdown("""
        <div style='padding: 1.5rem 0 1rem 0; text-align: center;'>
            <div style='font-size: 2.5rem;'>🏆</div>
            <h2 style='color: white; font-weight: 700; margin: 0; font-size: 1.5rem;'>Command</h2>
            <p style='color: rgba(255,255,255,0.2); font-size: 0.7rem; letter-spacing: 2px;'>CONTROL CENTER</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<p class="sidebar-label">📅 Date Range</p>', unsafe_allow_html=True)
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    
    date_range = st.date_input(
        "",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown('<p class="sidebar-label">⚙️ Settings</p>', unsafe_allow_html=True)
    show_confidence = st.toggle("Confidence Bands", value=True)
    
    st.markdown("---")
    
    st.markdown('<p class="sidebar-label">📊 Quick Stats</p>', unsafe_allow_html=True)
    
    total = df['Predicted_Sales'].sum()
    avg = df['Predicted_Sales'].mean()
    
    st.markdown(f"""
        <div style='background: rgba(255,255,255,0.02); border-radius: 12px; padding: 0.8rem 1rem; border: 1px solid rgba(255,255,255,0.03);'>
            <div style='display: flex; justify-content: space-between; padding: 0.3rem 0;'>
                <span style='color: rgba(255,255,255,0.3); font-size: 0.85rem;'>Total</span>
                <span style='color: #818cf8; font-weight: 600; font-size: 0.95rem;'>${total:,.0f}</span>
            </div>
            <div style='display: flex; justify-content: space-between; padding: 0.3rem 0;'>
                <span style='color: rgba(255,255,255,0.3); font-size: 0.85rem;'>Average</span>
                <span style='color: #34d399; font-weight: 600; font-size: 0.95rem;'>${avg:,.0f}</span>
            </div>
            <div style='display: flex; justify-content: space-between; padding: 0.3rem 0;'>
                <span style='color: rgba(255,255,255,0.3); font-size: 0.85rem;'>Days</span>
                <span style='color: #f472b6; font-weight: 600; font-size: 0.95rem;'>{len(df)}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    csv = df.to_csv(index=False)
    st.download_button(
        label="⬇️ Export Data",
        data=csv,
        file_name="sales_forecast.csv",
        mime="text/csv"
    )
    
    st.markdown(f"""
        <div style='text-align: center; color: rgba(255,255,255,0.05); font-size: 0.6rem; padding-top: 2rem; letter-spacing: 1px;'>
            {datetime.now().strftime('%Y')} · Future Interns
        </div>
    """, unsafe_allow_html=True)

# ============ FILTER DATA ============
if len(date_range) == 2:
    start_date, end_date = date_range
    df_filtered = df[(df['Date'] >= pd.Timestamp(start_date)) & 
                     (df['Date'] <= pd.Timestamp(end_date))]
else:
    df_filtered = df

# ============ HEADER ============
st.markdown(f"""
    <div class="header-container">
        <div class="header-left">
            <div class="header-icon">📊</div>
            <div>
                <h1 class="header-title">Executive <span>Dashboard</span></h1>
                <p class="header-subtitle">SALES FORECASTING · COMMAND CENTER</p>
            </div>
        </div>
        <div class="header-right">
            <div class="header-time">{datetime.now().strftime('%B %d, %Y · %I:%M %p')}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ============ CALCULATE METRICS ============
total = df_filtered['Predicted_Sales'].sum()
avg = df_filtered['Predicted_Sales'].mean()
peak = df_filtered['Predicted_Sales'].max()
min_val = df_filtered['Predicted_Sales'].min()

half = len(df_filtered) // 2
first = df_filtered['Predicted_Sales'].iloc[:half].mean() if half > 0 else avg
second = df_filtered['Predicted_Sales'].iloc[half:].mean() if half > 0 else avg
growth = ((second - first) / first) * 100 if first > 0 else 0

peak_day = df_filtered.loc[df_filtered['Predicted_Sales'].idxmax(), 'Day_Name'] if len(df_filtered) > 0 else 'N/A'
low_day = df_filtered.loc[df_filtered['Predicted_Sales'].idxmin(), 'Day_Name'] if len(df_filtered) > 0 else 'N/A'
peak_date = df_filtered.loc[df_filtered['Predicted_Sales'].idxmax(), 'Date'] if len(df_filtered) > 0 else None
low_date = df_filtered.loc[df_filtered['Predicted_Sales'].idxmin(), 'Date'] if len(df_filtered) > 0 else None

weeks = len(df_filtered['Week'].unique())
monthly = df_filtered.groupby('Month')['Predicted_Sales'].sum()
best_month = monthly.idxmax() if len(monthly) > 0 else 'N/A'
best_month_val = monthly.max() if len(monthly) > 0 else 0

# ============ SUMMARY FUNCTIONS ============
def show_summary(card_type):
    st.session_state.show_summary = card_type

def clear_summary():
    st.session_state.show_summary = None

# ============ METRIC CARDS ============
st.markdown('<p style="color: rgba(255,255,255,0.15); font-size: 0.7rem; text-align: center; margin-bottom: 0.5rem;">💡 Click any card for detailed summary</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💰", key="card_total", use_container_width=True):
        show_summary("total")
    st.markdown(f"""
        <div class="premium-card card-purple" onclick="document.getElementById('card_total').click()">
            <div class="card-top">
                <span class="card-icon">💰</span>
                <span class="card-badge badge-up">● Active</span>
            </div>
            <div class="card-label">Total Revenue</div>
            <div class="card-value">${total:,.0f}</div>
            <div class="card-sub">{len(df_filtered)} days forecast</div>
            <div class="click-hint">▼ Click for details</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("📈", key="card_avg", use_container_width=True):
        show_summary("avg")
    st.markdown(f"""
        <div class="premium-card card-pink">
            <div class="card-top">
                <span class="card-icon">📈</span>
                <span class="card-badge badge-up">● Growing</span>
            </div>
            <div class="card-label">Daily Average</div>
            <div class="card-value">${avg:,.0f}</div>
            <div class="card-sub">per day</div>
            <div class="click-hint">▼ Click for details</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    if st.button("📊", key="card_growth", use_container_width=True):
        show_summary("growth")
    badge_class = "badge-up" if growth >= 0 else "badge-down"
    change_class = "change-up" if growth >= 0 else "change-down"
    st.markdown(f"""
        <div class="premium-card card-green">
            <div class="card-top">
                <span class="card-icon">📊</span>
                <span class="card-badge {badge_class}">{'+' if growth >= 0 else ''}{growth:.1f}%</span>
            </div>
            <div class="card-label">Growth Trend</div>
            <div class="card-value">{growth:+.1f}%</div>
            <div class="card-change {change_class}">{'▲ Increasing' if growth >= 0 else '▼ Decreasing'}</div>
            <div class="click-hint">▼ Click for details</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    if st.button("🔥", key="card_peak", use_container_width=True):
        show_summary("peak")
    st.markdown(f"""
        <div class="premium-card card-orange">
            <div class="card-top">
                <span class="card-icon">🔥</span>
                <span class="card-badge badge-neutral">Peak</span>
            </div>
            <div class="card-label">Peak Day</div>
            <div class="card-value">${peak:,.0f}</div>
            <div class="card-sub">{peak_day}</div>
            <div class="click-hint">▼ Click for details</div>
        </div>
    """, unsafe_allow_html=True)

# Second Row - More Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📉", key="card_low", use_container_width=True):
        show_summary("low")
    st.markdown(f"""
        <div class="premium-card card-blue">
            <div class="card-top">
                <span class="card-icon">📉</span>
                <span class="card-badge badge-neutral">Low</span>
            </div>
            <div class="card-label">Lowest Day</div>
            <div class="card-value">${min_val:,.0f}</div>
            <div class="card-sub">{low_day}</div>
            <div class="click-hint">▼ Click for details</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("📅", key="card_period", use_container_width=True):
        show_summary("period")
    st.markdown(f"""
        <div class="premium-card card-cyan">
            <div class="card-top">
                <span class="card-icon">📅</span>
                <span class="card-badge badge-neutral">Period</span>
            </div>
            <div class="card-label">Forecast Period</div>
            <div class="card-value">{len(df_filtered)} Days</div>
            <div class="card-sub">{weeks} Weeks</div>
            <div class="click-hint">▼ Click for details</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    if st.button("🏆", key="card_month", use_container_width=True):
        show_summary("month")
    st.markdown(f"""
        <div class="premium-card card-indigo">
            <div class="card-top">
                <span class="card-icon">🏆</span>
                <span class="card-badge badge-up">Best</span>
            </div>
            <div class="card-label">Best Month</div>
            <div class="card-value">{best_month}</div>
            <div class="card-sub">${best_month_val:,.0f} total</div>
            <div class="click-hint">▼ Click for details</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    if st.button("📏", key="card_range", use_container_width=True):
        show_summary("range")
    range_val = peak - min_val
    st.markdown(f"""
        <div class="premium-card card-red">
            <div class="card-top">
                <span class="card-icon">📏</span>
                <span class="card-badge badge-neutral">Range</span>
            </div>
            <div class="card-label">Sales Range</div>
            <div class="card-value">${range_val:,.0f}</div>
            <div class="card-sub">${min_val:,.0f} → ${peak:,.0f}</div>
            <div class="click-hint">▼ Click for details</div>
        </div>
    """, unsafe_allow_html=True)

# ============ SUMMARY POPUP ============
if st.session_state.show_summary is not None:
    st.markdown("---")
    
    # Close button
    col_close, col_content = st.columns([1, 11])
    with col_close:
        if st.button("✕", key="close_summary"):
            clear_summary()
    
    with col_content:
        if st.session_state.show_summary == "total":
            st.markdown(f"""
                <div class="summary-popup">
                    <div class="summary-title">💰 Total Revenue Summary</div>
                    <div class="summary-text">
                        <p>📊 <span class="summary-highlight">Total Sales:</span> <b>${total:,.0f}</b> over {len(df_filtered)} days</p>
                        <p>📈 <span class="summary-green">Average per day:</span> <b>${avg:,.0f}</b></p>
                        <p>🔥 <span class="summary-pink">Peak day:</span> <b>${peak:,.0f}</b> on {peak_day} ({peak_date.strftime('%b %d, %Y') if peak_date else 'N/A'})</p>
                        <p>📉 <span class="summary-orange">Lowest day:</span> <b>${min_val:,.0f}</b> on {low_day}</p>
                        <p style='margin-top: 0.5rem; color: rgba(255,255,255,0.4); font-size: 0.85rem;'>
                            💡 <b>Business Insight:</b> Total revenue of ${total:,.0f} is expected over the forecast period. 
                            The business should plan inventory and staffing based on the average daily sales of ${avg:,.0f}.
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        elif st.session_state.show_summary == "avg":
            st.markdown(f"""
                <div class="summary-popup">
                    <div class="summary-title">📈 Daily Average Summary</div>
                    <div class="summary-text">
                        <p>📊 <span class="summary-highlight">Average Daily Sales:</span> <b>${avg:,.0f}</b></p>
                        <p>📅 <span class="summary-green">Total days:</span> <b>{len(df_filtered)}</b></p>
                        <p>💰 <span class="summary-pink">Total Revenue:</span> <b>${total:,.0f}</b></p>
                        <p>📈 <span class="summary-orange">Growth Trend:</span> <b>{growth:+.1f}%</b></p>
                        <p style='margin-top: 0.5rem; color: rgba(255,255,255,0.4); font-size: 0.85rem;'>
                            💡 <b>Business Insight:</b> The business should expect ${avg:,.0f} in daily sales. 
                            This means ${total:,.0f} in total revenue over the forecast period.
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        elif st.session_state.show_summary == "growth":
            st.markdown(f"""
                <div class="summary-popup">
                    <div class="summary-title">📊 Growth Trend Summary</div>
                    <div class="summary-text">
                        <p>📈 <span class="summary-highlight">Growth Rate:</span> <b>{growth:+.1f}%</b></p>
                        <p>📊 <span class="summary-green">First Half Avg:</span> <b>${first:,.0f}</b></p>
                        <p>📊 <span class="summary-pink">Second Half Avg:</span> <b>${second:,.0f}</b></p>
                        <p style='margin-top: 0.5rem; color: rgba(255,255,255,0.4); font-size: 0.85rem;'>
                            💡 <b>Business Insight:</b> Sales are {'increasing' if growth > 0 else 'decreasing'} at {abs(growth):.1f}% over the forecast period. 
                            {'This is a positive trend indicating growing demand.' if growth > 0 else 'Consider marketing initiatives to reverse this trend.'}
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        elif st.session_state.show_summary == "peak":
            st.markdown(f"""
                <div class="summary-popup">
                    <div class="summary-title">🔥 Peak Day Summary</div>
                    <div class="summary-text">
                        <p>📊 <span class="summary-highlight">Peak Sales:</span> <b>${peak:,.0f}</b></p>
                        <p>📅 <span class="summary-green">Date:</span> <b>{peak_day}</b></p>
                        <p>📈 <span class="summary-pink">Compared to Average:</span> <b>+{((peak - avg) / avg * 100):.0f}%</b></p>
                        <p style='margin-top: 0.5rem; color: rgba(255,255,255,0.4); font-size: 0.85rem;'>
                            💡 <b>Business Insight:</b> The peak day of ${peak:,.0f} is {((peak - avg) / avg * 100):.0f}% above average. 
                            Plan extra staff and inventory for {peak_day}s. This is a prime opportunity for promotions.
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        elif st.session_state.show_summary == "low":
            st.markdown(f"""
                <div class="summary-popup">
                    <div class="summary-title">📉 Lowest Day Summary</div>
                    <div class="summary-text">
                        <p>📊 <span class="summary-highlight">Lowest Sales:</span> <b>${min_val:,.0f}</b></p>
                        <p>📅 <span class="summary-green">Date:</span> <b>{low_day}</b></p>
                        <p>📈 <span class="summary-pink">Compared to Average:</span> <b>{(min_val - avg) / avg * 100:.0f}%</b></p>
                        <p style='margin-top: 0.5rem; color: rgba(255,255,255,0.4); font-size: 0.85rem;'>
                            💡 <b>Business Insight:</b> The lowest day of ${min_val:,.0f} is {(min_val - avg) / avg * 100:.0f}% below average. 
                            Consider running promotions or special offers on {low_day}s to boost sales.
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        elif st.session_state.show_summary == "period":
            st.markdown(f"""
                <div class="summary-popup">
                    <div class="summary-title">📅 Forecast Period Summary</div>
                    <div class="summary-text">
                        <p>📊 <span class="summary-highlight">Total Days:</span> <b>{len(df_filtered)}</b></p>
                        <p>📅 <span class="summary-green">Total Weeks:</span> <b>{weeks}</b></p>
                        <p>📈 <span class="summary-pink">Start Date:</span> <b>{df_filtered['Date'].min().strftime('%b %d, %Y')}</b></p>
                        <p>📉 <span class="summary-orange">End Date:</span> <b>{df_filtered['Date'].max().strftime('%b %d, %Y')}</b></p>
                        <p style='margin-top: 0.5rem; color: rgba(255,255,255,0.4); font-size: 0.85rem;'>
                            💡 <b>Business Insight:</b> The forecast covers {weeks} weeks ({len(df_filtered)} days). 
                            Use this timeframe for strategic planning and resource allocation.
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        elif st.session_state.show_summary == "month":
            st.markdown(f"""
                <div class="summary-popup">
                    <div class="summary-title">🏆 Best Month Summary</div>
                    <div class="summary-text">
                        <p>📊 <span class="summary-highlight">Best Month:</span> <b>{best_month}</b></p>
                        <p>📈 <span class="summary-green">Total Sales:</span> <b>${best_month_val:,.0f}</b></p>
                        <p>📅 <span class="summary-pink">Average per day:</span> <b>${best_month_val / 30:,.0f}</b></p>
                        <p style='margin-top: 0.5rem; color: rgba(255,255,255,0.4); font-size: 0.85rem;'>
                            💡 <b>Business Insight:</b> {best_month} is the highest performing month with ${best_month_val:,.0f} in sales. 
                            Plan marketing campaigns and staffing for next {best_month} based on this success.
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        elif st.session_state.show_summary == "range":
            st.markdown(f"""
                <div class="summary-popup">
                    <div class="summary-title">📏 Sales Range Summary</div>
                    <div class="summary-text">
                        <p>📊 <span class="summary-highlight">Total Range:</span> <b>${range_val:,.0f}</b></p>
                        <p>📈 <span class="summary-green">Minimum:</span> <b>${min_val:,.0f}</b> on {low_day}</p>
                        <p>📉 <span class="summary-pink">Maximum:</span> <b>${peak:,.0f}</b> on {peak_day}</p>
                        <p>📊 <span class="summary-orange">Volatility:</span> <b>{(range_val / avg * 100):.0f}%</b></p>
                        <p style='margin-top: 0.5rem; color: rgba(255,255,255,0.4); font-size: 0.85rem;'>
                            💡 <b>Business Insight:</b> Sales range from ${min_val:,.0f} to ${peak:,.0f}, 
                            a difference of ${range_val:,.0f} ({range_val / avg * 100:.0f}% volatility). 
                            This indicates significant variation. Plan staffing and inventory accordingly.
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# ============ MAIN CHART ============
st.markdown("""
    <div class="section-header">
        <div class="section-title">📈 <span>Sales Forecast</span> Trend</div>
        <div class="section-action">90-DAY VIEW</div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)

fig = go.Figure()

# Main line - Beautiful gradient
fig.add_trace(go.Scatter(
    x=df_filtered['Date'],
    y=df_filtered['Predicted_Sales'],
    mode='lines+markers',
    name='Forecast',
    line=dict(color='#818cf8', width=3, shape='spline'),
    marker=dict(
        size=5,
        color=df_filtered['Predicted_Sales'],
        colorscale='Viridis',
        showscale=False,
        line=dict(width=0)
    ),
    hovertemplate='<b>%{x|%b %d, %Y}</b><br>Sales: <b>$%{y:,.0f}</b><extra></extra>'
))

# Confidence bands
if show_confidence:
    upper = df_filtered['Predicted_Sales'] * 1.12
    lower = df_filtered['Predicted_Sales'] * 0.88
    
    fig.add_trace(go.Scatter(
        x=pd.concat([df_filtered['Date'], df_filtered['Date'][::-1]]),
        y=pd.concat([upper, lower[::-1]]),
        fill='toself',
        fillcolor='rgba(129, 140, 248, 0.08)',
        line=dict(color='rgba(129, 140, 248, 0)'),
        name='Confidence Band',
        hoverinfo='skip'
    ))

# Add a trend line
z = np.polyfit(range(len(df_filtered)), df_filtered['Predicted_Sales'], 1)
p = np.poly1d(z)
fig.add_trace(go.Scatter(
    x=df_filtered['Date'],
    y=p(range(len(df_filtered))),
    mode='lines',
    name='Trend',
    line=dict(color='rgba(52, 211, 153, 0.3)', width=1.5, dash='dash'),
    opacity=0.5,
    hoverinfo='skip'
))

fig.update_layout(
    height=400,
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    hovermode='x unified',
    margin=dict(l=10, r=10, t=10, b=10),
    font=dict(size=12),
    xaxis=dict(
        showgrid=False,
        tickfont=dict(color='rgba(255,255,255,0.15)', size=11),
        title=None
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='rgba(255,255,255,0.03)',
        tickfont=dict(color='rgba(255,255,255,0.15)', size=11),
        title=None,
        zeroline=False
    ),
    legend=dict(
        font=dict(color='rgba(255,255,255,0.2)', size=11),
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ============ TWO COLUMN CHARTS ============
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="section-header">
            <div class="section-title">📊 <span>Weekly</span> Performance</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    weekly = df_filtered.groupby('Week')['Predicted_Sales'].sum().reset_index()
    weekly['Week'] = weekly['Week'].astype(str)
    
    fig2 = px.bar(
        weekly,
        x='Week',
        y='Predicted_Sales',
        color='Predicted_Sales',
        color_continuous_scale=['#818cf8', '#a78bfa', '#c084fc'],
        labels={'Predicted_Sales': '', 'Week': ''},
        text=weekly['Predicted_Sales'].apply(lambda x: f'${x:,.0f}')
    )
    fig2.update_traces(
        textposition='outside',
        textfont=dict(color='rgba(255,255,255,0.3)', size=10),
        marker=dict(line=dict(width=0))
    )
    fig2.update_layout(
        height=340,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=5, r=5, t=5, b=5),
        font=dict(size=12),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color='rgba(255,255,255,0.15)', size=10)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.03)',
            tickfont=dict(color='rgba(255,255,255,0.15)', size=10),
            zeroline=False
        ),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="section-header">
            <div class="section-title">📊 <span>Day</span> Pattern</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_avg = df_filtered.groupby('Day_Name')['Predicted_Sales'].mean().reindex(dow_order)
    
    dow_values = dow_avg.values.tolist()
    dow_labels = dow_avg.index.tolist()
    
    colors = ['#818cf8', '#a78bfa', '#c084fc', '#f472b6', '#fbbf24', '#34d399', '#60a5fa']
    
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=dow_labels,
        y=dow_values,
        marker=dict(
            color=colors,
            line=dict(width=0)
        ),
        text=[f'${x:,.0f}' for x in dow_values],
        textposition='outside',
        textfont=dict(color='rgba(255,255,255,0.3)', size=10)
    ))
    fig3.update_layout(
        height=340,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=5, r=5, t=5, b=5),
        font=dict(size=12),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color='rgba(255,255,255,0.15)', size=10)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.03)',
            tickfont=dict(color='rgba(255,255,255,0.15)', size=10),
            zeroline=False
        ),
        showlegend=False
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============ DETAILED STATS ============
st.markdown("""
    <div class="section-header">
        <div class="section-title">📊 <span>Detailed</span> Analytics</div>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
    st.markdown('<div class="stat-header">📊 Day of Week Breakdown</div>', unsafe_allow_html=True)
    
    for day, val in dow_avg.items():
        pct = (val / dow_avg.max()) * 100 if dow_avg.max() > 0 else 0
        st.markdown(f"""
            <div class="stat-item">
                <span class="stat-label">{day}</span>
                <span style='color: #ffffff; font-weight: 600; font-size: 1rem;'>${val:,.0f}</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {pct}%; background: linear-gradient(90deg, #818cf8, #a78bfa);"></div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
    st.markdown('<div class="stat-header">📈 Monthly Performance</div>', unsafe_allow_html=True)
    
    monthly = df_filtered.groupby('Month')['Predicted_Sales'].sum().sort_values(ascending=False)
    
    for month, val in monthly.items():
        st.markdown(f"""
            <div class="stat-item">
                <span class="stat-label">{month}</span>
                <span class="stat-value stat-highlight">${val:,.0f}</span>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
    st.markdown('<div class="stat-header">🏆 Top Weeks</div>', unsafe_allow_html=True)
    
    weekly_top = df_filtered.groupby('Week')['Predicted_Sales'].sum().sort_values(ascending=False).head(5)
    
    for week, val in weekly_top.items():
        st.markdown(f"""
            <div class="stat-item">
                <span class="stat-label">Week {int(week)}</span>
                <span class="stat-value stat-green">${val:,.0f}</span>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============ DATA TABLE ============
st.markdown("""
    <div class="section-header">
        <div class="section-title">📋 <span>Forecast</span> Details</div>
    </div>
""", unsafe_allow_html=True)

search = st.text_input("", placeholder="🔍 Search by day, month, or date...", label_visibility="collapsed")

if search:
    table_df = df_filtered[
        df_filtered['Day_Name'].str.contains(search, case=False) |
        df_filtered['Month'].str.contains(search, case=False) |
        df_filtered['Date'].astype(str).str.contains(search)
    ]
else:
    table_df = df_filtered

st.dataframe(
    table_df[['Date', 'Day_Name', 'Predicted_Sales', 'Week', 'Month']]
    .style
    .format({
        'Predicted_Sales': '${:,.2f}',
        'Date': lambda x: x.strftime('%Y-%m-%d')
    })
    .background_gradient(subset=['Predicted_Sales'], cmap='Purples_r'),
    use_container_width=True,
    height=240
)

# ============ FOOTER ============
st.markdown("""
    <div class="footer">
        COPYRIGHT © 2026 FUTURE INTERNS · SALES & DEMAND FORECASTING
        <br>POWERED BY PYTHON · STREAMLIT · PLOTLY
    </div>
""", unsafe_allow_html=True)