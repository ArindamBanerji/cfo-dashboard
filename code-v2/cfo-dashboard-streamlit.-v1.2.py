import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('cfo_dashboard_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Set page config
st.set_page_config(page_title="CFO Dashboard - Overview", layout="wide")

# Title
st.title("CFO Dashboard - Overview")

# Date range selector
col1, col2 = st.columns(2)
start_date = col1.date_input("Start Date", df['Date'].min())
end_date = col2.date_input("End Date", df['Date'].max())

# Filter data based on date range
mask = (df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))
filtered_df = df.loc[mask]

# Key Metrics
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Bank Balance", f"${filtered_df['Bank_Balance'].iloc[-1]:,.0f}")
col2.metric("Credit Card Balance", f"${filtered_df['Credit_Card_Balance'].iloc[-1]:,.0f}")
col3.metric("Credit Line Available", f"${filtered_df['Credit_Line_Available'].iloc[-1]:,.0f}")
col4.metric("Inventory", f"${filtered_df['Inventory'].iloc[-1]:,.0f}")

# Financial Overview
st.subheader("Financial Overview")
col1, col2 = st.columns(2)

# Income vs Expenses
fig_income_expenses = px.bar(filtered_df, x='Date', y=['Income', 'Expenses'],
                             title='Income vs Expenses')
col1.plotly_chart(fig_income_expenses, use_container_width=True)

# Expense Breakdown (using last day's data)
expense_data = {
    'Category': ['Operating Expenses', 'Payroll', 'Marketing', 'R&D', 'Other'],
    'Amount': filtered_df['Expenses'].iloc[-1] * np.array([0.4, 0.3, 0.1, 0.15, 0.05])
}
fig_expenses = px.pie(expense_data, values='Amount', names='Category',
                      title='Expense Breakdown (Last Day)')
col2.plotly_chart(fig_expenses, use_container_width=True)

# Receivables and Payables
st.subheader("Receivables and Payables")
col1, col2 = st.columns(2)

# Receivables with Days Turnover
fig_receivables = go.Figure()
fig_receivables.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Receivables'],
                                     name='Receivables'))
fig_receivables.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Days_Turnover'],
                                     name='Days Turnover', yaxis='y2'))
fig_receivables.update_layout(title='Receivables and Days Turnover',
                              yaxis=dict(title='Receivables'),
                              yaxis2=dict(title='Days Turnover', overlaying='y', side='right'))
col1.plotly_chart(fig_receivables, use_container_width=True)

# Payables with Days to Pay
fig_payables = go.Figure()
fig_payables.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Payables'],
                                  name='Payables'))
fig_payables.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Days_to_Pay'],
                                  name='Days to Pay', yaxis='y2'))
fig_payables.update_layout(title='Payables and Days to Pay',
                           yaxis=dict(title='Payables'),
                           yaxis2=dict(title='Days to Pay', overlaying='y', side='right'))
col2.plotly_chart(fig_payables, use_container_width=True)

# Performance Metrics
st.subheader("Performance Metrics")
col1, col2 = st.columns(2)

# Return on Equity
fig_roe = px.line(filtered_df, x='Date', y='Return_on_Equity',
                  title='Return on Equity')
col1.plotly_chart(fig_roe, use_container_width=True)

# Return on Assets
fig_roa = px.line(filtered_df, x='Date', y='Return_on_Assets',
                  title='Return on Assets')
col2.plotly_chart(fig_roa, use_container_width=True)

# Historical Data Viewer
st.subheader("Historical Data Viewer")
days_to_view = st.slider("Select number of days to view", 7, 365, 30)
historical_df = filtered_df.tail(days_to_view)

# Historical data table
st.dataframe(historical_df)
