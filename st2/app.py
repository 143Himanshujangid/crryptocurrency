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
    elif chart_type == "Top cryptocurrencies by market capitalization":
        fig = px.bar(data, x='symbol', y='market_cap_usd', title='Top Cryptocurrencies by Market Capitalization')
    elif chart_type == "Top cryptocurrencies by 24-hour trading volume":
        fig = px.bar(data, x='symbol', y='24h_volume_usd', title='Top Cryptocurrencies by 24-Hour Trading Volume')
    elif chart_type == "Cryptocurrencies with the highest percentage change in 24 hours":
        fig = px.bar(data, x='symbol', y='percent_change_24h', title='Cryptocurrencies with the Highest Percentage Change in 24 Hours')
    elif chart_type == "Cryptocurrencies with the highest percentage change in the last hour":
        fig = px.bar(data, x='symbol', y='percent_change_1h', title='Cryptocurrencies with the Highest Percentage Change in the Last Hour')
    elif chart_type == "Cryptocurrencies with the highest percentage change in 7 days":
        fig = px.bar(data, x='symbol', y='percent_change_7d', title='Cryptocurrencies with the Highest Percentage Change in 7 Days')
    elif chart_type == "Correlation heatmap of numeric fields":
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        correlation_matrix = data[numeric_cols].corr()
        fig = px.imshow(correlation_matrix, title="Correlation Heatmap of Numeric Fields")
    elif chart_type == "Distribution of price_usd":
        fig = px.histogram(data, x='price_usd', title="Distribution of Price (USD)")
    elif chart_type == "Distribution of market_cap_usd":
        fig = px.histogram(data, x='market_cap_usd', title="Distribution of Market Cap (USD)")
    elif chart_type == "Average price of cryptocurrencies by symbol":
        avg_price_by_symbol = data.groupby('symbol')['price_usd'].mean().reset_index()
        fig = px.bar(avg_price_by_symbol, x='symbol', y='price_usd', title="Average Price of Cryptocurrencies by Symbol")
    elif chart_type == "Total market cap for each symbol":
        total_market_cap_by_symbol = data.groupby('symbol')['market_cap_usd'].sum().reset_index()
        fig = px.bar(total_market_cap_by_symbol, x='symbol', y='market_cap_usd', title="Total Market Cap for Each Symbol")
    elif chart_type == "Cryptocurrencies with the smallest circulating supply":
        data_sorted = data.sort_values('circulating_supply')
        fig = px.bar(data_sorted.head(10), x='symbol', y='circulating_supply', title="Cryptocurrencies with the Smallest Circulating Supply")
    elif chart_type == "Cryptocurrencies with the largest max supply":
        data_sorted = data.sort_values('max_supply', ascending=False)
        fig = px.bar(data_sorted.head(10), x='symbol', y='max_supply', title="Cryptocurrencies with the Largest Max Supply")
    elif chart_type == "Cryptocurrencies ranked by rank and their prices":
        fig = px.bar(data, x='rank', y='price_usd', title="Cryptocurrencies Ranked by Rank and Their Prices")
    elif chart_type == "Cryptocurrencies with a high volume-to-market-cap ratio":
        data['volume_to_market_cap_ratio'] = data['24h_volume_usd'] / data['market_cap_usd']
        data_sorted = data.sort_values('volume_to_market_cap_ratio', ascending=False)
        fig = px.bar(data_sorted.head(10), x='symbol', y='volume_to_market_cap_ratio', title="Cryptocurrencies with a High Volume-to-Market-Cap Ratio")
    elif chart_type == "Top 10 cryptocurrencies by price_btc":
        data_sorted = data.sort_values('price_btc', ascending=False)
        fig = px.bar(data_sorted.head(10), x='symbol', y='price_btc', title="Top 10 Cryptocurrencies by Price (BTC)")
    elif chart_type == "Relationship between price_usd and market_cap_usd":
        fig = px.scatter(data, x='price_usd', y='market_cap_usd', title="Relationship between Price (USD) and Market Cap (USD)")
    elif chart_type == "Relationship between percent_change_1h and percent_change_24h":
        fig = px.scatter(data, x='percent_change_1h', y='percent_change_24h', title="Relationship between Percent Change (1h) and Percent Change (24h)")
    elif chart_type == "Cryptocurrencies grouped by symbol and their average percent_change_7d":
        avg_percent_change_by_symbol = data.groupby('symbol')['percent_change_7d'].mean().reset_index()
        fig = px.bar(avg_percent_change_by_symbol, x='symbol', y='percent_change_7d', title="Cryptocurrencies Grouped by Symbol and Their Average Percent Change (7d)")
    elif chart_type == "Distribution of top 10 cryptocurrencies' 24h_volume_usd":
        top_10 = data.sort_values('market_cap_usd', ascending=False).head(10)
        fig = px.histogram(top_10, x='24h_volume_usd', title="Distribution of Top 10 Cryptocurrencies' 24h Volume (USD)")
    elif chart_type == "Comparison of price_usd and price_btc":
        fig = px.scatter(data, x='price_usd', y='price_btc', title="Comparison of Price (USD) and Price (BTC)")
    else:  # Histogram
        fig = px.histogram(data, x=columns[1], color=color_col, title="Histogram Analysis")
    return fig

