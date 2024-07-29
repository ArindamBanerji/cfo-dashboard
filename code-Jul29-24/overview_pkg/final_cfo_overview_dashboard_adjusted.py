import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def generate_sample_data():
    """
    Generate sample data for the CFO dashboard with more variation.
    
    Returns:
        tuple: A tuple containing quarterly data, latest quarter data, and previous quarter data.
    """
    quarters = ['Q2 2023', 'Q3 2023', 'Q4 2023', 'Q1 2024', 'Q2 2024', 'Q3 2024']
    
    base_income = 950000000
    base_expenses = 900000000
    
    data = []
    for i, quarter in enumerate(quarters):
        income_factor = np.random.uniform(0.9, 1.1)
        expense_factor = np.random.uniform(0.9, 1.1)
        
        income = base_income * income_factor * (1 + i * 0.02)  # Slight upward trend
        expenses = base_expenses * expense_factor * (1 + i * 0.015)  # Slightly slower upward trend
        
        data.append({
            'quarter': quarter,
            'bankBalance': np.random.uniform(50000000, 150000000),
            'creditCardBalance': np.random.uniform(5000000, 15000000),
            'bankCreditLineAvailable': np.random.uniform(25000000, 75000000),
            'inventory': np.random.uniform(100000000, 300000000),
            'expenses': expenses,
            'income': income,
            'payables': np.random.uniform(100000000, 250000000),
            'payableDays': np.random.uniform(30, 50),
            'receivables': np.random.uniform(150000000, 350000000),
            'receivableDays': np.random.uniform(35, 50),
            'returnOnEquity': np.random.uniform(0.1, 0.15),
            'returnOnAssets': np.random.uniform(0.05, 0.08),
            'salariesAndWages': np.random.uniform(20000000, 30000000),
            'payrollTaxes': np.random.uniform(5000000, 8000000),
            'employeeBenefits': np.random.uniform(8000000, 12000000),
            'accruedVacation': np.random.uniform(3000000, 5000000),
            'contributionsPayable': np.random.uniform(2000000, 4000000),
            'bonusesPayable': np.random.uniform(4000000, 7000000),
            'commissionsPayable': np.random.uniform(2000000, 4000000),
            'productSales': np.random.uniform(700000000, 800000000),
            'serviceRevenue': np.random.uniform(100000000, 150000000),
            'otherIncome': np.random.uniform(25000000, 50000000),
            'costOfGoodsSold': np.random.uniform(550000000, 600000000),
            'operatingExpenses': np.random.uniform(150000000, 200000000),
            'marketingExpenses': np.random.uniform(25000000, 50000000),
            'researchAndDevelopment': np.random.uniform(20000000, 30000000),
            'administrativeExpenses': np.random.uniform(50000000, 70000000),
        })
    
    df = pd.DataFrame(data)
    latest_quarter = df.iloc[-1]
    previous_quarter = df.iloc[-2]
    
    return df, latest_quarter, previous_quarter

def format_large_number(value):
    """
    Format large numbers into a more readable format.
    
    Args:
        value (float): The number to format.
    
    Returns:
        str: Formatted number string.
    """
    if value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif value >= 1e6:
        return f"${value/1e6:.2f}M"
    elif value >= 1e3:
        return f"${value/1e3:.2f}K"
    else:
        return f"${value:.2f}"

