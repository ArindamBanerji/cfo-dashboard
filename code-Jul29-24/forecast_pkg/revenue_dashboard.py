import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

def format_number(num):
    """Format large numbers into readable strings with B for billions and M for millions."""
    if num >= 1e9:
        return f"${num/1e9:.1f}B"
    elif num >= 1e6:
        return f"${num/1e6:.1f}M"
    else:
        return f"${num:.0f}"

def generate_sample_data(quarters=6):
    """Generate sample financial data for the specified number of quarters."""
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

def perform_sensitivity_analysis(base_data):
    """Perform sensitivity analysis on the input parameters and their effect on revenue."""
    parameters = ['topChannelValue', 'monthlyRecurringRevenue', 'newPromotionRevenue', 
                  'customerAcquisitionCost', 'customerLifetimeValue', 'inventoryTurnover']
    variations = [-20, -10, 0, 10, 20]  # Percentage variations
    
    results = {}
    base_revenue = base_data['revenueForecast'].sum()
    
    for param in parameters:
        param_results = []
        for variation in variations:
            modified_data = base_data.copy()
            if param in ['topChannelValue', 'monthlyRecurringRevenue', 'newPromotionRevenue']:
                modified_data[param] *= (1 + variation / 100)
                modified_revenue = (modified_data['topChannelValue'] + 
                                    modified_data['monthlyRecurringRevenue'] * 3 + 
                                    modified_data['newPromotionRevenue']).sum()
            elif param == 'customerAcquisitionCost':
                impact = 1 - (variation / 100)  # Inverse relationship
                modified_data['newPromotionRevenue'] *= impact
                modified_revenue = (modified_data['topChannelValue'] + 
                                    modified_data['monthlyRecurringRevenue'] * 3 + 
                                    modified_data['newPromotionRevenue']).sum()
            elif param == 'customerLifetimeValue':
                impact = 1 + (variation / 100)
                modified_data['monthlyRecurringRevenue'] *= impact
                modified_revenue = (modified_data['topChannelValue'] + 
                                    modified_data['monthlyRecurringRevenue'] * 3 + 
                                    modified_data['newPromotionRevenue']).sum()
            elif param == 'inventoryTurnover':
                impact = 1 + (variation / 200)  # Reduced impact
                modified_data['topChannelValue'] *= impact
                modified_revenue = (modified_data['topChannelValue'] + 
                                    modified_data['monthlyRecurringRevenue'] * 3 + 
                                    modified_data['newPromotionRevenue']).sum()
            
            percent_change = (modified_revenue - base_revenue) / base_revenue * 100
            param_results.append(percent_change)
        results[param] = param_results
    
    return results

def create_forecast_chart(data, min_forecast, max_forecast):
    """Create a line chart for revenue forecasts including min and max forecast lines."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data['quarter'],
        y=data['revenueForecast'],
        mode='lines+markers',
        name='Revenue Forecast',
        line=dict(color='rgb(31, 119, 180)', width=4)
    ))

    fig.add_trace(go.Scatter(
        x=data['quarter'],
        y=min_forecast,
        mode='lines',
        name='Min Forecast',
        line=dict(color='rgba(255, 0, 0, 0.5)', dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=data['quarter'],
        y=max_forecast,
        mode='lines',
        name='Max Forecast',
        line=dict(color='rgba(0, 255, 0, 0.5)', dash='dash')
    ))

    fig.update_layout(
        title='Quarterly Revenue Forecast',
        xaxis_title='Quarter',
        yaxis_title='Revenue',
        legend_title='Forecast Type',
        hovermode="x unified"
    )
    return fig

def color_cells(val):
    """Function to color code cells in sensitivity analysis table."""
    if val > 0:
        color = f'background-color: rgba(0, 255, 0, {min(abs(val)/20, 1)})'
    elif val < 0:
        color = f'background-color: rgba(255, 0, 0, {min(abs(val)/20, 1)})'
    else:
        color = 'background-color: white'
    return color

def revenue_forecast_dashboard():
    """Main function to create the revenue forecast dashboard."""
    st.title("Revenue Forecast Dashboard")

    # Generate sample data
    data = generate_sample_data(6)  # Generate data for 6 quarters

    # Perform sensitivity analysis
    sensitivity_results = perform_sensitivity_analysis(data)

    # Calculate base, min, and max forecasts for each quarter
    base_forecast = data['revenueForecast'].sum()
    min_forecast = data['revenueForecast'] * 0.8  # Simplified min forecast
    max_forecast = data['revenueForecast'] * 1.2  # Simplified max forecast

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
    forecast_chart = create_forecast_chart(data, min_forecast, max_forecast)
    st.plotly_chart(forecast_chart, use_container_width=True)

    # Sensitivity Analysis with colors
    st.subheader("Sensitivity Analysis")
    st.write("Impact on Total Revenue Forecast (%)")

    sensitivity_table = pd.DataFrame(sensitivity_results, index=[-20, -10, 0, 10, 20])
    styled_table = sensitivity_table.style.applymap(color_cells).format("{:.2f}%")
    st.table(styled_table)

    # Forecast Summary
    st.subheader("Forecast Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Base Forecast", format_number(base_forecast))
    with col2:
        st.metric("Minimum Forecast", format_number(min_forecast.sum()))
    with col3:
        st.metric("Maximum Forecast", format_number(max_forecast.sum()))

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

# This part is commented out as it will be called from the main dashboard file
# if __name__ == "__main__":
#     revenue_forecast_dashboard()
