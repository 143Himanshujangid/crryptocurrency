import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    layout="wide",
    page_title="Advanced Crypto Analysis Dashboard",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for better responsiveness and modern styling
st.markdown("""
    <style>
    .stApp {
        max-width: 100%;
        padding: 1rem;
    }
    .streamlit-expanderHeader {
        font-size: 1.2rem;
        font-weight: 500;
    }
    /* Modern card styling */
    .crypto-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    /* Metric styling */
    .stMetric {
        background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 0.8rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    /* Chart container styling */
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 0.8rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
    }
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 4px;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2193b0;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_data(file_path=None):
    try:
        if file_path:
            return pd.read_csv(file_path)
        
        local_path = "cleaned_sorted_output_cleaned.csv"
        if os.path.exists(local_path):
            df = pd.read_csv(local_path)
        else:
            url = "https://raw.githubusercontent.com/143Himanshujangid/crryptocurrency/main/st2/cleaned_sorted_output_cleaned.csv"
            df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def create_advanced_chart(data, chart_type, x_col, y_col, color_col=None):
    try:
        if len(data) == 0:
            return None
        
        # Enhanced chart configuration
        layout = dict(
            template="plotly_white",
            height=500,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(255,255,255,0.9)',
            font=dict(family="Arial, sans-serif")
        )
        
        title = f"{chart_type} Analysis: {y_col} vs {x_col}"
        
        if chart_type == "Candlestick":
            fig = go.Figure(data=[go.Candlestick(
                x=data[x_col],
                open=data['open'] if 'open' in data.columns else data[y_col],
                high=data['high'] if 'high' in data.columns else data[y_col],
                low=data['low'] if 'low' in data.columns else data[y_col],
                close=data['close'] if 'close' in data.columns else data[y_col]
            )])
        elif chart_type == "Area":
            fig = px.area(data, x=x_col, y=y_col, color=color_col)
        elif chart_type == "Bubble":
            size_col = data.select_dtypes(include=[np.number]).columns[0]
            fig = px.scatter(data, x=x_col, y=y_col, size=size_col, color=color_col)
        elif chart_type == "Heat Map":
            pivot_table = pd.pivot_table(data, values=y_col, index=x_col, aggfunc='mean')
            fig = px.imshow(pivot_table, aspect='auto')
        else:
            # Default charts from previous implementation
            chart_funcs = {
                "Bar": px.bar,
                "Line": px.line,
                "Scatter": px.scatter,
                "Box": px.box,
                "Violin": px.violin,
                "Histogram": px.histogram
            }
            fig = chart_funcs[chart_type](data, x=x_col, y=y_col, color=color_col)
        
        fig.update_layout(title=title, **layout)
        return fig
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return None

def display_enhanced_metrics(df, currency):
    metrics_container = st.container()
    with metrics_container:
        cols = st.columns(4)
        metrics = [
            ("Current Price", "price_usd", "${:,.2f}"),
            ("Market Cap", "market_cap_usd", "${:,.0f}"),
            ("24h Volume", "24h_volume_usd", "${:,.0f}"),
            ("24h Change", "percent_change_24h", "{:,.2f}%")
        ]
        
        for i, (label, col_name, format_str) in enumerate(metrics):
            with cols[i]:
                try:
                    value = df[col_name].iloc[-1]
                    formatted_value = format_str.format(value)
                    delta = None
                    if "percent_change" in col_name:
                        delta = f"{value:+.2f}%"
                    st.metric(
                        label=label,
                        value=formatted_value,
                        delta=delta,
                        delta_color="normal" if not delta or float(delta.strip('%+')) > 0 else "inverse"
                    )
                except Exception as e:
                    st.error(f"Error displaying metric {label}: {str(e)}")

def main():
    st.title("🚀 Advanced Cryptocurrency Analysis Dashboard")
    
    # Sidebar configuration
    with st.sidebar:
        st.title("Analysis Controls")
        
        # Data source selection
        data_source = st.radio("Select Data Source", ["Default Dataset", "Local Dataset"])
        
        if data_source == "Local Dataset":
            uploaded_file = st.file_uploader("Upload Dataset (CSV)", type=["csv"])
            df = load_data(uploaded_file) if uploaded_file else None
        else:
            df = load_data()
        
        if df is not None:
            # Currency selection with search
            currency_options = df['symbol'].unique().tolist() if 'symbol' in df.columns else []
            if currency_options:
                selected_currency = st.selectbox(
                    "Select Cryptocurrency",
                    currency_options,
                    index=0 if 'BTC' in currency_options else 0
                )
            
            # Enhanced visualization options
            st.subheader("Visualization Settings")
            chart_types = [
                "Line", "Bar", "Scatter", "Area", "Candlestick", 
                "Heat Map", "Bubble", "Box", "Violin", "Histogram"
            ]
            selected_chart = st.selectbox("Chart Type", chart_types)
            
            # Dataset statistics
            st.subheader("Dataset Info")
            st.write(f"Total Records: {len(df):,}")
            st.write(f"Columns: {len(df.columns)}")
            if 'last_updated' in df.columns:
                st.write(f"Last Updated: {df['last_updated'].max()}")

    if df is not None:
        # Main content area
        tabs = st.tabs(["📊 Advanced Analysis", "📈 Time Series", "🔍 Custom Analysis"])
        
        with tabs[0]:
            if 'symbol' in df.columns:
                filtered_df = df[df['symbol'] == selected_currency].copy()
                display_enhanced_metrics(filtered_df, selected_currency)
            
            # Column selection for visualization
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox("Select X-axis", df.columns)
            with col2:
                y_col = st.selectbox("Select Y-axis", df.select_dtypes(include=[np.number]).columns)
            
            # Create and display chart
            fig = create_advanced_chart(df, selected_chart, x_col, y_col)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with tabs[1]:
            st.subheader("Time Series Analysis")
            if 'last_updated' in df.columns:
                time_fig = create_advanced_chart(
                    df, 
                    "Line", 
                    "last_updated",
                    st.selectbox("Select Metric", df.select_dtypes(include=[np.number]).columns)
                )
                if time_fig:
                    st.plotly_chart(time_fig, use_container_width=True)
        
        with tabs[2]:
            st.subheader("Custom Analysis")
            # Multi-chart analysis
            col1, col2 = st.columns(2)
            with col1:
                chart_type_1 = st.selectbox("First Chart Type", chart_types, key="chart1")
                x_col_1 = st.selectbox("X-axis (Chart 1)", df.columns, key="x1")
                y_col_1 = st.selectbox("Y-axis (Chart 1)", df.select_dtypes(include=[np.number]).columns, key="y1")
                fig1 = create_advanced_chart(df, chart_type_1, x_col_1, y_col_1)
                if fig1:
                    st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                chart_type_2 = st.selectbox("Second Chart Type", chart_types, key="chart2")
                x_col_2 = st.selectbox("X-axis (Chart 2)", df.columns, key="x2")
                y_col_2 = st.selectbox("Y-axis (Chart 2)", df.select_dtypes(include=[np.number]).columns, key="y2")
                fig2 = create_advanced_chart(df, chart_type_2, x_col_2, y_col_2)
                if fig2:
                    st.plotly_chart(fig2, use_container_width=True)

if __name__ == "__main__":
    main()
