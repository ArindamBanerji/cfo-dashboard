import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Set page config - check
st.set_page_config(page_title="CFO Dashboard", layout="wide")

# Function to generate sample data
def generate_sample_data():
    return {
        "financial_performance": {
            "profitability": {
                "gross_profit_margin": np.random.uniform(0.2, 0.6),
                "operating_profit_margin": np.random.uniform(0.1, 0.3),
                "net_profit_margin": np.random.uniform(0.05, 0.2),
                "ebitda_margin": np.random.uniform(0.15, 0.4),
                "roa": np.random.uniform(0.05, 0.2),
                "roe": np.random.uniform(0.1, 0.3),
                "roic": np.random.uniform(0.08, 0.26),
            },
            "revenue": {
                "total": np.random.uniform(500000000, 1500000000),
                "by_product_line": {
                    "Product A": np.random.uniform(100000000, 400000000),
                    "Product B": np.random.uniform(100000000, 300000000),
                    "Product C": np.random.uniform(50000000, 150000000),
                },
                "growth_rate": np.random.uniform(-0.05, 0.15),
                "average_revenue_per_customer": np.random.uniform(5000, 15000),
            },
            "costs": {
                "cogs": np.random.uniform(300000000, 900000000),
                "operating_expenses": np.random.uniform(100000000, 300000000),
                "sga_expenses": np.random.uniform(75000000, 225000000),
                "rd_expenses": np.random.uniform(25000000, 75000000),
            },
            "cash_flow": {
                "operating_cash_flow": np.random.uniform(50000000, 250000000),
                "free_cash_flow": np.random.uniform(25000000, 125000000),
                "cash_conversion_cycle": np.random.uniform(30, 90),
            },
            "working_capital": {
                "current_ratio": np.random.uniform(1.5, 2.5),
                "quick_ratio": np.random.uniform(1, 1.5),
                "inventory_turnover_ratio": np.random.uniform(4, 10),
                "days_sales_outstanding": np.random.uniform(30, 60),
                "days_payables_outstanding": np.random.uniform(45, 75),
            },
        },
        "operational_efficiency": {
            "production": {
                "capacity_utilization": np.random.uniform(0.6, 0.9),
                "oee": np.random.uniform(0.6, 0.9),
                "production_volume": np.random.uniform(500000, 1500000),
                "production_cycle_time": np.random.uniform(5, 15),
            },
            "inventory_management": {
                "inventory_levels": np.random.uniform(25000000, 75000000),
                "inventory_turnover_ratio": np.random.uniform(4, 10),
                "days_inventory_outstanding": np.random.uniform(30, 60),
            },
            "supply_chain": {
                "supplier_on_time_delivery_rate": np.random.uniform(0.8, 1),
                "supply_chain_costs_percentage": np.random.uniform(0.05, 0.15),
            },
            "quality_control": {
                "defect_rate": np.random.uniform(0.01, 0.05),
                "customer_return_rate": np.random.uniform(0.01, 0.03),
            },
        },
        "market_and_competitive_analysis": {
            "market_share": np.random.uniform(0.1, 0.4),
            "customer_acquisition_cost": np.random.uniform(500, 1500),
            "customer_lifetime_value": np.random.uniform(5000, 15000),
            "customer_satisfaction_score": np.random.uniform(80, 100),
        },
        "financial_health_and_risk": {
            "debt_to_equity_ratio": np.random.uniform(0.5, 1.5),
            "interest_coverage_ratio": np.random.uniform(2, 7),
            "altman_z_score": np.random.uniform(1.5, 3.5),
            "credit_rating": np.random.choice(['AA', 'A', 'BBB', 'BB', 'B']),
        },
        "investment_and_growth": {
            "capex": np.random.uniform(25000000, 75000000),
            "rd_spending": np.random.uniform(15000000, 45000000),
            "ma_activity": np.random.uniform(0, 100000000),
            "new_product_introduction_rate": np.random.uniform(0.05, 0.15),
        },
        "sustainability_and_compliance": {
            "carbon_footprint": np.random.uniform(500000, 1500000),
            "safety_incidents": np.random.randint(0, 10),
            "compliance_violations": np.random.randint(0, 5),
        },
    }

# Function to format currency
def format_currency(value):
    if abs(value) >= 1e9:
        return f"${value/1e9:.1f}B"
    elif abs(value) >= 1e6:
        return f"${value/1e6:.1f}M"
    elif abs(value) >= 1e3:
        return f"${value/1e3:.1f}K"
    else:
        return f"${value:.2f}"

# Function to format percentage
def format_percentage(value):
    return f"{value:.1%}"

