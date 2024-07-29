import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def generate_sample_data():
    """
    Generate sample data for revenue growth components over 5 quarters.
    
    Returns:
        pd.DataFrame: DataFrame containing the sample data.
    """
    components = [
        'Organic growth - Tires',
        'Organic growth - Auto parts',
        'New product introductions',
        'Geographic expansion',
        'E-commerce growth',
        'Channel partner expansion',
        'Manufacturer relationships',
        'Value-added services',
        'Marketing initiatives',
        'Mergers and acquisitions',
        'Price optimization',
        'Foreign exchange impact'
    ]

    quarters = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025']

    data = []
    for quarter in quarters:
        quarter_data = {'quarter': quarter}
        for component in components:
            value = np.random.uniform(-2, 5) if component == 'Foreign exchange impact' else np.random.uniform(0, 5)
            quarter_data[component] = value
        data.append(quarter_data)

    return pd.DataFrame(data)

def create_stacked_area_chart(data):
    """
    Create a stacked area chart using Plotly.
    
    Args:
        data (pd.DataFrame): DataFrame containing the data.
    
    Returns:
        go.Figure: Plotly figure object for the stacked area chart.
    """
    fig = go.Figure()
    components = [col for col in data.columns if col != 'quarter']
    
    for component in components:
        fig.add_trace(go.Scatter(
            x=data['quarter'], 
            y=data[component], 
            name=component,
            mode='lines',
            stackgroup='one',
            groupnorm='percent'
        ))
    
    fig.update_layout(
        title={
            'text': 'Revenue Growth Components Over Time',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Quarter',
        yaxis_title='Percentage',
        legend_title='Components',
        hovermode='x unified',
        margin=dict(l=0, r=0, t=50, b=0),
        height=400
    )
    
    return fig

def create_heatmap_table(data):
    """
    Create a heatmap table using Plotly.
    
    Args:
        data (pd.DataFrame): DataFrame containing the data.
    
    Returns:
        go.Figure: Plotly figure object for the heatmap table.
    """
    heatmap_data = data.set_index('quarter').T
    
    heatmap_data_formatted = heatmap_data.map(lambda x: f'{x:.2f}%')
    
    table = go.Figure(data=[go.Table(
        header=dict(values=['Component'] + list(heatmap_data.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[heatmap_data_formatted.index] + [heatmap_data_formatted[col] for col in heatmap_data_formatted.columns],
                   align='left'))
    ])
    
    table.update_layout(
        title={
            'text': 'Revenue Growth Heatmap',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        margin=dict(l=0, r=0, t=50, b=0),
        height=400
    )
    
    return table, heatmap_data

def color_heatmap_cells(fig, heatmap_data):
    """
    Color the cells of the heatmap table.
    
    Args:
        fig (go.Figure): Plotly figure object for the table.
        heatmap_data (pd.DataFrame): DataFrame containing the numeric data.
    """
    def get_color(value):
        hue = ((value + 5) / 10) * 120  # Map -5 to 5 to 0 to 120 (red to green)
        return f'hsl({hue}, 70%, 50%)'
    
    for i, col in enumerate(heatmap_data.columns):
        colors = [get_color(val) for val in heatmap_data[col]]
        fig.update_traces(cells=dict(fill_color=['white'] + colors))
    
    return fig

def create_bar_chart(data):
    """
    Create a bar chart for the latest quarter using Plotly.
    
    Args:
        data (pd.DataFrame): DataFrame containing the data.
    
    Returns:
        go.Figure: Plotly figure object for the bar chart.
    """
    latest_quarter = data.iloc[-1].drop('quarter')
    fig = px.bar(x=latest_quarter.index, y=latest_quarter.values,
                 labels={'x': 'Component', 'y': 'Percentage'})
    fig.update_layout(
        title={
            'text': f'Latest Quarter ({data.iloc[-1]["quarter"]}) Revenue Growth Breakdown',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_tickangle=-45,
        margin=dict(l=0, r=0, t=50, b=0),
        height=400
    )
    return fig

def revenue_growth_component():
    """
    Main function to create the Revenue Growth Component dashboard.
    This function serves as an entry point for the dashboard tab.
    """
    st.title("Revenue Growth Dashboard")

    # Generate sample data
    data = generate_sample_data()

    # Create and display stacked area chart
    with st.container():
        st.plotly_chart(create_stacked_area_chart(data), use_container_width=True)

    # Create and display heatmap
    with st.container():
        heatmap_table, heatmap_data = create_heatmap_table(data)
        colored_heatmap = color_heatmap_cells(heatmap_table, heatmap_data)
        st.plotly_chart(colored_heatmap, use_container_width=True)

    # Create and display bar chart for the latest quarter
    with st.container():
        st.plotly_chart(create_bar_chart(data), use_container_width=True)

if __name__ == "__main__":
    revenue_growth_component()
