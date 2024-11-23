import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
from datetime import datetime
import plotly.graph_objects as go

# Set page configuration with improved styling
st.set_page_config(
    layout="wide",
    page_title="Crypto Analysis Dashboard",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .big-font {
        font-size:24px !important;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    .metric-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .chart-container {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Improved data loading with progress bar
@st.cache_data
def load_data():
    with st.spinner('Loading data...'):
        local_path = "cleaned_sorted_output_cleaned.csv"
        if os.path.exists(local_path):
            df = pd.read_csv(local_path)
        else:
            url = "https://raw.githubusercontent.com/143Himanshujangid/crryptocurrency/main/st2/cleaned_sorted_output_cleaned.csv"
            df = pd.read_csv(url)
        return df

# Enhanced authentication with session management
def authenticate(username, password):
    valid_credentials = {
        "admin": "admin123",
        "user": "user123"
    }
    return username in valid_credentials and valid_credentials[username] == password

# Improved chart creation with better styling and responsiveness
def create_chart(data, chart_type, columns, color_col=None):
    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode='closest'
    )
    
    if chart_type == "Bar":
        fig = px.bar(data, x=columns[0], y=columns[1], color=color_col,
                     title=f"{columns[1]} vs {columns[0]}")
    elif chart_type == "Line":
        fig = px.line(data, x=columns[0], y=columns[1], color=color_col,
                      title=f"Trend of {columns[1]} over {columns[0]}")
    elif chart_type == "Scatter":
        fig = px.scatter(data, x=columns[0], y=columns[1], color=color_col,
                         title=f"Relationship between {columns[1]} and {columns[0]}")
    elif chart_type == "Pie":
        fig = px.pie(data, values=columns[1], names=columns[0],
                     title=f"Distribution of {columns[1]}")
    elif chart_type == "Box":
        fig = px.box(data, x=columns[0], y=columns[1], color=color_col,
                     title=f"Distribution of {columns[1]} by {columns[0]}")
    else:  # Histogram
        fig = px.histogram(data, x=columns[1], color=color_col,
                           title=f"Distribution of {columns[1]}")
    
    fig.update_layout(layout)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    return fig

# Function to display metric cards
def display_metric_card(label, value, delta=None):
    st.markdown(f"""
        <div class="metric-card">
            <h3>{label}</h3>
            <h2>{value}</h2>
            {f"<p style='color: {'green' if delta > 0 else 'red'}'>{delta:+.2f}%</p>" if delta is not None else ""}
        </div>
    """, unsafe_allow_html=True)

def main():
    # Session state initialization
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.login_attempts = 0

    # Enhanced login interface
    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align: center;'>🔐 Crypto Analysis Dashboard</h1>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
                <div style='background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                    <h2 style='text-align: center;'>Login</h2>
                </div>
            """, unsafe_allow_html=True)
            
            username = st.text_input("👤 Username")
            password = st.text_input("🔑 Password", type="password")
            
            if st.button("Login", key="login_button"):
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.experimental_rerun()
                else:
                    st.session_state.login_attempts += 1
                    remaining_attempts = 3 - st.session_state.login_attempts
                    if remaining_attempts > 0:
                        st.error(f"Invalid credentials. {remaining_attempts} attempts remaining.")
                    else:
                        st.error("Too many failed attempts. Please try again later.")
                        st.session_state.login_attempts = 0
        return

    # Main dashboard after authentication
    st.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h1 style='text-align: center;'>Crypto Analysis Dashboard</h1>
            <p style='text-align: center;'>Welcome, {st.session_state.username}!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_data()

    # Sidebar configuration
    with st.sidebar:
        st.markdown("### Dashboard Controls")
        currency_options = df['symbol'].unique().tolist()
        selected_currency = st.selectbox("📈 Select Currency", currency_options)
        
        st.markdown("### Analysis Settings")
        analysis_type = st.radio("📊 Analysis Type", ["Static", "Dynamic"])
        
        with st.expander("📈 Dataset Information"):
            st.write(f"Total Records: {len(df):,}")
            st.write(f"Total Columns: {len(df.columns)}")
            st.write(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Filter data
    filtered_df = df[df['symbol'] == selected_currency]

    # Main content area
    if analysis_type == "Static":
        # Metrics Row
        st.markdown("### Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            display_metric_card(
                "Price (USD)", 
                f"${filtered_df['price_usd'].iloc[0]:,.2f}",
                filtered_df['percent_change_24h'].iloc[0]
            )
        with col2:
            display_metric_card(
                "Market Cap (USD)", 
                f"${filtered_df['market_cap_usd'].iloc[0]:,.0f}"
            )
        with col3:
            display_metric_card(
                "24h Volume (USD)", 
                f"${filtered_df['24h_volume_usd'].iloc[0]:,.0f}"
            )
        with col4:
            display_metric_card(
                "Available Supply", 
                f"{filtered_df['available_supply'].iloc[0]:,.0f}"
            )

        # Chart section
        st.markdown("### Analysis Charts")
        col1, col2 = st.columns(2)
        
        with col1:
            with st.container():
                st.markdown("#### Price Analysis")
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                x_col = st.selectbox("Select X-axis", df.columns, key='x1')
                y_col = st.selectbox("Select Y-axis", numeric_cols, key='y1')
                chart_type = st.selectbox("Select Chart Type", 
                    ["Bar", "Line", "Scatter", "Box", "Histogram"], key='chart1')
                fig1 = create_chart(filtered_df, chart_type, [x_col, y_col])
                st.plotly_chart(fig1, use_container_width=True)

        with col2:
            with st.container():
                st.markdown("#### Market Analysis")
                x_col2 = st.selectbox("Select X-axis", df.columns, key='x2')
                y_col2 = st.selectbox("Select Y-axis", numeric_cols, key='y2')
                chart_type2 = st.selectbox("Select Chart Type", 
                    ["Bar", "Line", "Scatter", "Box", "Histogram"], key='chart2')
                fig2 = create_chart(filtered_df, chart_type2, [x_col2, y_col2])
                st.plotly_chart(fig2, use_container_width=True)

    else:  # Dynamic Analysis
        st.markdown("### Dynamic Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### File 1 Analysis")
            uploaded_file_1 = st.file_uploader("Upload CSV File 1", type=["csv"])
            if uploaded_file_1:
                df1 = pd.read_csv(uploaded_file_1)
                x_col1 = st.selectbox("Select X-axis column", df1.columns)
                y_col1 = st.selectbox("Select Y-axis column", 
                    df1.select_dtypes(include=[np.number]).columns)
                chart_type1 = st.selectbox("Select Chart Type", 
                    ["Bar", "Line", "Scatter", "Box", "Histogram"], key='chart3')
                fig1 = create_chart(df1, chart_type1, [x_col1, y_col1])
                st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.markdown("#### File 2 Analysis")
            uploaded_file_2 = st.file_uploader("Upload CSV File 2", type=["csv"])
            if uploaded_file_2:
                df2 = pd.read_csv(uploaded_file_2)
                x_col2 = st.selectbox("Select X-axis column", df2.columns, key='x4')
                y_col2 = st.selectbox("Select Y-axis column", 
                    df2.select_dtypes(include=[np.number]).columns, key='y4')
                chart_type2 = st.selectbox("Select Chart Type", 
                    ["Bar", "Line", "Scatter", "Box", "Histogram"], key='chart4')
                fig2 = create_chart(df2, chart_type2, [x_col2, y_col2])
                st.plotly_chart(fig2, use_container_width=True)

    # Footer
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: center;'>
            <p>© 2024 Crypto Analysis Dashboard. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
