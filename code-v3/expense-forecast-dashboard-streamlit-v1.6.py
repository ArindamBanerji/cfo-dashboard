import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# Set page config for a wide layout
st.set_page_config(page_title="Expense Forecast Dashboard", layout="wide")

# Utility function to format numbers
def format_number(num):
    if num >= 1e9:
        return f"${num/1e9:.1f}B"
    elif num >= 1e6:
        return f"${num/1e6:.1f}M"
    else:
        return f"${num:.0f}"

# Function to generate sample data
def generate_sample_data(quarters=5):
    data = []
    base_date = datetime.now()
    for i in range(quarters):
        quarter_date = base_date + timedelta(days=90*i)
        quarter_data = {
            'quarter': f"Q{((quarter_date.month-1)//3)+1} {quarter_date.year}",
            'payrollCosts': np.random.uniform(800000000, 1000000000),
            'COGS': np.random.uniform(1600000000, 2000000000),
            'operatingCost': np.random.uniform(400000000, 500000000),
            'overheadCost': np.random.uniform(200000000, 250000000),
            'RDExpenses': np.random.uniform(200000000, 250000000),
            'marketingSalesExpenses': np.random.uniform(300000000, 375000000)
        }
        quarter_data['totalExpenses'] = sum(v for k, v in quarter_data.items() if k != 'quarter')
        data.append(quarter_data)
    return pd.DataFrame(data)

# Function to perform sensitivity analysis
def sensitivity_analysis(base_data):
    parameters = ['payrollCosts', 'COGS', 'operatingCost', 'overheadCost', 'RDExpenses', 'marketingSalesExpenses']
    variations = [-20, -10, 0, 10, 20]  # Percentage variations

    results = []
    base_expenses = base_data['totalExpenses'].sum()

    sensitivity_factors = {
        'payrollCosts': 0.8,
        'COGS': 1.2,
        'operatingCost': 0.6,
        'overheadCost': 0.4,
        'RDExpenses': 0.3,
        'marketingSalesExpenses': 0.5
    }

    for param in parameters:
        for variation in variations:
            modified_data = base_data.copy()
            modified_data[param] *= (1 + variation / 100)
            modified_data['totalExpenses'] = modified_data[parameters].sum(axis=1)
            total_expenses = modified_data['totalExpenses'].sum()
            parameter_contribution = total_expenses - base_expenses
            
            percent_change = (parameter_contribution / base_expenses) * 100 * sensitivity_factors[param]
            
            results.append({
                'parameter': param,
                'variation': variation,
                'percentChange': percent_change
            })

    return pd.DataFrame(results)

# Generate sample data
data = generate_sample_data()

# Perform sensitivity analysis
sensitivity_results = sensitivity_analysis(data)

# Calculate base expenses
base_expenses = data['totalExpenses'].sum()

# Dashboard title
st.title("Expense Forecast Dashboard")

# Input Parameters section
st.subheader("Expense Categories")
cols = st.columns(3)
for i, (key, value) in enumerate(data.iloc[0].items()):
    if key not in ['quarter', 'totalExpenses']:
        cols[i % 3].metric(key, format_number(value))

# Quarterly Expense Forecast chart
st.subheader("Quarterly Expense Forecast")
fig = px.bar(data, x='quarter', y='totalExpenses', 
             labels={'totalExpenses': 'Total Expenses'},
             title='Quarterly Expense Forecast')
fig.update_layout(yaxis_title='Expenses')
fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
st.plotly_chart(fig, use_container_width=True)

# Sensitivity Analysis
st.subheader("Sensitivity Analysis")

# Prepare data for the table
pivot_table = sensitivity_results.pivot(index='parameter', columns='variation', values='percentChange')
pivot_table = pivot_table.reset_index()
pivot_table.columns = ['Parameter', '-20%', '-10%', '0%', '10%', '20%']

# Format percentages and prepare color coding
def format_and_color(val):
    color = 'red' if val > 0 else 'green'
    return f'<span style="color:{color}">{val:.2f}%</span>'

for col in pivot_table.columns[1:]:
    pivot_table[col] = pivot_table[col].apply(format_and_color)

# Display the table with colors
st.write(pivot_table.to_html(escape=False, index=False), unsafe_allow_html=True)

# Forecast Summary
st.subheader("Forecast Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Base Expenses", format_number(base_expenses))
with col2:
    min_expenses = base_expenses * (1 + sensitivity_results['percentChange'].min() / 100)
    st.metric("Minimum Expenses", format_number(min_expenses))
with col3:
    max_expenses = base_expenses * (1 + sensitivity_results['percentChange'].max() / 100)
    st.metric("Maximum Expenses", format_number(max_expenses))

# Forecast Data
st.subheader("Forecast Data")
st.dataframe(data)

# Add a download button for the full dataset
csv = data.to_csv(index=False)
st.download_button(
    label="Download full dataset as CSV",
    data=csv,
    file_name="expense_forecast_data.csv",
    mime="text/csv",
)
