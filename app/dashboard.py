import streamlit as st
import pandas as pd
from src.data_collection import DataCollector
from src.sentiment_analysis import SentimentAnalyzer
from src.model import SentimentPredictor
from .plots import create_plots

def create_dashboard():
    # Initialize components
    collector = DataCollector()
    analyzer = SentimentAnalyzer()
    predictor = SentimentPredictor()
    
    # Sidebar controls
    st.sidebar.title("Controls")
    symbol = st.sidebar.text_input("Stock Symbol", "TSLA")
    days = st.sidebar.slider("Days of History", 7, 90, 30)
    
    try:
        # Collect data
        with st.spinner('Fetching data...'):
            stock_data, reddit_posts = collector.collect_all_data(
                symbol=symbol,
                period=f"{days}d"
            )
        
        # Analyze and merge data
        with st.spinner('Analyzing sentiment...'):
            merged_df = analyzer.analyze_and_merge(stock_data, reddit_posts)
            
        # Train model and show predictions
        with st.spinner('Training model...'):
            # Train the model
            accuracy = predictor.train(merged_df)
            st.sidebar.metric("Model Accuracy", f"{accuracy:.2%}")
            
            # Make prediction
            prediction = predictor.predict(merged_df)
            
            # Show prediction
            st.sidebar.metric(
                "Prediction for Tomorrow",
                "Up" if prediction[1] > 0.5 else "Down",
                f"Confidence: {max(prediction):.1%}"
            )
        
        # Create visualizations
        create_plots(merged_df)
        
        # Show raw data if requested
        if st.checkbox("Show raw data"):
            st.dataframe(merged_df)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")