import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Utility function to format numbers
def format_number(num):
    """Format large numbers into readable strings with B for billions and M for millions."""
    if num >= 1e9:
        return f"${num/1e9:.1f}B"
    elif num >= 1e6:
        return f"${num/1e6:.1f}M"
    return f"${num:.0f}"

# Function to generate sample data
def generate_expense_sample_data(quarters=6):
    """Generate sample expense forecast data for the specified number of quarters."""
    data = []
    baseline_expense = 4000000000 / 4  # $4B annual / 4 quarters
    for i in range(quarters):
        quarter_data = {
            "quarter": f"Q{i + 1} {pd.Timestamp.now().year}",
            "baseForecast": baseline_expense * (0.9 + np.random.random() * 0.2),
        }
        quarter_data["minForecast"] = quarter_data["baseForecast"] * (0.8 + np.random.random() * 0.1)
        quarter_data["maxForecast"] = quarter_data["baseForecast"] * (1.1 + np.random.random() * 0.1)
        data.append(quarter_data)
    return pd.DataFrame(data)

# Function to perform sensitivity analysis
def perform_expense_sensitivity_analysis():
    """Generate sensitivity analysis data for various expense parameters."""
    parameters = ['payrollCosts', 'COGS', 'operatingCost', 'overheadCost', 'inventoryValue', 'RDExpenses', 'marketingSalesExpenses']
    variations = [-20, -10, 0, 10, 20]
    
    results = {}
    for param in parameters:
        results[param] = []
        for variation in variations:
            # Generate a value between -50 and 50, with a tendency to be close to the variation percentage
            base_effect = variation * (0.5 + np.random.random())
            random_factor = (np.random.random() - 0.5) * 20  # Additional randomness
            effect = base_effect + random_factor
            effect = max(-50, min(50, effect))  # Limit to ±50% for realism
            results[param].append(effect)
    
    return pd.DataFrame(results, index=variations)

# Function to create the expense forecast chart
def create_expense_forecast_chart(data):
    """Create a line chart for expense forecasts using Plotly."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['quarter'], y=data['baseForecast'], mode='lines+markers', name='Base Forecast', line=dict(color='purple', width=2)))
    fig.add_trace(go.Scatter(x=data['quarter'], y=data['maxForecast'], mode='lines+markers', name='Max Forecast', line=dict(color='green', width=2)))
    fig.add_trace(go.Scatter(x=data['quarter'], y=data['minForecast'], mode='lines+markers', name='Min Forecast', line=dict(color='orange', width=2)))
    
    fig.update_layout(
        title='Quarterly Expense Forecast',
        xaxis_title='Quarter',
        yaxis_title='Expense',
        legend_title='Forecast Type',
        hovermode="x unified"
    )
    return fig

# Function to color sensitivity analysis cells
def color_sensitivity(val):
    """Color cells in the sensitivity analysis table based on their values."""
    if val > 0:
        return f'background-color: rgba(255, 0, 0, {min(abs(val) / 50, 1)})'
    else:
        return f'background-color: rgba(0, 255, 0, {min(abs(val) / 50, 1)})'

# Main function for the expense forecast dashboard
def expense_forecast_dashboard():
    st.title("Expense Forecast Dashboard")

    # Generate data
    data = generate_expense_sample_data()
    sensitivity_results = perform_expense_sensitivity_analysis()

    # Display expense forecast chart
    st.subheader("Quarterly Expense Forecast")
    chart = create_expense_forecast_chart(data)
    st.plotly_chart(chart, use_container_width=True)

    # Display sensitivity analysis
    st.subheader("Sensitivity Analysis")
    st.write("Impact on Total Expense Forecast (%)")
    styled_sensitivity = sensitivity_results.style.applymap(color_sensitivity).format("{:.2f}%")
    st.dataframe(styled_sensitivity)

    # Display expense data table
    st.subheader("Expense Data")
    st.dataframe(data.style.format({
        'baseForecast': format_number,
        'minForecast': format_number,
        'maxForecast': format_number
    }))

# This part would be removed when integrating into a multi-tab dashboard
if __name__ == "__main__":
    expense_forecast_dashboard()