# Custom CSS for borders and styling
def add_custom_css():
    st.markdown(
        """
        <style>
        /* Admin Login Page Styling */
        .login-page {
            border: 2px solid red;
            border-radius: 15px;
            padding: 30px;
            background-color: #f9f9f9;
            box-shadow: 2px 2px 12px rgba(255, 0, 0, 0.4);
        }

        /* Styling Sidebar Items */
        .stSelectbox, .stRadio, .stMetric {
            border: 1px solid red;
            border-radius: 10px;
            padding: 5px;
        }

        /* Heading Customization */
        .highlight {
            color: red;
            font-weight: bold;
        }

        /* Cards with consistent border-radius */
        .stMetric {
            margin: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Main function
def main():
    # Add custom styles
    add_custom_css()

    # Session state initialization
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # Login section
    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 2, 1]) 
        with col2:
            st.markdown('<div class="login-page">', unsafe_allow_html=True)
            st.markdown(
                """
                <h1>Admin <span class="highlight">Login</span></h1>
                """,
                unsafe_allow_html=True,
            )
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials")
            st.markdown('</div>', unsafe_allow_html=True)
        return

    # Main dashboard after authentication
    st.markdown(
        """
        <h1>📊Data <span class="highlight">Analysis</span> Dashboard</h1>
        """,
        unsafe_allow_html=True,
    )

    # Load data
    df = load_data()

    # Sidebar configuration
    currency_options = df['symbol'].unique().tolist()
    selected_currency = st.sidebar.selectbox("Select Currency", currency_options)

    # Sidebar Analysis Type
    analysis_type = st.sidebar.radio("Select Analysis Type", ["Static", "Dynamic"])

    # Sidebar Chart Type
    chart_types_sidebar = ["Bar", "Line", "Scatter", "Pie", "Box", "Histogram"]
    selected_chart = st.sidebar.selectbox("Select Chart Type", chart_types_sidebar)

    # Filter data based on selected currency
    filtered_df = df[df['symbol'] == selected_currency]

    # Static Analysis
    if analysis_type == "Static":
        st.header("Static Analysis")

        # Display all static analysis options
        st.subheader("Currency Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Price (USD)", f"${filtered_df['price_usd'].iloc[0]:.2f}")
        with col2:
            st.metric("Market Cap (USD)", f"${filtered_df['market_cap_usd'].iloc[0]:.2f}")
        with col3:
            st.metric("24h Volume (USD)", f"${filtered_df['24h_volume_usd'].iloc[0]:.2f}")

        st.subheader("Static Charts")

        # Add the dropdown here, only if "Static" is selected
        chart_types = [
            "Top cryptocurrencies by market capitalization",
            "Top cryptocurrencies by 24-hour trading volume",
            "Cryptocurrencies with the highest percentage change in 24 hours",
            "Cryptocurrencies with the highest percentage change in the last hour",
            "Cryptocurrencies with the highest percentage change in 7 days",
            "Correlation heatmap of numeric fields",
            "Distribution of price_usd",
            "Distribution of market_cap_usd",
            "Average price of cryptocurrencies by symbol",
            "Total market cap for each symbol",
            "Cryptocurrencies with the smallest circulating supply",
            "Cryptocurrencies with the largest max supply",
            "Cryptocurrencies ranked by rank and their prices",
            "Cryptocurrencies with a high volume-to-market-cap ratio",
            "Top 10 cryptocurrencies by price_btc",
            "Relationship between price_usd and market_cap_usd",
            "Relationship between percent_change_1h and percent_change_24h",
            "Cryptocurrencies grouped by symbol and their average percent_change_7d",
            "Distribution of top 10 cryptocurrencies' 24h_volume_usd",
            "Comparison of price_usd and price_btc"
        ]
        question_dropdown = st.selectbox("Select a question:", chart_types)

        # Call create_chart based on the selected question
        if question_dropdown:
            fig = create_chart(df, question_dropdown, [], color_col=None)
            st.plotly_chart(fig, use_container_width=True)


        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns

        x_cols = st.multiselect("Select X-axis columns", categorical_cols)
        y_cols = st.multiselect("Select Y-axis columns", numeric_cols)

        if x_cols and y_cols:
            for x_col, y_col in zip(x_cols, y_cols):
                fig = create_chart(df, selected_chart, [x_col, y_col])
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Please select at least one X and Y column for chart generation.")

    # Dynamic Analysis
    elif analysis_type == "Dynamic":
        col1, col2 = st.columns(2)
        with col1:
            st.header("Dynamic Analysis - File 1")
            uploaded_file_1 = st.file_uploader("Upload CSV File 1", type=["csv"])
            if uploaded_file_1:
                df1 = pd.read_csv(uploaded_file_1)
                x_col1 = st.selectbox("Select X-axis column (File 1)", df1.columns, key="file1_x")
                y_col1 = st.selectbox("Select Y-axis column (File 1)", df1.select_dtypes(include=[np.number]).columns, key="file1_y")
                fig1 = create_chart(df1, selected_chart, [x_col1, y_col1])
                st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.header("Dynamic Analysis - File 2")
            uploaded_file_2 = st.file_uploader("Upload CSV File 2", type=["csv"])
            if uploaded_file_2:
                df2 = pd.read_csv(uploaded_file_2)
                x_col2 = st.selectbox("Select X-axis column (File 2)", df2.columns, key="file2_x")
                y_col2 = st.selectbox("Select Y-axis column (File 2)", df2.select_dtypes(include=[np.number]).columns, key="file2_y")
                fig2 = create_chart(df2, selected_chart, [x_col2, y_col2])
                st.plotly_chart(fig2, use_container_width=True)

if __name__ == "__main__":
    main()
