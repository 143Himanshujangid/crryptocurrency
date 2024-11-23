import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

# Custom CSS for dark theme and responsiveness
st.markdown("""
    <style>
    /* Dark theme for main container */
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Dark sidebar */
    .css-1d391kg {
        background-color: #1a1c23;
        padding: 1rem 1rem 1rem;
    }
    
    /* Sidebar text */
    .css-1d391kg {
        color: #ffffff;
    }
    
    /* Card containers */
    div.element-container {
        background-color: #1a1c23;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #2d3035;
    }
    
    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: #2d3035;
        border-radius: 8px;
        padding: 15px;
        margin: 5px;
        color: #ffffff;
        border: 1px solid #404348;
    }
    
    /* Metric text colors */
    div[data-testid="metric-container"] label {
        color: #c2c7d0;
    }
    
    div[data-testid="metric-container"] div {
        color: #ffffff;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Text inputs */
    .stTextInput>div>div>input {
        background-color: #2d3035;
        color: #ffffff;
        border: 1px solid #404348;
    }
    
    /* Selectbox */
    .stSelectbox>div>div {
        background-color: #2d3035;
        color: #ffffff;
    }
    
    /* Multiselect */
    .stMultiSelect>div {
        background-color: #2d3035;
        color: #ffffff;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #4a4f57;
        color: #ffffff;
        border: 1px solid #5c616a;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #5c616a;
        border-color: #696e78;
    }
    
    /* File uploader */
    .stUploadButton {
        background-color: #2d3035;
        color: #ffffff;
        border: 1px solid #404348;
        border-radius: 5px;
    }
    
    /* Plotly chart background */
    .js-plotly-plot .plotly .main-svg {
        background-color: #1a1c23 !important;
    }
    
    /* Error messages */
    .stAlert {
        background-color: #462c32;
        color: #ff4b4b;
        border: 1px solid #ff4b4b;
    }
    
    /* Better spacing for mobile */
    @media (max-width: 768px) {
        .row-widget {
            margin: 10px 0;
        }
        .stMetric {
            margin: 5px 0;
        }
    }
    
    /* Chart container */
    .stPlotlyChart {
        background-color: #1a1c23;
        border-radius: 10px;
        padding: 10px;
        margin: 15px 0;
        border: 1px solid #2d3035;
    }
    
    /* Links */
    a {
        color: #4a9eff !important;
    }
    
    /* Dropdown options */
    option {
        background-color: #2d3035;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Set page configuration with dark theme
st.set_page_config(layout="wide", page_title="Data Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    local_path = "cleaned_sorted_output_cleaned.csv"
    if os.path.exists(local_path):
        df = pd.read_csv(local_path)
    else:
        url = "https://raw.githubusercontent.com/143Himanshujangid/crryptocurrency/main/st2/cleaned_sorted_output_cleaned.csv"
        df = pd.read_csv(url)
    return df

# Authentication
def authenticate(username, password):
    return username == "admin" and password == "admin123"

# Function to create charts based on selection with dark theme
def create_chart(data, chart_type, columns, color_col=None):
    # Define dark theme colors
    dark_template = dict(
        layout=dict(
            paper_bgcolor='#1a1c23',
            plot_bgcolor='#1a1c23',
            font=dict(color='#ffffff'),
            title=dict(color='#ffffff'),
            xaxis=dict(
                gridcolor='#2d3035',
                linecolor='#2d3035',
                tickcolor='#ffffff',
                tickfont=dict(color='#ffffff'),
                title=dict(color='#ffffff')
            ),
            yaxis=dict(
                gridcolor='#2d3035',
                linecolor='#2d3035',
                tickcolor='#ffffff',
                tickfont=dict(color='#ffffff'),
                title=dict(color='#ffffff')
            )
        )
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
    else:  # Histogram
        fig = px.histogram(data, x=columns[1], color=color_col,
                           title="Histogram Analysis")
    
    # Apply dark theme to chart
    fig.update_layout(
        dark_template['layout'],
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=20),
        height=450,
        showlegend=True,
        legend=dict(
            font=dict(color='#ffffff'),
            bgcolor='#1a1c23',
            bordercolor='#2d3035'
        )
    )
    
    return fig

# Main function
def main():
    # Session state initialization
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # Login section
    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 2, 1]) 
        with col2:
            st.title("Admin Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Login"):
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials")
        return

    # Main dashboard after authentication
    st.title("Data Analysis Dashboard")
    
    # Load data
    df = load_data()

    # Currency selection dropdown
    currency_options = df['symbol'].unique().tolist()
    selected_currency = st.sidebar.selectbox("Select Currency", currency_options)

    # Filter data based on selected currency
    filtered_df = df[df['symbol'] == selected_currency]

    # Display dataset info
    st.sidebar.subheader("Dataset Information")
    st.sidebar.write(f"Total Records: {len(df)}")
    st.sidebar.write(f"Total Columns: {len(df.columns)}")
    
    # Analysis type selection
    analysis_type = st.sidebar.selectbox("Select Analysis Type", ["Static", "Dynamic"])
    
    # Analysis questions
    questions = [
        "Distribution Analysis",
        "Category Comparison",
        "Value Ranges Analysis",
        "Correlation Analysis",
        "Frequency Analysis",
        "Top/Bottom Analysis",
        "Aggregation Analysis",
        "Percentage Distribution",
        "Statistical Summary",
        "Variance Analysis",
        "Pattern Recognition",
        "Outlier Detection",
        "Group Comparison",
        "Composition Analysis",
        "Range Distribution",
        "Value Counts",
        "Measure of Central Tendency",
        "Dispersion Analysis",
        "Category Distribution",
        "Numerical Distribution"
    ]
    selected_question = st.sidebar.selectbox("Select Analysis Question", questions)
    
    # Chart type selection
    chart_types = ["Bar", "Line", "Scatter", "Pie", "Box", "Histogram"]
    selected_chart = st.sidebar.selectbox("Select Chart Type", chart_types)

    # Common column selections
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    if analysis_type == "Static":
        col1, _ = st.columns(2)
        with col1:
            st.header("Static Analysis")

            # Display cards with currency information
            st.subheader("Currency Information")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Price (USD)", f"${filtered_df['price_usd'].iloc[0]:.2f}")
            with col2:
                st.metric("Market Cap (USD)", f"${filtered_df['market_cap_usd'].iloc[0]:.2f}")
            with col3:
                st.metric("24h Volume (USD)", f"${filtered_df['24h_volume_usd'].iloc[0]:.2f}")

            # Column selection for multiple charts
            x_cols = st.multiselect("Select X-axis columns", df.columns)
            y_cols = st.multiselect("Select Y-axis columns", numeric_cols)

            for x_col, y_col in zip(x_cols, y_cols):
                fig = create_chart(df, selected_chart, [x_col, y_col])
                st.plotly_chart(fig, use_container_width=True)

    else:  # Dynamic Analysis
        col3, col4 = st.columns(2)

        with col3:
            st.header("Dynamic Analysis - File 1")
            uploaded_file_1 = st.file_uploader("Upload CSV File 1", type=["csv"])
            if uploaded_file_1 is not None:
                df1 = pd.read_csv(uploaded_file_1)
                x_col1 = st.selectbox("Select X-axis column (File 1)", df1.columns)
                y_col1 = st.selectbox("Select Y-axis column (File 1)", df1.select_dtypes(include=[np.number]).columns)
                fig1 = create_chart(df1, selected_chart, [x_col1, y_col1])
                st.plotly_chart(fig1, use_container_width=True)

        with col4:
            st.header("Dynamic Analysis - File 2")
            uploaded_file_2 = st.file_uploader("Upload CSV File 2", type=["csv"])
            if uploaded_file_2 is not None:
                df2 = pd.read_csv(uploaded_file_2)
                x_col2 = st.selectbox("Select X-axis column (File 2)", df2.columns)
                y_col2 = st.selectbox("Select Y-axis column (File 2)", df2.select_dtypes(include=[np.number]).columns)
                fig2 = create_chart(df2, selected_chart, [x_col2, y_col2])
                st.plotly_chart(fig2, use_container_width=True)

if __name__ == "__main__":
    main()
