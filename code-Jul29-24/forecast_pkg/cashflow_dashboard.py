import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict

def generate_realistic_sample_data() -> List[Dict]:
    """
    Generate realistic sample data for 5 quarters.
    
    Returns:
        List[Dict]: A list of dictionaries containing the sample data for each quarter.
    """
    quarters = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025']
    base_revenue = 1000000000
    base_costs = 400000000

    data = []
    for index, quarter in enumerate(quarters):
        seasonal_factor = 1 + np.sin(index * np.pi / 2) * 0.15
        random_factor = 0.9 + np.random.random() * 0.2

        data.append({
            'quarter': quarter,
            'salesRevenue': base_revenue * seasonal_factor * random_factor,
            'accountsReceivableDays': 45 + np.random.randint(-5, 6),
            'rawMaterialCosts': base_costs * seasonal_factor * (0.95 + np.random.random() * 0.1),
            'laborCosts': 300000000 * (1 + index * 0.02) * random_factor,
            'accountsPayableDays': 30 + np.random.randint(-3, 4),
            'capex': 50000000 * (1 - index * 0.05) * random_factor,
            'inventoryTurnover': 6 + np.random.random() - 0.5,
            'operatingExpenses': 180000000 * (1 + index * 0.01) * random_factor,
            'debtRepayments': 20000000,
            'taxPayments': 10000000 * seasonal_factor * random_factor,
            'seasonalFactor': seasonal_factor,
            'customerPrepayments': 50000000 * seasonal_factor * random_factor,
            'supplierCreditDays': 45 + np.random.randint(-2, 3),
            'dividendPayments': 5000000,
            'fxRate': 1 + (index * 0.02) + (np.random.random() * 0.04 - 0.02)
        })

    return data

def calculate_cashflow(data: List[Dict], variation_percentage: float = 0) -> List[Dict]:
    """
    Calculate cashflow based on the given data and variation percentage.
    
    Args:
        data (List[Dict]): List of dictionaries containing financial data for each quarter.
        variation_percentage (float): Percentage to vary the cashflow calculation.
    
    Returns:
        List[Dict]: Calculated cashflow for each quarter.
    """
    cashflow = []
    for quarter in data:
        days_in_quarter = 91
        variation_factor = 1 + (variation_percentage / 100)
        
        cash_inflow = (quarter['salesRevenue'] * variation_factor * (days_in_quarter / quarter['accountsReceivableDays']) +
                       quarter['customerPrepayments'] * variation_factor)
        
        cash_outflow = ((quarter['rawMaterialCosts'] + quarter['laborCosts']) * variation_factor * (days_in_quarter / quarter['accountsPayableDays']) +
                        quarter['capex'] * variation_factor +
                        quarter['operatingExpenses'] * variation_factor +
                        quarter['debtRepayments'] +
                        quarter['taxPayments'] * variation_factor +
                        quarter['dividendPayments'])
        
        net_cashflow = cash_inflow - cash_outflow
        
        cashflow.append({
            'quarter': quarter['quarter'],
            'netCashflow': net_cashflow
        })

    return cashflow

def sensitivity_analysis(base_data: List[Dict], variation_percentage: float = 10) -> Dict:
    """
    Perform sensitivity analysis on the given data.
    
    Args:
        base_data (List[Dict]): List of dictionaries containing financial data for each quarter.
        variation_percentage (float): Percentage to vary for sensitivity analysis.
    
    Returns:
        Dict: Results of the sensitivity analysis.
    """
    parameters = [
        'salesRevenue', 'accountsReceivableDays', 'rawMaterialCosts', 'laborCosts',
        'accountsPayableDays', 'capex', 'inventoryTurnover', 'operatingExpenses',
        'debtRepayments', 'taxPayments', 'seasonalFactor', 'customerPrepayments',
        'supplierCreditDays', 'dividendPayments', 'fxRate'
    ]

    results = {}

    for param in parameters:
        increased_data = [{**quarter, param: quarter[param] * (1 + variation_percentage / 100)} for quarter in base_data]
        decreased_data = [{**quarter, param: quarter[param] * (1 - variation_percentage / 100)} for quarter in base_data]

        base_cashflow = calculate_cashflow(base_data)
        increased_cashflow = calculate_cashflow(increased_data)
        decreased_cashflow = calculate_cashflow(decreased_data)

        total_base_net_cashflow = sum(q['netCashflow'] for q in base_cashflow)
        total_increased_net_cashflow = sum(q['netCashflow'] for q in increased_cashflow)
        total_decreased_net_cashflow = sum(q['netCashflow'] for q in decreased_cashflow)

        results[param] = {
            'increased': (total_increased_net_cashflow - total_base_net_cashflow) / total_base_net_cashflow * 100,
            'decreased': (total_decreased_net_cashflow - total_base_net_cashflow) / total_base_net_cashflow * 100
        }

    return results