def create_metric_card(title, value, previous_value):
    """
    Create a metric card with current value and colored percentage change.
    
    Args:
        title (str): Title of the metric.
        value (float): Current value of the metric.
        previous_value (float): Previous value of the metric.
    """
    percent_change = (value - previous_value) / previous_value * 100
    is_increase = percent_change >= 0
    color = "green" if is_increase else "red"
    arrow = "▲" if is_increase else "▼"
    
    st.markdown(f"""
    <div style="border: 1px solid #ccc; border-radius: 5px; padding: 5px; margin-bottom: 10px; height: 100%;">
        <h4 style="margin: 0 0 5px 0; font-size: 0.9em;">{title}</h4>
        <p style="font-size: 1.2em; font-weight: bold; margin: 0;">{format_large_number(value)}</p>
        <p style="color: {color}; font-size: 0.9em; margin: 2px 0 0 0;">
            {arrow} {abs(percent_change):.2f}%
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_bar_chart(data, x, y, title, orientation='v', height=400):
    """
    Create a bar chart using Plotly.
    
    Args:
        data (pd.DataFrame): Data for the chart.
        x (str): Column name for x-axis.
        y (str or list): Column name(s) for y-axis.
        title (str): Title of the chart.
        orientation (str): Orientation of the bars ('v' for vertical, 'h' for horizontal).
        height (int): Height of the chart in pixels.
    
    Returns:
        go.Figure: Plotly figure object.
    """
    fig = px.bar(data, x=x, y=y, title=title, orientation=orientation, barmode='group', height=height)
    fig.update_traces(texttemplate='%{value:$.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    return fig

def create_line_chart(data, x, y, title):
    """
    Create a line chart using Plotly.
    
    Args:
        data (pd.DataFrame): Data for the chart.
        x (str): Column name for x-axis.
        y (list): List of column names for y-axis.
        title (str): Title of the chart.
    
    Returns:
        go.Figure: Plotly figure object.
    """
    fig = px.line(data, x=x, y=y, title=title)
    fig.update_traces(texttemplate='%{y:$.2s}', textposition='top center')
    return fig

def create_area_chart(data, x, y, title):
    """
    Create an area chart using Plotly.
    
    Args:
        data (pd.DataFrame): Data for the chart.
        x (str): Column name for x-axis.
        y (list): List of column names for y-axis.
        title (str): Title of the chart.
    
    Returns:
        go.Figure: Plotly figure object.
    """
    fig = px.area(data, x=x, y=y, title=title)
    return fig

def cfo_financial_overview():
    """
    Main function to create the CFO Financial Overview dashboard.
    This function serves as an entry point for the dashboard tab.
    """
    st.title("CFO Financial Overview Dashboard")

    # Generate sample data
    df, latest_quarter, previous_quarter = generate_sample_data()

    # Display metric cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        create_metric_card("Bank Balance", latest_quarter['bankBalance'], previous_quarter['bankBalance'])
    with col2:
        create_metric_card("Credit Card Balance", latest_quarter['creditCardBalance'], previous_quarter['creditCardBalance'])
    with col3:
        create_metric_card("Bank Credit Line", latest_quarter['bankCreditLineAvailable'], previous_quarter['bankCreditLineAvailable'])
    with col4:
        create_metric_card("Inventory", latest_quarter['inventory'], previous_quarter['inventory'])

    # Expenses vs Income
    st.plotly_chart(create_bar_chart(df, 'quarter', ['expenses', 'income'], "Expenses vs Income"))

    # Payables and Receivables
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['quarter'], y=df['payables'], name='Payables', yaxis='y1'))
    fig.add_trace(go.Scatter(x=df['quarter'], y=df['receivables'], name='Receivables', yaxis='y1'))
    fig.add_trace(go.Scatter(x=df['quarter'], y=df['payableDays'], name='Days to Pay', yaxis='y2'))
    fig.add_trace(go.Scatter(x=df['quarter'], y=df['receivableDays'], name='Days Turnover', yaxis='y2'))
    fig.update_layout(
        title='Payables and Receivables',
        yaxis=dict(title='Amount', side='left', showgrid=False),
        yaxis2=dict(title='Days', side='right', overlaying='y', showgrid=False)
    )
    st.plotly_chart(fig)

    # Payroll Liabilities
    payroll_columns = ['salariesAndWages', 'payrollTaxes', 'employeeBenefits', 'accruedVacation', 'contributionsPayable', 'bonusesPayable', 'commissionsPayable']
    st.plotly_chart(create_area_chart(df, 'quarter', payroll_columns, "Payroll Liabilities"))

    # Payroll Liabilities (Last Quarter)
    last_quarter_payroll = latest_quarter[payroll_columns].reset_index()
    last_quarter_payroll.columns = ['Category', 'Value']
    st.plotly_chart(create_bar_chart(last_quarter_payroll, 'Value', 'Category', "Payroll Liabilities (Last Quarter)", orientation='h'))

    # Income Components and Expense Components side by side
    col1, col2 = st.columns(2)

    with col1:
        # Income Components (Last Quarter)
        income_components = pd.DataFrame({
            'Category': ['Product Sales', 'Service Revenue', 'Other Income'],
            'Value': [latest_quarter['productSales'], latest_quarter['serviceRevenue'], latest_quarter['otherIncome']]
        })
        st.plotly_chart(create_bar_chart(income_components, 'Value', 'Category', "Income Components (Last Quarter)", orientation='h', height=300), use_container_width=True)

    with col2:
        # Expense Components (Last Quarter)
        expense_components = pd.DataFrame({
            'Category': ['Cost of Goods Sold', 'Operating Expenses', 'Marketing Expenses', 'Research & Development', 'Administrative Expenses'],
            'Value': [latest_quarter['costOfGoodsSold'], latest_quarter['operatingExpenses'], latest_quarter['marketingExpenses'], 
                      latest_quarter['researchAndDevelopment'], latest_quarter['administrativeExpenses']]
        })
        st.plotly_chart(create_bar_chart(expense_components, 'Value', 'Category', "Expense Components (Last Quarter)", orientation='h', height=300), use_container_width=True)

    # Return on Equity and Assets
    st.plotly_chart(create_line_chart(df, 'quarter', ['returnOnEquity', 'returnOnAssets'], "Return on Equity and Assets"))

if __name__ == "__main__":
    cfo_financial_overview()
