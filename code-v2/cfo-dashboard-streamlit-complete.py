import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="CFO Dashboard - Overview", layout="wide")

# Data Generation Function
@st.cache_data
def generate_data(days=365):
    np.random.seed(42)  # For reproducibility
    date_range = pd.date_range(end=datetime.now(), periods=days)
    
    data = {
        'Date': date_range,
        'Bank_Balance': np.random.uniform(50000000, 100000000, days),
        'Credit_Card_Balance': np.random.uniform(1000000, 5000000, days),
        'Credit_Line_Available': np.random.uniform(20000000, 50000000, days),
        'Expenses': np.random.uniform(9800000, 10200000, days),
        'Income': np.random.uniform(10800000, 11200000, days),
        'Inventory': np.random.uniform(200000000, 400000000, days),
        'Payables': np.random.uniform(100000000, 200000000, days),
        'Receivables': np.random.uniform(150000000, 300000000, days),
        'Payroll_Liabilities': np.random.uniform(20000000, 40000000, days),
        'Days_to_Pay': np.random.randint(30, 60, days),
        'Days_Turnover': np.random.randint(45, 75, days),
        'Return_on_Equity': np.random.uniform(0.05, 0.15, days),
        'Return_on_Assets': np.random.uniform(0.03, 0.10, days),
    }
    
    return pd.DataFrame(data)

# Load or generate data
data = generate_data()

# Title
st.title("CFO Dashboard - Overview")

# Date range selector
col1, col2 = st.columns(2)
start_date = col1.date_input("Start Date", data['Date'].min())
end_date = col2.date_input("End Date", data['Date'].max())

# Filter data based on date range
mask = (data['Date'] >= pd.to_datetime(start_date)) & (data['Date'] <= pd.to_datetime(end_date))
filtered_data = data.loc[mask]

# Key Metrics
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Bank Balance", f"${filtered_data['Bank_Balance'].iloc[-1]:,.0f}")
col2.metric("Credit Card Balance", f"${filtered_data['Credit_Card_Balance'].iloc[-1]:,.0f}")
col3.metric("Credit Line Available", f"${filtered_data['Credit_Line_Available'].iloc[-1]:,.0f}")
col4.metric("Inventory", f"${filtered_data['Inventory'].iloc[-1]:,.0f}")

# Financial Overview
st.subheader("Financial Overview")
col1, col2 = st.columns(2)

# Income vs Expenses
fig_income_expenses = px.bar(filtered_data, x='Date', y=['Income', 'Expenses'],
                             title='Income vs Expenses')
col1.plotly_chart(fig_income_expenses, use_container_width=True)

# Expense Breakdown (using last day's data)
expense_data = {
    'Category': ['Operating', 'Payroll', 'Marketing', 'R&D', 'Other'],
    'Amount': filtered_data['Expenses'].iloc[-1] * np.array([0.4, 0.3, 0.1, 0.15, 0.05])
}
fig_expenses = px.pie(expense_data, values='Amount', names='Category',
                      title='Expense Breakdown (Last Day)')
col2.plotly_chart(fig_expenses, use_container_width=True)

# Receivables and Payables
st.subheader("Receivables and Payables")
col1, col2 = st.columns(2)

# Receivables with Days Turnover
fig_receivables = go.Figure()
fig_receivables.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Receivables'],
                                     name='Receivables'))
fig_receivables.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Days_Turnover'],
                                     name='Days Turnover', yaxis='y2'))
fig_receivables.update_layout(title='Receivables and Days Turnover',
                              yaxis=dict(title='Receivables'),
                              yaxis2=dict(title='Days Turnover', overlaying='y', side='right'))
col1.plotly_chart(fig_receivables, use_container_width=True)

# Payables with Days to Pay
fig_payables = go.Figure()
fig_payables.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Payables'],
                                  name='Payables'))
fig_payables.add_trace(go.Scatter(x=filtered_data['Date'], y=filtered_data['Days_to_Pay'],
                                  name='Days to Pay', yaxis='y2'))
fig_payables.update_layout(title='Payables and Days to Pay',
                           yaxis=dict(title='Payables'),
                           yaxis2=dict(title='Days to Pay', overlaying='y', side='right'))
col2.plotly_chart(fig_payables, use_container_width=True)

# Performance Metrics
st.subheader("Performance Metrics")
col1, col2 = st.columns(2)

# Return on Equity
fig_roe = px.line(filtered_data, x='Date', y='Return_on_Equity',
                  title='Return on Equity')
col1.plotly_chart(fig_roe, use_container_width=True)

# Return on Assets
fig_roa = px.line(filtered_data, x='Date', y='Return_on_Assets',
                  title='Return on Assets')
col2.plotly_chart(fig_roa, use_container_width=True)

# Historical Data Viewer
st.subheader("Historical Data Viewer")
days_to_view = st.slider("Select number of days to view", 7, 365, 30)
historical_df = filtered_data.tail(days_to_view)

# Historical data table
st.dataframe(historical_df)
