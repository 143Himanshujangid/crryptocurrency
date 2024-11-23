import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

# Set page configuration
st.set_page_config(layout="wide", page_title="Responsive Data Analysis Dashboard")

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

# Chart creation
def create_chart(data, chart_type, columns, color_col=None):
    try:
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
    except Exception as e:
        st.error(f"Error creating chart: {e}")
        return None

# Main function
def main():
    # Session state initialization
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # Login section
    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align: center;'>Admin Login</h1>", unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.success("Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")
        return

    # Main dashboard after authentication
    st.title("Responsive Data Analysis Dashboard")
    
    # Load data
    df = load_data()

    # Sidebar
    st.sidebar.title("Dashboard Options")
    
    currency_options = df['symbol'].unique().tolist()
    selected_currency = st.sidebar.selectbox("Select Currency", currency_options)

    filtered_df = df[df['symbol'] == selected_currency]

    analysis_type = st.sidebar.radio("Select Analysis Type", ["Static", "Dynamic"])
    selected_chart = st.sidebar.selectbox("Select Chart Type", ["Bar", "Line", "Scatter", "Pie", "Box", "Histogram"])

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    # Display metrics
    with st.container():
        st.subheader(f"Analysis for {selected_currency}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Price (USD)", f"${filtered_df['price_usd'].iloc[0]:.2f}")
        col2.metric("Market Cap (USD)", f"${filtered_df['market_cap_usd'].iloc[0]:.2f}")
        col3.metric("24h Volume (USD)", f"${filtered_df['24h_volume_usd'].iloc[0]:.2f}")

    # Static Analysis
    if analysis_type == "Static":
        st.header("Static Analysis")
        x_col = st.selectbox("Select X-axis column", categorical_cols + numeric_cols)
        y_col = st.selectbox("Select Y-axis column", numeric_cols)
        color_col = st.selectbox("Select Color column (optional)", [None] + categorical_cols)

        if x_col and y_col:
            fig = create_chart(filtered_df, selected_chart, [x_col, y_col], color_col)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

    # Dynamic Analysis
    elif analysis_type == "Dynamic":
        st.header("Dynamic Analysis")
        uploaded_file = st.file_uploader("Upload a CSV File for Analysis", type=["csv"])
        if uploaded_file:
            try:
                user_df = pd.read_csv(uploaded_file)
                x_col = st.selectbox("Select X-axis column (Uploaded Data)", user_df.columns)
                y_col = st.selectbox("Select Y-axis column (Uploaded Data)", user_df.select_dtypes(include=[np.number]).columns)
                if x_col and y_col:
                    fig = create_chart(user_df, selected_chart, [x_col, y_col])
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading file: {e}")

if __name__ == "__main__":
    main()