# Function to create a metric card
def metric_card(title, value, format_func=lambda x: x):
    st.markdown(
        f"""
        <div style="
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            padding: 10px;
            text-align: center;
            height: 100px;
        ">
            <h3 style="font-size: 1em; color: #666;">{title}</h3>
            <p style="font-size: 1.5em; font-weight: bold;">{format_func(value)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Generate sample data
data = generate_sample_data()

# Dashboard title
st.title("CFO Dashboard")

# Sidebar for time frame selection
st.sidebar.title("Settings")
time_frame = st.sidebar.slider("Select Time Frame (months)", 1, 24, 12)

# Tabs for different sections
tabs = st.tabs([
    "Financial Performance",
    "Operational Efficiency",
    "Market & Competition",
    "Financial Health & Risk",
    "Investment & Growth",
    "Sustainability & Compliance"
])

# Financial Performance Tab
with tabs[0]:
    st.header("Financial Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Gross Profit Margin", data["financial_performance"]["profitability"]["gross_profit_margin"], format_percentage)
    with col2:
        metric_card("Net Profit Margin", data["financial_performance"]["profitability"]["net_profit_margin"], format_percentage)
    with col3:
        metric_card("Total Revenue", data["financial_performance"]["revenue"]["total"], format_currency)
    with col4:
        metric_card("EBITDA Margin", data["financial_performance"]["profitability"]["ebitda_margin"], format_percentage)
    
    col1, col2 = st.columns(2)
    with col1:
        # Revenue by Product Line pie chart
        fig_revenue = px.pie(
            values=list(data["financial_performance"]["revenue"]["by_product_line"].values()),
            names=list(data["financial_performance"]["revenue"]["by_product_line"].keys()),
            title="Revenue by Product Line"
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        # Cash Flow bar chart
        cash_flow_data = pd.DataFrame({
            "Cash Flow Type": ["Operating Cash Flow", "Free Cash Flow"],
            "Amount": [data["financial_performance"]["cash_flow"]["operating_cash_flow"],
                       data["financial_performance"]["cash_flow"]["free_cash_flow"]]
        })
        fig_cash_flow = px.bar(cash_flow_data, x="Cash Flow Type", y="Amount", title="Cash Flow Comparison")
        fig_cash_flow.update_traces(text=cash_flow_data["Amount"].apply(format_currency), textposition="outside")
        st.plotly_chart(fig_cash_flow, use_container_width=True)

# Operational Efficiency Tab
with tabs[1]:
    st.header("Operational Efficiency")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Capacity Utilization", data["operational_efficiency"]["production"]["capacity_utilization"], format_percentage)
    with col2:
        metric_card("OEE", data["operational_efficiency"]["production"]["oee"], format_percentage)
    with col3:
        metric_card("Inventory Turnover", data["operational_efficiency"]["inventory_management"]["inventory_turnover_ratio"], lambda x: f"{x:.2f}")
    with col4:
        metric_card("Defect Rate", data["operational_efficiency"]["quality_control"]["defect_rate"], format_percentage)
    
    col1, col2 = st.columns(2)
    with col1:
        # Supply Chain Performance
        supply_chain_data = pd.DataFrame({
            "Metric": ["Supplier On-Time Delivery", "Supply Chain Costs"],
            "Value": [data["operational_efficiency"]["supply_chain"]["supplier_on_time_delivery_rate"],
                      data["operational_efficiency"]["supply_chain"]["supply_chain_costs_percentage"]]
        })
        fig_supply_chain = px.bar(supply_chain_data, x="Metric", y="Value", title="Supply Chain Performance")
        fig_supply_chain.update_traces(text=supply_chain_data["Value"].apply(format_percentage), textposition="outside")
        st.plotly_chart(fig_supply_chain, use_container_width=True)
    
    with col2:
        # Inventory Management
        st.subheader("Inventory Management")
        metric_card("Inventory Levels", data["operational_efficiency"]["inventory_management"]["inventory_levels"], format_currency)
        metric_card("Days Inventory Outstanding", data["operational_efficiency"]["inventory_management"]["days_inventory_outstanding"], lambda x: f"{x:.0f} days")

# Market & Competition Tab
with tabs[2]:
    st.header("Market & Competitive Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Market Share", data["market_and_competitive_analysis"]["market_share"], format_percentage)
    with col2:
        metric_card("Customer Acquisition Cost", data["market_and_competitive_analysis"]["customer_acquisition_cost"], format_currency)
    with col3:
        metric_card("Customer Lifetime Value", data["market_and_competitive_analysis"]["customer_lifetime_value"], format_currency)
    with col4:
        metric_card("Customer Satisfaction", data["market_and_competitive_analysis"]["customer_satisfaction_score"], lambda x: f"{x:.1f}")

# Financial Health & Risk Tab
with tabs[3]:
    st.header("Financial Health & Risk")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Debt-to-Equity Ratio", data["financial_health_and_risk"]["debt_to_equity_ratio"], lambda x: f"{x:.2f}")
    with col2:
        metric_card("Interest Coverage Ratio", data["financial_health_and_risk"]["interest_coverage_ratio"], lambda x: f"{x:.2f}")
    with col3:
        metric_card("Altman Z-Score", data["financial_health_and_risk"]["altman_z_score"], lambda x: f"{x:.2f}")
    with col4:
        metric_card("Credit Rating", data["financial_health_and_risk"]["credit_rating"])

# Investment & Growth Tab
with tabs[4]:
    st.header("Investment & Growth")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("CAPEX", data["investment_and_growth"]["capex"], format_currency)
    with col2:
        metric_card("R&D Spending", data["investment_and_growth"]["rd_spending"], format_currency)
    with col3:
        metric_card("M&A Activity", data["investment_and_growth"]["ma_activity"], format_currency)
    with col4:
        metric_card("New Product Introduction Rate", data["investment_and_growth"]["new_product_introduction_rate"], format_percentage)

# Sustainability & Compliance Tab
with tabs[5]:
    st.header("Sustainability & Compliance")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Carbon Footprint", data["sustainability_and_compliance"]["carbon_footprint"], lambda x: f"{x:,.0f} tons CO2e")
    with col2:
        metric_card("Safety Incidents", data["sustainability_and_compliance"]["safety_incidents"])
    with col3:
        metric_card("Compliance Violations", data["sustainability_and_compliance"]["compliance_violations"])

# Note about data refresh
st.sidebar.info("Note: This dashboard uses randomly generated data. Refresh the page to see new data.")
