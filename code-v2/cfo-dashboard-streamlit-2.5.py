import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Set page config for a wide layout
st.set_page_config(page_title="CFO Dashboard", layout="wide")

# Function to generate quarterly financial data
def generate_quarterly_data(years=1):
    data = []
    base_date = datetime.now()
    for i in range(years * 4):
        date = base_date - timedelta(days=90 * i)
        total_income = np.random.uniform(900000000, 1000000000)  # Income around $900M-$1B
        total_expenses = np.random.uniform(880000000, 970000000)  # Expenses slightly lower for profit
        quarter_data = {
            'quarter': f"Q{((date.month - 1) // 3) + 1} {date.year}",
            'income': total_income,
            'expenses': total_expenses,
            'income_components': {
                'passenger_vehicles': total_income * 0.4,
                'trucking_lines': total_income * 0.3,
                'services': total_income * 0.2,
                'licensing': total_income * 0.1
            },
            'expense_components': {
                'COGS': total_expenses * 0.5,
                'SGA': total_expenses * 0.2,
                'RD': total_expenses * 0.15,
                'depreciation_amortization': total_expenses * 0.1,
                'other': total_expenses * 0.05
            },
            'bank_balance': np.random.uniform(50000000, 100000000),
            'credit_card_balance': np.random.uniform(1000000, 5000000),
            'credit_line_available': np.random.uniform(20000000, 50000000),
            'inventory': np.random.uniform(200000000, 400000000),
            'payables': np.random.uniform(100000000, 200000000),
            'receivables': np.random.uniform(150000000, 300000000),
            'payroll_liabilities': np.random.uniform(20000000, 40000000),
            'days_to_pay': np.random.randint(30, 60),
            'days_turnover': np.random.randint(45, 75),
            'return_on_equity': np.random.uniform(0.05, 0.15),
            'return_on_assets': np.random.uniform(0.03, 0.10),
        }
        data.append(quarter_data)
    return list(reversed(data))  # Most recent quarter first

# Function to abbreviate large numbers for readability
def abbreviate_number(num):
    if num >= 1e9:
        return f"${num/1e9:.1f}B"
    elif num >= 1e6:
        return f"${num/1e6:.1f}M"
    elif num >= 1e3:
        return f"${num/1e3:.1f}K"
    else:
        return f"${num:.1f}"

# Generate 2 years of quarterly data
data = generate_quarterly_data(2)

# Create DataFrames for easier data manipulation
df = pd.DataFrame(data)
df_income = pd.DataFrame([q['income_components'] for q in data])
df_expenses = pd.DataFrame([q['expense_components'] for q in data])

# Dashboard title
st.title("CFO Dashboard - Overview")

# Metric cards for key financial indicators
col1, col2, col3, col4 = st.columns(4)
latest = df.iloc[-1]  # Most recent quarter
previous = df.iloc[-2]  # Previous quarter

def metric_card(col, title, current, previous):
    change = (current - previous) / previous
    arrow = "▲" if change >= 0 else "▼"
    color = "green" if change >= 0 else "red"
    
    col.markdown(f"**{title}**")
    col.markdown(f"### {abbreviate_number(current)}")
    col.markdown(f"<span style='color: {color}'>{arrow} {change:.1%}</span>", unsafe_allow_html=True)

# Display metric cards
metric_card(col1, "Bank Balance", latest['bank_balance'], previous['bank_balance'])
metric_card(col2, "Credit Card Balance", latest['credit_card_balance'], previous['credit_card_balance'])
metric_card(col3, "Credit Line Available", latest['credit_line_available'], previous['credit_line_available'])
metric_card(col4, "Inventory", latest['inventory'], previous['inventory'])

# Quarterly Income vs Expenses chart
st.subheader("Quarterly Income vs Expenses")
fig = go.Figure()
fig.add_trace(go.Bar(x=df['quarter'], y=df['income'], name='Income'))
fig.add_trace(go.Bar(x=df['quarter'], y=df['expenses'], name='Expenses'))
fig.update_layout(barmode='group', height=400)
fig.update_yaxes(tickprefix="$", tickformat=",.0f")
st.plotly_chart(fig, use_container_width=True)

# Income and Expense Components charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Income Components (Last Quarter)")
    fig = px.bar(
        x=df_income.iloc[-1].values,
        y=df_income.iloc[-1].index,
        orientation='h'
    )
    fig.update_xaxes(tickprefix="$", tickformat=",.0f")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Expense Components (Last Quarter)")
    fig = px.bar(
        x=df_expenses.iloc[-1].values,
        y=df_expenses.iloc[-1].index,
        orientation='h'
    )
    fig.update_xaxes(tickprefix="$", tickformat=",.0f")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Receivables and Days Turnover chart
st.subheader("Receivables and Days Turnover")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['quarter'], y=df['receivables'], name='Receivables', yaxis='y'))
fig.add_trace(go.Scatter(x=df['quarter'], y=df['days_turnover'], name='Days Turnover', yaxis='y2'))
fig.update_layout(
    yaxis=dict(title='Receivables', tickprefix="$", tickformat=",.0f"),
    yaxis2=dict(title='Days Turnover', overlaying='y', side='right'),
    height=400
)
st.plotly_chart(fig, use_container_width=True)

# Return on Equity (ROE) and Return on Assets (ROA) charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Return on Equity")
    fig = px.line(df, x='quarter', y='return_on_equity')
    fig.update_yaxes(tickformat=".1%")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Return on Assets")
    fig = px.line(df, x='quarter', y='return_on_assets')
    fig.update_yaxes(tickformat=".1%")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Historical Data Table
st.subheader("Historical Data")

# Prepare data for display
display_df = df.copy()
numeric_columns = ['income', 'expenses', 'bank_balance', 'credit_card_balance', 'credit_line_available', 
                   'inventory', 'payables', 'receivables', 'payroll_liabilities']

# Format numeric columns
for col in numeric_columns:
    display_df[col] = display_df[col].apply(abbreviate_number)

# Format percentage columns
display_df['return_on_equity'] = display_df['return_on_equity'].apply(lambda x: f"{x:.2%}")
display_df['return_on_assets'] = display_df['return_on_assets'].apply(lambda x: f"{x:.2%}")

# Reorder columns for logical display
columns_order = ['quarter', 'income', 'expenses', 'bank_balance', 'credit_card_balance', 'credit_line_available', 
                 'inventory', 'payables', 'receivables', 'payroll_liabilities', 'days_to_pay', 'days_turnover', 
                 'return_on_equity', 'return_on_assets']
display_df = display_df[columns_order]

# Display the formatted table
st.dataframe(display_df, use_container_width=True)

# Add a download button for the full dataset
csv = df.to_csv(index=False)
st.download_button(
    label="Download full dataset as CSV",
    data=csv,
    file_name="cfo_dashboard_data.csv",
    mime="text/csv",
)
