import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Set page config for a wide layout
st.set_page_config(page_title="Revenue Forecast Dashboard", layout="wide")

# Utility function to format numbers
def format_number(num):
    """
    Format large numbers into readable strings with B for billions and M for millions.
    """
    if num >= 1e9:
        return f"${num/1e9:.1f}B"
    elif num >= 1e6:
        return f"${num/1e6:.1f}M"
    else:
        return f"${num:.0f}"

# Function to generate sample data
def generate_sample_data(quarters=5):
    """
    Generate sample financial data for the specified number of quarters.
    """
    data = []
    base_date = datetime.now()
    for i in range(quarters):
        quarter_date = base_date + timedelta(days=90*i)
        quarter_data = {
            'quarter': f"Q{((quarter_date.month-1)//3)+1} {quarter_date.year}",
            'topChannelValue': np.random.uniform(800000000, 1000000000),
            'monthlyRecurringRevenue': np.random.uniform(200000000, 300000000),
            'newPromotionRevenue': np.random.uniform(50000000, 100000000),
            'customerAcquisitionCost': np.random.uniform(1000, 2000),
            'customerLifetimeValue': np.random.uniform(10000, 20000),
            'inventoryTurnover': np.random.uniform(4, 6)
        }
        quarter_data['revenueForecast'] = (
            quarter_data['topChannelValue'] +
            quarter_data['monthlyRecurringRevenue'] * 3 +
            quarter_data['newPromotionRevenue']
        )
        data.append(quarter_data)
    return pd.DataFrame(data)

# Function to perform sensitivity analysis
def sensitivity_analysis(base_data):
    """
    Perform sensitivity analysis on the input parameters and their effect on revenue.
    """
    parameters = ['topChannelValue', 'monthlyRecurringRevenue', 'newPromotionRevenue', 
                  'customerAcquisitionCost', 'customerLifetimeValue', 'inventoryTurnover']
    variations = [-20, -10, 0, 10, 20]  # Percentage variations
    
    results = []
    for param in parameters:
        for variation in variations:
            modified_data = base_data.copy()
            modified_data[param] *= (1 + variation / 100)
            total_revenue = (modified_data['topChannelValue'] + 
                             modified_data['monthlyRecurringRevenue'] * 3 + 
                             modified_data['newPromotionRevenue']).sum()
            results.append({
                'parameter': param,
                'variation': variation,
                'revenue': total_revenue
            })
    
    return pd.DataFrame(results)

# Generate sample data
data = generate_sample_data(5)  # Generate 5 quarters of data

# Perform sensitivity analysis
sensitivity_results = sensitivity_analysis(data)

# Calculate base forecast
base_forecast = data['revenueForecast'].sum()

# Dashboard title
st.title("Revenue Forecast Dashboard")

# Input Parameters section
st.subheader("Input Parameters")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Top Channel Value", format_number(data['topChannelValue'].iloc[0]))
    st.metric("Monthly Recurring Revenue", format_number(data['monthlyRecurringRevenue'].iloc[0]))
with col2:
    st.metric("New Promotion Revenue", format_number(data['newPromotionRevenue'].iloc[0]))
    st.metric("Customer Acquisition Cost", format_number(data['customerAcquisitionCost'].iloc[0]))
with col3:
    st.metric("Customer Lifetime Value", format_number(data['customerLifetimeValue'].iloc[0]))
    st.metric("Inventory Turnover", f"{data['inventoryTurnover'].iloc[0]:.2f}")

# Quarterly Revenue Forecast chart
st.subheader("Quarterly Revenue Forecast")
fig = px.bar(data, x='quarter', y='revenueForecast', 
             labels={'revenueForecast': 'Revenue Forecast'},
             title='Quarterly Revenue Forecast')
fig.update_layout(
    yaxis_title='Revenue',
    bargap=0.4  # Adjust this value to change the width of the bars (0.4 means 40% gap)
)
fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
st.plotly_chart(fig, use_container_width=True)

# Sensitivity Analysis
st.subheader("Sensitivity Analysis")

# Prepare data for sensitivity analysis table
sensitivity_table = sensitivity_results.pivot(index='parameter', columns='variation', values='revenue')
sensitivity_table = (sensitivity_table - base_forecast) / base_forecast * 100  # Convert to percentage change

# Create sensitivity analysis table
st.write("Impact on Revenue Forecast (%)")
sensitivity_styled = sensitivity_table.style.format("{:.2f}%").background_gradient(cmap="RdYlGn", axis=None)
st.write(sensitivity_styled)

# Forecast Summary
st.subheader("Forecast Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Base Forecast", format_number(base_forecast))
with col2:
    st.metric("Minimum Forecast", format_number(sensitivity_results['revenue'].min()))
with col3:
    st.metric("Maximum Forecast", format_number(sensitivity_results['revenue'].max()))

# Forecast Data
st.subheader("Forecast Data")
st.dataframe(data)

# Add a download button for the full dataset
csv = data.to_csv(index=False)
st.download_button(
    label="Download full dataset as CSV",
    data=csv,
    file_name="revenue_forecast_data.csv",
    mime="text/csv",
)
