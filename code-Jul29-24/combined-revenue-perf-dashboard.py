import streamlit as st

# Import the dashboard modules

import streamlit as st

# Import the dashboard modules
from revenue_perf_pkg.revised_revenue_growth_dashboard import revenue_growth_component
from revenue_perf_pkg.cfo_financial_dashboard import margins_recurring_revenues
from overview_pkg.final_cfo_overview_dashboard_adjusted import cfo_financial_overview
from forecast_pkg.revenue_dashboard import revenue_forecast_dashboard
from forecast_pkg.expense_dashboard import expense_forecast_dashboard
from forecast_pkg.cashflow_dashboard import cashflow_forecast_dashboard
from forecast_pkg.balance_sheet_dashboard import balance_sheet_forecast_dashboard



# Set page config
st.set_page_config(page_title="CFO Margins & Recurring Revenues", layout="wide")

def main():
    st.title("Revenue Performance Dashboard")

    # Create tabs
#    tab1  = st.tabs( ["Revenue Growth Components"])
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7  = st.tabs(
        ["Financial Overview",
         "Revenue Growth", 
         "Margins & Recurring Rev",
         "Revenue Forecast", 
         "Expense Forecast", 
         "Cashflow Forecast",
         "Balance Sheet Forecast"
         ])



    # Revenue Forecast Tab
    with tab1:
        cfo_financial_overview()

    with tab2:
        revenue_growth_component()

    with tab3:
        margins_recurring_revenues()
        
         # Revenue Forecast Tab
    with tab4:
        revenue_forecast_dashboard()

    # Expense Forecast Tab
    with tab5:
        expense_forecast_dashboard()

    # Expense Forecast Tab
    with tab6:
        cashflow_forecast_dashboard()

 # Balance Sheet Forecast Tab
    with tab7:
        balance_sheet_forecast_dashboard()

    

if __name__ == "__main__":
    main()