def format_currency(value: float) -> str:
    """
    Format a currency value into a string with appropriate suffix (B, M, K).
    
    Args:
        value (float): The currency value to format.
    
    Returns:
        str: Formatted currency string.
    """
    abs_value = abs(value)
    if abs_value >= 1e9:
        return f"${value/1e9:.1f}B"
    elif abs_value >= 1e6:
        return f"${value/1e6:.1f}M"
    elif abs_value >= 1e3:
        return f"${value/1e3:.1f}K"
    else:
        return f"${value:.0f}"

def create_forecast_chart(combined_forecast: pd.DataFrame) -> go.Figure:
    """
    Create a line chart for the cashflow forecast.
    
    Args:
        combined_forecast (pd.DataFrame): DataFrame containing the forecast data.
    
    Returns:
        go.Figure: Plotly figure object for the forecast chart.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=combined_forecast['quarter'], y=combined_forecast['baseNetCashflow'],
                             mode='lines+markers', name='Base Forecast'))
    fig.add_trace(go.Scatter(x=combined_forecast['quarter'], y=combined_forecast['maxNetCashflow'],
                             mode='lines+markers', name='Maximum Forecast'))
    fig.add_trace(go.Scatter(x=combined_forecast['quarter'], y=combined_forecast['minNetCashflow'],
                             mode='lines+markers', name='Minimum Forecast'))
    fig.update_layout(title='Quarterly Cashflow Forecast',
                      xaxis_title='Quarter',
                      yaxis_title='Net Cashflow',
                      yaxis_tickformat='$,.0f')
    return fig

def create_sensitivity_heatmap(sensitivity_results: Dict) -> go.Figure:
    """
    Create a heatmap for the sensitivity analysis results.
    
    Args:
        sensitivity_results (Dict): Dictionary containing the sensitivity analysis results.
    
    Returns:
        go.Figure: Plotly figure object for the sensitivity heatmap.
    """
    df = pd.DataFrame(sensitivity_results).T.reset_index()
    df.columns = ['Parameter', 'Increased', 'Decreased']
    df_melted = df.melt(id_vars=['Parameter'], var_name='Change', value_name='Impact')
    
    fig = px.imshow(df_melted.pivot(index='Parameter', columns='Change', values='Impact'),
                    labels=dict(x="Change", y="Parameter", color="Impact (%)"),
                    x=['Increased', 'Decreased'],
                    color_continuous_scale='RdYlGn',
                    aspect="auto")
    
    fig.update_traces(text=df_melted.pivot(index='Parameter', columns='Change', values='Impact').values,
                      texttemplate="%{text:.2f}%")
    fig.update_layout(title='Sensitivity Analysis')
    return fig

def cashflow_forecast_dashboard():
    """
    Main function to create and display the cashflow forecast dashboard.
    """
    # st.set_page_config(page_title="Cashflow Forecast Dashboard", layout="wide")
    st.title("Cashflow Forecast Dashboard")

    # Generate data
    data = generate_realistic_sample_data()
    base_forecast = calculate_cashflow(data)
    max_forecast = calculate_cashflow(data, 10)
    min_forecast = calculate_cashflow(data, -10)
    sensitivity_results = sensitivity_analysis(data)

    # Prepare data for charts
    combined_forecast = pd.DataFrame({
        'quarter': [q['quarter'] for q in base_forecast],
        'baseNetCashflow': [q['netCashflow'] for q in base_forecast],
        'maxNetCashflow': [q['netCashflow'] for q in max_forecast],
        'minNetCashflow': [q['netCashflow'] for q in min_forecast]
    })

    # Display summary cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Base Forecast", format_currency(combined_forecast['baseNetCashflow'].sum()))
    with col2:
        st.metric("Maximum Forecast", format_currency(combined_forecast['maxNetCashflow'].sum()))
    with col3:
        st.metric("Minimum Forecast", format_currency(combined_forecast['minNetCashflow'].sum()))

    # Display forecast chart
    st.plotly_chart(create_forecast_chart(combined_forecast), use_container_width=True)

    # Display sensitivity heatmap
    st.plotly_chart(create_sensitivity_heatmap(sensitivity_results), use_container_width=True)

    # Display last quarter's data
    st.subheader("Last Quarter's Data")
    last_quarter_data = pd.DataFrame([data[-1]]).T.reset_index()
    last_quarter_data.columns = ['Parameter', 'Value']
    st.dataframe(last_quarter_data)

if __name__ == "__main__":
    cashflow_forecast_dashboard()
