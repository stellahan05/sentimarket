import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st

def create_plots(merged_df):
    """Create all dashboard plots"""
    # Calculate moving averages
    merged_df['sentiment_ma7'] = merged_df['sentiment'].rolling(window=7).mean()
    merged_df['price_ma7'] = merged_df['Close'].rolling(window=7).mean()
    
    # Create tabs for different plots
    tab1, tab2, tab3 = st.tabs(["Main Chart", "Correlation Analysis", "Volume Analysis"])
    
    with tab1:
        plot_main_chart(merged_df)
    
    with tab2:
        plot_correlation_analysis(merged_df)
    
    with tab3:
        plot_volume_analysis(merged_df)

def plot_main_chart(merged_df):
    """Create main chart with sentiment and price"""
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add sentiment traces
    fig.add_trace(
        go.Scatter(
            x=merged_df['time'],
            y=merged_df['sentiment'],
            name="Daily Sentiment",
            line=dict(color='blue', width=1),
            opacity=0.5
        ),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(
            x=merged_df['time'],
            y=merged_df['sentiment_ma7'],
            name="7-day Sentiment MA",
            line=dict(color='blue', width=2, dash='dash')
        ),
        secondary_y=False,
    )
    
    # Add price traces
    fig.add_trace(
        go.Scatter(
            x=merged_df['time'],
            y=merged_df['Close'],
            name="Stock Price",
            line=dict(color='red', width=1),
            opacity=0.5
        ),
        secondary_y=True,
    )
    
    fig.add_trace(
        go.Scatter(
            x=merged_df['time'],
            y=merged_df['price_ma7'],
            name="7-day Price MA",
            line=dict(color='red', width=2, dash='dash')
        ),
        secondary_y=True,
    )
    
    # Update layout
    fig.update_layout(
        title="Stock Price vs Reddit Sentiment",
        xaxis_title="Date",
        hovermode="x unified"
    )
    
    # Update axes labels
    fig.update_yaxes(title_text="Sentiment Score", secondary_y=False)
    fig.update_yaxes(title_text="Stock Price ($)", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add statistics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Average Sentiment", f"{merged_df['sentiment'].mean():.3f}")
    with col2:
        st.metric("Price Change", 
                 f"{((merged_df['Close'].iloc[-1] / merged_df['Close'].iloc[0] - 1) * 100):.1f}%")

def plot_correlation_analysis(merged_df):
    """Create correlation analysis plots"""
    # Calculate rolling correlation
    rolling_corr = merged_df['sentiment'].rolling(window=7).corr(merged_df['Close'])
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=merged_df['time'],
            y=rolling_corr,
            name="7-day Rolling Correlation",
            line=dict(color='purple')
        )
    )
    
    fig.update_layout(
        title="Rolling Correlation between Sentiment and Price",
        xaxis_title="Date",
        yaxis_title="Correlation Coefficient",
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add correlation statistics
    st.write("### Correlation Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Overall Correlation", 
                 f"{merged_df['sentiment'].corr(merged_df['Close']):.3f}")
    with col2:
        st.metric("Recent Correlation (Last 7 Days)", 
                 f"{rolling_corr.iloc[-7:].mean():.3f}")

def plot_volume_analysis(merged_df):
    """Create volume analysis plots"""
    fig = make_subplots(rows=2, cols=1, 
                       subplot_titles=("Trading Volume", "Volume vs Sentiment"))
    
    # Volume over time
    fig.add_trace(
        go.Bar(
            x=merged_df['time'],
            y=merged_df['Volume'],
            name="Volume",
            marker_color='gray'
        ),
        row=1, col=1
    )
    
    # Volume vs Sentiment scatter
    fig.add_trace(
        go.Scatter(
            x=merged_df['sentiment'],
            y=merged_df['Volume'],
            mode='markers',
            name="Volume vs Sentiment",
            marker=dict(
                size=8,
                color=merged_df['Close'],
                colorscale='RdYlBu',
                showscale=True
            )
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        height=800,
        showlegend=False,
        hovermode="closest"
    )
    
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Sentiment Score", row=2, col=1)
    fig.update_yaxes(title_text="Volume", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add volume statistics
    st.write("### Volume Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Average Daily Volume", 
                 f"{merged_df['Volume'].mean():,.0f}")
    with col2:
        st.metric("Volume-Sentiment Correlation", 
                 f"{merged_df['Volume'].corr(merged_df['sentiment']):.3f}")

def add_annotations(fig, merged_df):
    """Add annotations for significant events"""
    # Find extreme sentiment days (beyond 2 standard deviations)
    sentiment_mean = merged_df['sentiment'].mean()
    sentiment_std = merged_df['sentiment'].std()
    significant_days = merged_df[
        (merged_df['sentiment'] > sentiment_mean + 2*sentiment_std) |
        (merged_df['sentiment'] < sentiment_mean - 2*sentiment_std)
    ]
    
    # Add annotations
    for idx, row in significant_days.iterrows():
        fig.add_annotation(
            x=row['time'],
            y=row['sentiment'],
            text=f"Extreme sentiment: {row['sentiment']:.2f}",
            showarrow=True,
            arrowhead=1,
        )
    
    return fig
