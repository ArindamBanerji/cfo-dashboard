import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Set page config
st.set_page_config(layout="wide", page_title="CFO Dashboard - Overview")

# Generate sample data
@st.cache_data
def generate_data(days):
    data = []
    base_date = datetime.now()
    for i in range(days):
        date = base_date - timedelta(days=i)
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "bank_balance": np.random.uniform(50000000, 100000000),
            "credit_card_balance": np.random.uniform(1000000, 5000000),
            "credit_line_available": np.random.uniform(20000000, 50000000),
            "expenses": np.random.uniform(9800000, 10200000),
            "income": np.random.uniform(10800000, 11200000),
            "inventory": np.random.uniform(200000000, 400000000),
            "payables": np.random.uniform(100000000, 200000000),
            "receivables": np.random.uniform(150000000, 300000000),
            "payroll_liabilities": np.random.uniform(20000000, 40000000),
            "days_to_pay": np.random.randint(30, 60),
            "days_turnover": np.random.randint(45, 75),
            "return_on_equity": np.random.uniform(0.05, 0.15),
            "return_on_assets": np.random.uniform(0.03, 0.10),
        })
    return pd.DataFrame(data[::-1])

# Load data
df = generate_data(365)

# Title
st.title("CFO Dashboard - Overview")

# Metric cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Bank Balance", f"${df['bank_balance'].iloc[-1]:,.0f}")
with col2:
    st.metric("Credit Card Balance", f"${df['credit_card_balance'].iloc[-1]:,.0f}")
with col3:
    st.metric("Credit Line Available", f"${df['credit_line_available'].iloc[-1]:,.0f}")
with col4:
    st.metric("Inventory", f"${df['inventory'].iloc[-1]:,.0f}")

# Income vs Expenses
st.subheader("Income vs Expenses")
fig_income_expenses = go.Figure()
fig_income_expenses.add_trace(go.Bar(x=df['date'].tail(30), y=df['income'].tail(30), name="Income"))
fig_income_expenses.add_trace(go.Bar(x=df['date'].tail(30), y=df['expenses'].tail(30), name="Expenses"))
fig_income_expenses.update_layout(barmode='group', height=400)
st.plotly_chart(fig_income_expenses, use_container_width=True)

# Expense Breakdown
st.subheader("Expense Breakdown")
expense_data = {
    'Category': ['Operating', 'Payroll', 'Marketing', 'R&D', 'Other'],
    'Amount': df['expenses'].iloc[-1] * np.array([0.4, 0.3, 0.1, 0.15, 0.05])
}
fig_expense_breakdown = px.pie(expense_data, values='Amount', names='Category', height=400)
st.plotly_chart(fig_expense_breakdown, use_container_width=True)

# Receivables and Days Turnover
st.subheader("Receivables and Days Turnover")
fig_receivables = go.Figure()
fig_receivables.add_trace(go.Scatter(x=df['date'].tail(90), y=df['receivables'].tail(90), name="Receivables"))
fig_receivables.add_trace(go.Scatter(x=df['date'].tail(90), y=df['days_turnover'].tail(90), name="Days Turnover", yaxis="y2"))
fig_receivables.update_layout(
    yaxis2=dict(title="Days", overlaying="y", side="right"),
    height=400
)
st.plotly_chart(fig_receivables, use_container_width=True)

# Payables and Days to Pay
st.subheader("Payables and Days to Pay")
fig_payables = go.Figure()
fig_payables.add_trace(go.Scatter(x=df['date'].tail(90), y=df['payables'].tail(90), name="Payables"))
fig_payables.add_trace(go.Scatter(x=df['date'].tail(90), y=df['days_to_pay'].tail(90), name="Days to Pay", yaxis="y2"))
fig_payables.update_layout(
    yaxis2=dict(title="Days", overlaying="y", side="right"),
    height=400
)
st.plotly_chart(fig_payables, use_container_width=True)

# Return on Equity
st.subheader("Return on Equity")
fig_roe = px.line(df, x='date', y='return_on_equity', height=400)
st.plotly_chart(fig_roe, use_container_width=True)

# Return on Assets
st.subheader("Return on Assets")
fig_roa = px.line(df, x='date', y='return_on_assets', height=400)
st.plotly_chart(fig_roa, use_container_width=True)
