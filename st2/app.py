import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration
st.set_page_config(
    layout="wide",
    page_title="Advanced Crypto Analysis Dashboard",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        max-width: 100%;
        padding: 1rem;
    }
    .metric-card {
        background: linear-gradient(145deg, #f3f4f6, #ffffff);
        border: 1px solid #e5e7eb;
        padding: 1rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    .price-up {
        background: linear-gradient(145deg, #dcffe4, #f0fff4);
        border-color: #9ae6b4;
    }
    .price-down {
        background: linear-gradient(145deg, #fed7d7, #fff5f5);
        border-color: #feb2b2;
    }
    .volume-card {
        background: linear-gradient(145deg, #e6f6ff, #f0f9ff);
        border-color: #90cdf4;
    }
    .market-cap-card {
        background: linear-gradient(145deg, #faf5ff, #f8f5ff);
        border-color: #d6bcfa;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f8fafc;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem 0.5rem 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_data():
    try:
        local_path = "cleaned_sorted_output_cleaned.csv"
        if os.path.exists(local_path):
            df = pd.read_csv(local_path)
        else:
            url = "https://raw.githubusercontent.com/143Himanshujangid/crryptocurrency/main/st2/cleaned_sorted_output_cleaned.csv"
            df = pd.read_csv(url)
        # Convert timestamp to datetime
        df['last_updated'] = pd.to_datetime(df['last_updated'])
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def create_advanced_chart(data, chart_type, x_col, y_cols, color_col=None):
    try:
        if len(data) == 0:
            return None
        
        layout = dict(
            template="plotly_white",
            height=500,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode='x unified'
        )
        
        if chart_type == "Multi-Line":
            fig = go.Figure()
            for y_col in y_cols:
                fig.add_trace(go.Scatter(
                    x=data[x_col],
                    y=data[y_col],
                    name=y_col,
                    mode='lines+markers'
                ))
        elif chart_type == "Area":
            fig = go.Figure()
            for y_col in y_cols:
                fig.add_trace(go.Scatter(
                    x=data[x_col],
                    y=data[y_col],
                    name=y_col,
                    fill='tonexty'
                ))
        elif chart_type == "Candlestick":
            fig = go.Figure(go.Candlestick(
                x=data[x_col],
                open=data[y_cols[0]],
                high=data[y_cols[1]],
                low=data[y_cols[2]],
                close=data[y_cols[3]]
            ))
        elif chart_type == "Bar":
            fig = px.bar(data, x=x_col, y=y_cols[0], color=color_col)
        elif chart_type == "Scatter Matrix":
            fig = px.scatter_matrix(data, dimensions=y_cols)
        elif chart_type == "3D Scatter":
            if len(y_cols) >= 3:
                fig = px.scatter_3d(data, x=y_cols[0], y=y_cols[1], z=y_cols[2])
        elif chart_type == "Bubble":
            if len(y_cols) >= 3:
                fig = px.scatter(data, x=y_cols[0], y=y_cols[1], size=y_cols[2],
                               hover_name=x_col)
        else:  # Default to line chart
            fig = px.line(data, x=x_col, y=y_cols[0])
            
        fig.update_layout(**layout)
        return fig
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return None

def display_enhanced_metrics(filtered_df):
    with st.container():
        cols = st.columns(4)
        current_price = filtered_df['price_usd'].iloc[-1]
        price_change = filtered_df['percent_change_24h'].iloc[-1]
        
        # Price Card
        with cols[0]:
            price_class = "price-up" if price_change >= 0 else "price-down"
            st.markdown(f"""
                <div class="metric-card {price_class}">
                    <h3 style="margin:0;">Current Price</h3>
                    <h2 style="margin:0;">${current_price:,.2f}</h2>
                    <p style="margin:0;color:{'green' if price_change >= 0 else 'red'}">
                        {price_change:+.2f}% (24h)
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        # Market Cap Card
        with cols[1]:
            market_cap = filtered_df['market_cap_usd'].iloc[-1]
            st.markdown(f"""
                <div class="metric-card market-cap-card">
                    <h3 style="margin:0;">Market Cap</h3>
                    <h2 style="margin:0;">${market_cap:,.0f}</h2>
                    <p style="margin:0;">Rank: {filtered_df['rank'].iloc[-1]}</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Volume Card
        with cols[2]:
            volume = filtered_df['24h_volume_usd'].iloc[-1]
            st.markdown(f"""
                <div class="metric-card volume-card">
                    <h3 style="margin:0;">24h Volume</h3>
                    <h2 style="margin:0;">${volume:,.0f}</h2>
                    <p style="margin:0;">Volume/Market Cap: {(volume/market_cap):,.2%}</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Supply Card
        with cols[3]:
            available_supply = filtered_df['available_supply'].iloc[-1]
            total_supply = filtered_df['total_supply'].iloc[-1]
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style="margin:0;">Supply Info</h3>
                    <h2 style="margin:0;">{available_supply:,.0f}</h2>
                    <p style="margin:0;">Total Supply: {total_supply:,.0f}</p>
                </div>
            """, unsafe_allow_html=True)

def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # Login section
    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.title("📊 Crypto Analysis Dashboard")
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")
                
                if submit:
                    if username == "admin" and password == "admin123":
                        st.session_state.authenticated = True
                        st.experimental_rerun()
                    else:
                        st.error("Invalid credentials!")
        return

    # Main dashboard
    st.title("🚀 Advanced Cryptocurrency Analysis Dashboard")
    
    # Load data
    df = load_data()
    if df is None:
        st.error("Failed to load data. Please try again later.")
        return

    # Sidebar controls
    with st.sidebar:
        st.title("Dashboard Controls")
        
        analysis_options = ["Currency Analysis", "Global Analysis", "Dynamic Analysis"]
        analysis_type = st.selectbox("Select Analysis Type", analysis_options)
        
        if analysis_type == "Currency Analysis":
            currency_options = df['symbol'].unique().tolist()
            selected_currency = st.selectbox(
                "Select Cryptocurrency",
                currency_options,
                index=0 if 'BTC' in currency_options else 0
            )
            filtered_df = df[df['symbol'] == selected_currency].copy()
        
        # Chart selection
        chart_types = [
            "Multi-Line", "Area", "Candlestick", "Bar", 
            "Scatter Matrix", "3D Scatter", "Bubble"
        ]
        selected_chart = st.selectbox("Select Chart Type", chart_types)

    # Main content area
    if analysis_type == "Currency Analysis":
        # Display enhanced metrics
        display_enhanced_metrics(filtered_df)
        
        # Analysis tabs
        tabs = st.tabs(["📈 Price Analysis", "📊 Market Analysis", "📱 Technical Indicators"])
        
        with tabs[0]:
            st.subheader("Price and Volume Analysis")
            x_col = st.selectbox("Select X-axis", df.columns)
            y_cols = st.multiselect(
                "Select Y-axis Metrics",
                df.select_dtypes(include=[np.number]).columns,
                default=['price_usd']
            )
            
            if y_cols:
                fig = create_advanced_chart(filtered_df, selected_chart, x_col, y_cols)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Global Analysis":
        st.subheader("Global Market Analysis")
        
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", min(df['last_updated']).date())
        with col2:
            end_date = st.date_input("End Date", max(df['last_updated']).date())
        
        # Filter data by date
        mask = (df['last_updated'].dt.date >= start_date) & (df['last_updated'].dt.date <= end_date)
        date_filtered_df = df[mask]
        
        # Metric selectors
        x_col = st.selectbox("Select X-axis Metric", df.columns)
        y_cols = st.multiselect(
            "Select Y-axis Metrics",
            df.select_dtypes(include=[np.number]).columns,
            default=['price_usd', 'market_cap_usd']
        )
        
        # Optional filters
        col1, col2 = st.columns(2)
        with col1:
            min_market_cap = st.number_input(
                "Minimum Market Cap (USD)",
                min_value=0,
                value=0
            )
        with col2:
            top_n = st.number_input(
                "Top N Cryptocurrencies",
                min_value=1,
                max_value=len(df['symbol'].unique()),
                value=10
            )
        
        # Apply filters
        filtered_df = date_filtered_df[date_filtered_df['market_cap_usd'] >= min_market_cap]
        top_symbols = filtered_df.groupby('symbol')['market_cap_usd'].mean().nlargest(top_n).index
        filtered_df = filtered_df[filtered_df['symbol'].isin(top_symbols)]
        
        if y_cols:
            fig = create_advanced_chart(filtered_df, selected_chart, x_col, y_cols, color_col='symbol')
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    else:  # Dynamic Analysis
        st.header("Dynamic Data Comparison")
        
        col1, col2 = st.columns(2)
        with col1:
            uploaded_file_1 = st.file_uploader("Upload First Dataset (CSV)", type=["csv"])
            if uploaded_file_1:
                df1 = pd.read_csv(uploaded_file_1)
                with st.expander("Preview Dataset 1"):
                    st.dataframe(df1.head())
                x_col = st.selectbox("Select X-axis (Dataset 1)", df1.columns)
                y_cols = st.multiselect(
                    "Select Y-axis Metrics (Dataset 1)",
                    df1.select_dtypes(include=[np.number]).columns
                )
                if y_cols:
                    fig = create_advanced_chart(df1, selected_chart, x_col, y_cols)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

        with col2:
            uploaded_file_2 = st.file_uploader("Upload Second Dataset (CSV)", type=["csv"])
            if uploaded_file_2:
                df2 = pd.read_csv(uploaded_file_2)
                with st.expander("Preview Dataset 2"):
                    st.dataframe(df2.head())
                x_col = st.selectbox("Select X-axis (Dataset 2)", df2.columns)
                y_cols = st.multiselect(
                    "Select Y-axis Metrics (Dataset 2)",
                    df2.select_dtypes(include=[np.number]).columns
                )
                if y_cols:
                    fig = create_advanced_chart(df2, selected_chart, x_col, y_cols)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
