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

# Function to create charts based on selection
def create_chart(data, chart_type, columns, color_col=None):
    if chart_type == "Bar":
        fig = px.bar(data, x=columns[0], y=columns[1], color=color_col, title="Bar Chart Analysis")
    elif chart_type == "Line":
        fig = px.line(data, x=columns[0], y=columns[1], color=color_col, title="Line Chart Analysis")
    elif chart_type == "Scatter":
        fig = px.scatter(data, x=columns[0], y=columns[1], color=color_col, title="Scatter Plot Analysis")
    elif chart_type == "Pie":
        fig = px.pie(data, values=columns[1], names=columns[0], title="Pie Chart Analysis")
    elif chart_type == "Box":
        fig = px.box(data, x=columns[0], y=columns[1], color=color_col, title="Box Plot Analysis")
    else:  # Histogram
        fig = px.histogram(data, x=columns[1], color=color_col, title="Histogram Analysis")
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

    # Static Analysis
    if st.sidebar.button("Show Static Analysis"):
        st.header("Static Analysis")
        
        # Display all analysis options in a single layout
        st.subheader("Currency Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Price (USD)", f"${filtered_df['price_usd'].iloc[0]:.2f}")
        with col2:
            st.metric("Market Cap (USD)", f"${filtered_df['market_cap_usd'].iloc[0]:.2f}")
        with col3:
            st.metric("24h Volume (USD)", f"${filtered_df['24h_volume_usd'].iloc[0]:.2f}")

        st.subheader("Analysis Charts")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns

        x_cols = st.multiselect("Select X-axis columns", categorical_cols)
        y_cols = st.multiselect("Select Y-axis columns", numeric_cols)

        chart_types = ["Bar", "Line", "Scatter", "Pie", "Box", "Histogram"]
        selected_chart = st.selectbox("Select Chart Type", chart_types)

        for x_col, y_col in zip(x_cols, y_cols):
            fig = create_chart(df, selected_chart, [x_col, y_col])
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
