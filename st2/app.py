import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

# Set page configuration
st.set_page_config(layout="wide", page_title="Data Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    # Check if file exists locally
    local_path = "cleaned_sorted_output_cleaned.csv"
    if os.path.exists(local_path):
        df = pd.read_csv(local_path)
    else:
        # Use GitHub URL if not found locally
        url = "https://raw.githubusercontent.com/143Himanshujangid/crryptocurrency/main/st2/cleaned_sorted_output_cleaned.csv"
        df = pd.read_csv(url)
    return df

# Authentication
def authenticate(username, password):
    return username == "admin" and password == "admin123"

# Function to create charts based on selection
def create_chart(data, chart_type, columns, color_col=None):
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
