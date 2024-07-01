import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(page_title="CFO Dashboard - Forecast", layout="wide")

# Data Generation Function
def generate_forecast_data(years=2, periods_per_year=12):
    np.random.seed(42)  # For reproducibility
    total_periods = years * periods_per_year
    
    base_revenue = 4_000_000_000 / periods_per_year  # $4B annual revenue
    base_profit_margin = 0.02
    
    date_range = pd.date_range(start='2024-01-01', periods=total_periods, freq='M')
    
    data = []
    for i in range(total_periods):
        revenue = base_revenue * (1 + 0.1 * i / total_periods) + np.random.normal(0, base_revenue * 0.05)
        expenses = revenue * (1 - base_profit_margin) + np.random.normal(0, base_revenue * 0.02)
        profit = revenue - expenses
        
        operating_cash_flow = profit + np.random.normal(0, base_revenue * 0.01)
        investing_cash_flow = -np.abs(np.random.normal(base_revenue * 0.05, base_revenue * 0.02))
        financing_cash_flow = np.random.normal(0, base_revenue * 0.03)
        net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow
        
        if i == 0:
            assets = 5_000_000_000 + net_cash_flow
        else:
            assets = data[-1]['assets'] + net_cash_flow
        assets += np.random.normal(0, 100_000_000)
        
        liabilities = assets * 0.4 + np.random.normal(0, 100_000_000)
        equity = assets - liabilities
        
        data.append({
            'date': date_range[i],
            'revenue': revenue,
            'expenses': expenses,
            'profit': profit,
            'operating_cash_flow': operating_cash_flow,
            'investing_cash_flow': investing_cash_flow,
            'financing_cash_flow': financing_cash_flow,
            'net_cash_flow': net_cash_flow,
            'assets': assets,
            'liabilities': liabilities,
            'equity': equity
        })
    
    return pd.DataFrame(data)

# Sensitivity Analysis Function
def perform_sensitivity_analysis(data, column, variations=[-0.1, -0.05, 0, 0.05, 0.1]):
    sensitivity_data = []
    for var in variations:
        adjusted_data = data[column] * (1 + var)
        sensitivity_data.append({
            'variation': f"{var*100}%",
            'value': adjusted_data.sum()
        })
    return pd.DataFrame(sensitivity_data)

# Generate forecast data
@st.cache_data
def get_forecast_data():
    return generate_forecast_data()

forecast_data = get_forecast_data()

# Perform sensitivity analysis
revenue_sensitivity = perform_sensitivity_analysis(forecast_data, 'revenue')
expense_sensitivity = perform_sensitivity_analysis(forecast_data, 'expenses')
cash_flow_sensitivity = perform_sensitivity_analysis(forecast_data, 'net_cash_flow')
asset_sensitivity = perform_sensitivity_analysis(forecast_data, 'assets')

# Plotting functions
def create_forecast_chart(data, y_column, title, color):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['date'], y=data[y_column], mode='lines', name=y_column.replace('_', ' ').title(), line=dict(color=color)))
    fig.update_layout(title=title, xaxis_title="Date", yaxis_title="Amount ($)", height=300)
    return fig

def create_sensitivity_chart(data, title, color):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data['variation'], y=data['value'], name='Sensitivity', marker_color=color))
    fig.update_layout(title=title, xaxis_title="Variation", yaxis_title="Amount ($)", height=300)
    return fig

# Dashboard
st.title("CFO Dashboard - Forecast")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(create_forecast_chart(forecast_data, 'revenue', "Revenue Forecast", "#8884d8"), use_container_width=True)
with col2:
    st.plotly_chart(create_sensitivity_chart(revenue_sensitivity, "Revenue Sensitivity", "#8884d8"), use_container_width=True)

with col1:
    st.plotly_chart(create_forecast_chart(forecast_data, 'expenses', "Expense Forecast", "#82ca9d"), use_container_width=True)
with col2:
    st.plotly_chart(create_sensitivity_chart(expense_sensitivity, "Expense Sensitivity", "#82ca9d"), use_container_width=True)

with col1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=forecast_data['date'], y=forecast_data['operating_cash_flow'], mode='lines', name='Operating Cash Flow', line=dict(color="#8884d8")))
    fig.add_trace(go.Scatter(x=forecast_data['date'], y=forecast_data['investing_cash_flow'], mode='lines', name='Investing Cash Flow', line=dict(color="#82ca9d")))
    fig.add_trace(go.Scatter(x=forecast_data['date'], y=forecast_data['financing_cash_flow'], mode='lines', name='Financing Cash Flow', line=dict(color="#ffc658")))
    fig.add_trace(go.Scatter(x=forecast_data['date'], y=forecast_data['net_cash_flow'], mode='lines', name='Net Cash Flow', line=dict(color="#ff7300")))
    fig.update_layout(title="Cash Flow Forecast", xaxis_title="Date", yaxis_title="Amount ($)", height=300)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.plotly_chart(create_sensitivity_chart(cash_flow_sensitivity, "Net Cash Flow Sensitivity", "#ff7300"), use_container_width=True)

with col1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=forecast_data['date'], y=forecast_data['assets'], mode='lines', name='Assets', line=dict(color="#8884d8")))
    fig.add_trace(go.Scatter(x=forecast_data['date'], y=forecast_data['liabilities'], mode='lines', name='Liabilities', line=dict(color="#82ca9d")))
    fig.add_trace(go.Scatter(x=forecast_data['date'], y=forecast_data['equity'], mode='lines', name='Equity', line=dict(color="#ffc658")))
    fig.update_layout(title="Balance Sheet Forecast", xaxis_title="Date", yaxis_title="Amount ($)", height=300)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.plotly_chart(create_sensitivity_chart(asset_sensitivity, "Asset Sensitivity", "#8884d8"), use_container_width=True)

# Display raw data
st.subheader("Raw Forecast Data")
st.dataframe(forecast_data)
