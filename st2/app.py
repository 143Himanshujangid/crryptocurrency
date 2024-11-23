import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Set page configuration with improved layout
st.set_page_config(
    layout="wide",
    page_title="Crypto Data Analysis Dashboard",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Custom CSS for better responsiveness and styling
st.markdown("""
    <style>
    .stApp {
        max-width: 100%;
        padding: 1rem;
    }
    .streamlit-expanderHeader {
        font-size: 1.2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .stProgress .st-bo {
        background-color: #00a0dc;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)  # Cache data for 1 hour
def load_data():
    try:
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

def authenticate(username, password):
    return username == "admin" and password == "admin123"

def create_chart(data, chart_type, columns, color_col=None):
    try:
        if len(data) == 0:
            return None
        
        # Common chart configuration
        layout = dict(
            template="plotly_white",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        if chart_type == "Bar":
            fig = px.bar(data, x=columns[0], y=columns[1], color=color_col,
                        title="Bar Chart Analysis")
        elif chart_type == "Line":
            fig = px.line(data, x=columns[0], y=columns[1], color=color_col,
                         title="Line Chart Analysis")
        elif chart_type == "Scatter":
            fig = px.scatter(data, x=columns[0], y=columns[1], color=color_col,
                           title="Scatter Plot Analysis")
        elif chart_type == "Pie":
            fig = px.pie(data, values=columns[1], names=columns[0],
                        title="Pie Chart Analysis")
        elif chart_type == "Box":
            fig = px.box(data, x=columns[0], y=columns[1], color=color_col,
                        title="Box Plot Analysis")
        elif chart_type == "Histogram":
            fig = px.histogram(data, x=columns[1], color=color_col,
                             title="Histogram Analysis")
        
        fig.update_layout(**layout)
        return fig
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return None

def display_currency_metrics(filtered_df):
    with st.container():
        cols = st.columns(4)
        metrics = [
            ("Price (USD)", "price_usd", "${:,.2f}"),
            ("Market Cap (USD)", "market_cap_usd", "${:,.0f}"),
            ("24h Volume (USD)", "24h_volume_usd", "${:,.0f}"),
            ("% Change (24h)", "percent_change_24h", "{:,.2f}%")
        ]
        
        for i, (label, col_name, format_str) in enumerate(metrics):
            with cols[i]:
                try:
                    value = filtered_df[col_name].iloc[0]
                    formatted_value = format_str.format(value)
                    delta_color = "normal"
                    if "percent_change" in col_name:
                        delta_color = "inverse" if value < 0 else "normal"
                    st.metric(
                        label=label,
                        value=formatted_value,
                        delta=f"{value:+.2f}%" if "percent_change" in col_name else None,
                        delta_color=delta_color
                    )
                except Exception as e:
                    st.error(f"Error displaying metric {label}: {str(e)}")

def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # Login section with improved styling
    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.title("📊 Crypto Analysis Dashboard")
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")
                
                if submit:
                    if authenticate(username, password):
                        st.session_state.authenticated = True
                        st.experimental_rerun()
                    else:
                        st.error("Invalid credentials! Please try again.")
        return

    # Main dashboard after authentication
    st.title("🚀 Cryptocurrency Analysis Dashboard")
    
    # Load data with error handling
    df = load_data()
    if df is None:
        st.error("Failed to load data. Please try again later.")
        return

    # Sidebar configuration
    with st.sidebar:
        st.title("Dashboard Controls")
        
        # Currency selection with search
        currency_options = df['symbol'].unique().tolist()
        selected_currency = st.selectbox(
            "Select Cryptocurrency",
            currency_options,
            index=0 if 'BTC' in currency_options else 0
        )
        
        # Analysis controls
        with st.expander("Analysis Settings", expanded=True):
            analysis_type = st.radio("Analysis Type", ["Static", "Dynamic"])
            
            chart_types = ["Bar", "Line", "Scatter", "Pie", "Box", "Histogram"]
            selected_chart = st.selectbox("Chart Type", chart_types)
            
            # Dataset info
            st.subheader("Dataset Statistics")
            st.write(f"Total Cryptocurrencies: {len(currency_options)}")
            st.write(f"Total Records: {len(df):,}")
            st.write(f"Last Updated: {df['last_updated'].max()}")

    # Filter data
    filtered_df = df[df['symbol'] == selected_currency].copy()

    # Main content area
    if analysis_type == "Static":
        # Display metrics
        display_currency_metrics(filtered_df)
        
        # Analysis tabs
        tab1, tab2 = st.tabs(["📈 Price Analysis", "📊 Market Analysis"])
        
        with tab1:
            st.subheader("Price Trends")
            col1, col2 = st.columns(2)
            
            with col1:
                # Price over time
                fig_price = create_chart(
                    filtered_df,
                    "Line",
                    ["last_updated", "price_usd"]
                )
                if fig_price:
                    st.plotly_chart(fig_price, use_container_width=True)
            
            with col2:
                # Volume analysis
                fig_volume = create_chart(
                    filtered_df,
                    "Bar",
                    ["last_updated", "24h_volume_usd"]
                )
                if fig_volume:
                    st.plotly_chart(fig_volume, use_container_width=True)
        
        with tab2:
            st.subheader("Market Overview")
            # Custom column selection
            cols = st.columns(2)
            with cols[0]:
                x_col = st.selectbox("Select X-axis", df.columns)
            with cols[1]:
                y_col = st.selectbox("Select Y-axis", df.select_dtypes(include=[np.number]).columns)
            
            fig_custom = create_chart(filtered_df, selected_chart, [x_col, y_col])
            if fig_custom:
                st.plotly_chart(fig_custom, use_container_width=True)

    else:  # Dynamic Analysis
        st.header("Dynamic Data Comparison")
        
        col1, col2 = st.columns(2)
        with col1:
            uploaded_file_1 = st.file_uploader("Upload First Dataset (CSV)", type=["csv"])
            if uploaded_file_1:
                df1 = pd.read_csv(uploaded_file_1)
                with st.expander("Preview Dataset 1"):
                    st.dataframe(df1.head(), use_container_width=True)
                x_col1 = st.selectbox("X-axis (Dataset 1)", df1.columns)
                y_col1 = st.selectbox("Y-axis (Dataset 1)", df1.select_dtypes(include=[np.number]).columns)
                fig1 = create_chart(df1, selected_chart, [x_col1, y_col1])
                if fig1:
                    st.plotly_chart(fig1, use_container_width=True)

        with col2:
            uploaded_file_2 = st.file_uploader("Upload Second Dataset (CSV)", type=["csv"])
            if uploaded_file_2:
                df2 = pd.read_csv(uploaded_file_2)
                with st.expander("Preview Dataset 2"):
                    st.dataframe(df2.head(), use_container_width=True)
                x_col2 = st.selectbox("X-axis (Dataset 2)", df2.columns)
                y_col2 = st.selectbox("Y-axis (Dataset 2)", df2.select_dtypes(include=[np.number]).columns)
                fig2 = create_chart(df2, selected_chart, [x_col2, y_col2])
                if fig2:
                    st.plotly_chart(fig2, use_container_width=True)

if __name__ == "__main__":
    main()
