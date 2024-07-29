import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict

def generate_sample_data() -> List[Dict]:
    """
    Generate realistic sample data for 5 quarters.
    
    Returns:
        List[Dict]: A list of dictionaries containing the sample data for each quarter.
    """
    quarters = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025']
    base_assets = 4000000000  # $4B company
    
    data = []
    for index, quarter in enumerate(quarters):
        seasonal_factor = 1 + np.sin(index * np.pi / 2) * 0.2
        random_factor = 0.8 + np.random.random() * 0.4
        
        data.append({
            'quarter': quarter,
            'cash': base_assets * 0.1 * seasonal_factor * random_factor,
            'accountsReceivable': base_assets * 0.15 * seasonal_factor * random_factor,
            'inventory': base_assets * 0.2 * seasonal_factor * random_factor,
            'ppe': base_assets * 0.4 * (1 + index * 0.05) * random_factor,
            'accountsPayable': base_assets * 0.1 * seasonal_factor * random_factor,
            'shortTermDebt': base_assets * 0.05 * (1 - index * 0.03) * random_factor,
            'longTermDebt': base_assets * 0.3 * (1 - index * 0.01) * random_factor,
            'retainedEarnings': base_assets * 0.2 * (1 + index * 0.04) * random_factor,
            'capex': base_assets * 0.05 * seasonal_factor * random_factor,
            'depreciationAmortization': base_assets * 0.03 * (1 + index * 0.02) * random_factor,
        })
    
    return data

def calculate_balance_sheet(data: List[Dict], variation_percentage: float = 0) -> List[Dict]:
    """
    Calculate balance sheet totals based on the given data and variation percentage.
    
    Args:
        data (List[Dict]): List of dictionaries containing financial data for each quarter.
        variation_percentage (float): Percentage to vary the balance sheet calculation.
    
    Returns:
        List[Dict]: Calculated balance sheet totals for each quarter.
    """
    variation_factor = 1 + (variation_percentage / 100)
    
    balance_sheet = []
    for quarter in data:
        total_assets = (quarter['cash'] + quarter['accountsReceivable'] + 
                        quarter['inventory'] + quarter['ppe']) * variation_factor
        total_liabilities = (quarter['accountsPayable'] + quarter['shortTermDebt'] + 
                             quarter['longTermDebt']) * variation_factor
        total_equity = quarter['retainedEarnings'] * variation_factor
        
        balance_sheet.append({
            'quarter': quarter['quarter'],
            'totalAssets': total_assets,
            'totalLiabilities': total_liabilities,
            'totalEquity': total_equity,
            'balanceSheetTotal': total_assets,  # Assets = Liabilities + Equity
        })
    
    return balance_sheet

def sensitivity_analysis() -> Dict:
    """
    Perform sensitivity analysis for balance sheet parameters.
    
    Returns:
        Dict: Results of the sensitivity analysis.
    """
    parameters = [
        'cash', 'accountsReceivable', 'inventory', 'ppe', 'accountsPayable',
        'shortTermDebt', 'longTermDebt', 'retainedEarnings', 'capex', 'depreciationAmortization'
    ]

    results = {}
    for param in parameters:
        # Generate random impacts between -20% and 20%, ensuring they're not close to zero
        increased_impact = (np.random.random() * 15 + 5) * (1 if np.random.random() < 0.5 else -1)
        decreased_impact = (np.random.random() * 15 + 5) * (1 if np.random.random() < 0.5 else -1)
        
        results[param] = {
            'increased': increased_impact,
            'decreased': decreased_impact
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
        return f"${value/1e9:.2f}B"
    elif abs_value >= 1e6:
        return f"${value/1e6:.2f}M"
    elif abs_value >= 1e3:
        return f"${value/1e3:.2f}K"
    else:
        return f"${value:.2f}"

def create_forecast_chart(combined_forecast: pd.DataFrame) -> go.Figure:
    """
    Create a line chart for the balance sheet forecast.
    
    Args:
        combined_forecast (pd.DataFrame): DataFrame containing the forecast data.
    
    Returns:
        go.Figure: Plotly figure object for the forecast chart.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=combined_forecast['quarter'], y=combined_forecast['baseTotal'],
                             mode='lines+markers', name='Base Forecast'))
    fig.add_trace(go.Scatter(x=combined_forecast['quarter'], y=combined_forecast['maxTotal'],
                             mode='lines+markers', name='Maximum Forecast'))
    fig.add_trace(go.Scatter(x=combined_forecast['quarter'], y=combined_forecast['minTotal'],
                             mode='lines+markers', name='Minimum Forecast'))
    fig.update_layout(title='Quarterly Balance Sheet Forecast',
                      xaxis_title='Quarter',
                      yaxis_title='Balance Sheet Total',
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

def balance_sheet_forecast_dashboard():
    """
    Main function to create and display the balance sheet forecast dashboard.
    """
#   st.set_page_config(page_title="Balance Sheet Forecast Dashboard", layout="wide")
    
    st.title("Balance Sheet Forecast Dashboard")

    # Generate data
    data = generate_sample_data()
    base_balance_sheet = calculate_balance_sheet(data)
    max_balance_sheet = calculate_balance_sheet(data, 10)
    min_balance_sheet = calculate_balance_sheet(data, -10)
    sensitivity_results = sensitivity_analysis()

    # Prepare data for charts
    combined_forecast = pd.DataFrame({
        'quarter': [q['quarter'] for q in base_balance_sheet],
        'baseTotal': [q['balanceSheetTotal'] for q in base_balance_sheet],
        'maxTotal': [q['balanceSheetTotal'] for q in max_balance_sheet],
        'minTotal': [q['balanceSheetTotal'] for q in min_balance_sheet]
    })

    # Display summary cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Base Forecast", format_currency(combined_forecast['baseTotal'].sum()))
    with col2:
        st.metric("Maximum Forecast", format_currency(combined_forecast['maxTotal'].sum()))
    with col3:
        st.metric("Minimum Forecast", format_currency(combined_forecast['minTotal'].sum()))

    # Display forecast chart
    st.plotly_chart(create_forecast_chart(combined_forecast), use_container_width=True)

    # Display sensitivity heatmap
    st.plotly_chart(create_sensitivity_heatmap(sensitivity_results), use_container_width=True)

    # Display last quarter's data
    st.subheader("Last Quarter's Data")
    last_quarter_data = pd.DataFrame([data[-1]]).T.reset_index()
    last_quarter_data.columns = ['Parameter', 'Value']
    last_quarter_data['Value'] = last_quarter_data['Value'].apply(lambda x: format_currency(x) if isinstance(x, (int, float)) else x)
    st.dataframe(last_quarter_data)

def balance_sheet_forecast_table():
    """
    Entry point function to create the balance sheet forecast dashboard.
    This function can be called from another module to create the entire dashboard.
    """
    balance_sheet_forecast_dashboard()

if __name__ == "__main__":
    balance_sheet_forecast_table()
