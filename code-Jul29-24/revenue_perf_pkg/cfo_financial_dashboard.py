import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def generate_quarterly_data():
    """
    Generate sample quarterly data for financial metrics.
    
    Returns:
        pd.DataFrame: DataFrame containing quarterly financial data.
    """
    quarters = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025']
    data = []
    for quarter in quarters:
        data.append({
            'quarter': quarter,
            'ebitdaGrowth': np.random.uniform(-1, 5),
            'ebitdaMargin': np.random.uniform(3, 4),
            'grossMargin': np.random.uniform(18, 20),
            'netIncomeMargin': np.random.uniform(1, 1.5),
            'productSalesMargin': np.random.uniform(1.2, 1.4),
            'volumeDiscounts': np.random.uniform(0.16, 0.24),
            'inventoryManagement': np.random.uniform(0.1, 0.16),
            'valueAddedServices': np.random.uniform(0.1, 0.14),
            'privateLabel': np.random.uniform(0.08, 0.12),
            'otherContributions': np.random.uniform(0.2, 0.3)
        })
    return pd.DataFrame(data)

def generate_monthly_data():
    """
    Generate sample monthly data for recurring revenue.
    
    Returns:
        pd.DataFrame: DataFrame containing monthly recurring revenue data.
    """
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    data = []
    for month in months:
        data.append({
            'month': month,
            'mrr': np.random.uniform(9000000, 10000000),
            'ongoingMaintenance': np.random.uniform(27.5, 32.5),
            'autoPartSubscriptions': np.random.uniform(22.5, 27.5),
            'inventoryManagement': np.random.uniform(12.5, 17.5),
            'vehicleTracking': np.random.uniform(7.5, 12.5),
            'onlineTraining': np.random.uniform(6.5, 9.5),
            'digitalMarketing': np.random.uniform(5.5, 8.5),
            'mobileAppSubscriptions': np.random.uniform(4, 6)
        })
    return pd.DataFrame(data)

def generate_arr():
    """
    Generate a sample Annual Recurring Revenue (ARR) value.
    
    Returns:
        float: Sample ARR value.
    """
    return np.random.uniform(180000000, 200000000)

def create_financial_metrics_chart(data):
    """
    Create a line chart for financial metrics over time.
    
    Args:
        data (pd.DataFrame): DataFrame containing quarterly financial data.
    
    Returns:
        go.Figure: Plotly figure object for the financial metrics chart.
    """
    fig = go.Figure()
    metrics = ['ebitdaGrowth', 'ebitdaMargin', 'grossMargin', 'netIncomeMargin']
    colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300']
    
    for metric, color in zip(metrics, colors):
        fig.add_trace(go.Scatter(x=data['quarter'], y=data[metric], mode='lines+markers', name=metric, line=dict(color=color)))
    
    fig.update_layout(
        title='Financial Metrics Over Time',
        xaxis_title='Quarter',
        yaxis_title='Percentage',
        yaxis_tickformat=',.1%',
        legend_title='Metrics',
        hovermode='x unified'
    )
    return fig

def create_margin_contributions_chart(data):
    """
    Create a stacked area chart for margin contributions over time.
    
    Args:
        data (pd.DataFrame): DataFrame containing quarterly financial data.
    
    Returns:
        go.Figure: Plotly figure object for the margin contributions chart.
    """
    fig = go.Figure()
    contributions = ['productSalesMargin', 'volumeDiscounts', 'inventoryManagement', 'valueAddedServices', 'privateLabel', 'otherContributions']
    colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#a4de6c', '#d0ed57']
    
    for contribution, color in zip(contributions, colors):
        fig.add_trace(go.Scatter(
            x=data['quarter'], y=data[contribution], mode='none', stackgroup='one', fillcolor=color, name=contribution
        ))
    
    fig.update_layout(
        title='Margin Contributions Over Time',
        xaxis_title='Quarter',
        yaxis_title='Percentage',
        yaxis_tickformat=',.1%',
        legend_title='Contributions',
        hovermode='x unified'
    )
    return fig

def create_mrr_chart(data):
    """
    Create a line chart for Monthly Recurring Revenue (MRR).
    
    Args:
        data (pd.DataFrame): DataFrame containing monthly recurring revenue data.
    
    Returns:
        go.Figure: Plotly figure object for the MRR chart.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['month'], y=data['mrr'], mode='lines+markers', name='MRR'))
    
    fig.update_layout(
        title='Monthly Recurring Revenue',
        xaxis_title='Month',
        yaxis_title='Revenue',
        yaxis_tickformat='$,.0f',
        hovermode='x unified'
    )
    return fig

def create_arr_contributions_chart():
    """
    Create a pie chart for Annual Recurring Revenue (ARR) contributions.
    
    Returns:
        go.Figure: Plotly figure object for the ARR contributions chart.
    """
    arr_contributions = [
        {'name': 'Long-term service contracts', 'value': 40},
        {'name': 'Auto part subscription services', 'value': 25},
        {'name': 'Fleet management solutions', 'value': 15},
        {'name': 'Diagnostic tool subscriptions', 'value': 10},
        {'name': 'Training and certification programs', 'value': 5},
        {'name': 'Extended warranty plans', 'value': 3},
        {'name': 'Software licenses', 'value': 2}
    ]
    
    fig = px.pie(arr_contributions, values='value', names='name', title='ARR Contributions')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_mrr_contributions_chart(data):
    """
    Create a stacked area chart for Monthly Recurring Revenue (MRR) contributions.
    
    Args:
        data (pd.DataFrame): DataFrame containing monthly recurring revenue data.
    
    Returns:
        go.Figure: Plotly figure object for the MRR contributions chart.
    """
    fig = go.Figure()
    contributions = ['ongoingMaintenance', 'autoPartSubscriptions', 'inventoryManagement', 'vehicleTracking', 'onlineTraining', 'digitalMarketing', 'mobileAppSubscriptions']
    colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#a4de6c', '#d0ed57', '#ffc0cb']
    
    for contribution, color in zip(contributions, colors):
        fig.add_trace(go.Scatter(
            x=data['month'], y=data[contribution], mode='none', stackgroup='one', fillcolor=color, name=contribution
        ))
    
    fig.update_layout(
        title='MRR Contributions Over Time',
        xaxis_title='Month',
        yaxis_title='Percentage',
        yaxis_tickformat=',.1%',
        legend_title='Contributions',
        hovermode='x unified'
    )
    return fig

def margins_recurring_revenues():
    """
    Main function to create the Margins and Recurring Revenues dashboard.
    This function serves as an entry point for the dashboard tab.
    """
    st.title("CFO Margins & Recurring Revenues")

    # Generate sample data
    quarterly_data = generate_quarterly_data()
    monthly_data = generate_monthly_data()
    arr = generate_arr()

    # Display ARR card
    st.metric("Annual Recurring Revenue", f"${arr/1e6:.2f}M")

    # Create and display financial metrics chart
    st.plotly_chart(create_financial_metrics_chart(quarterly_data), use_container_width=True)

    # Create and display margin contributions chart
    st.plotly_chart(create_margin_contributions_chart(quarterly_data), use_container_width=True)

    # Create and display MRR chart
    st.plotly_chart(create_mrr_chart(monthly_data), use_container_width=True)

    # Create and display ARR contributions and MRR contributions charts side by side
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_arr_contributions_chart(), use_container_width=True)
    with col2:
        st.plotly_chart(create_mrr_contributions_chart(monthly_data), use_container_width=True)

if __name__ == "__main__":
    margins_recurring_revenues()
