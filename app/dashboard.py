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
        with st.spinner(f'Fetching data for {symbol}...'):
            stock_data, reddit_posts = collector.collect_all_data(
                symbol=symbol,
                period=f"{days}d"
            )
            
            # Show data source info
            st.sidebar.write("### Data Sources")
            st.sidebar.write(f"Subreddits analyzed: {', '.join(collector.get_relevant_subreddits(symbol))}")
            st.sidebar.write(f"Number of posts: {len(reddit_posts)}")
        
        # Analyze and merge data
        with st.spinner('Analyzing sentiment...'):
            merged_df = analyzer.analyze_and_merge(stock_data, reddit_posts)
            
        # Train model and show predictions
        with st.spinner('Training model...'):
            # Train the model
            metrics = predictor.train(merged_df)
            
            # Show metrics
            st.sidebar.write("### Model Performance")
            st.sidebar.metric("Best Accuracy", f"{metrics['best_accuracy']:.2%}")
            st.sidebar.metric("Cross-Val Mean", f"{metrics['cv_mean']:.2%}")
            st.sidebar.metric("Cross-Val Std", f"±{metrics['cv_std']:.2%}")
            
            # Show feature importance
            st.sidebar.write("### Feature Importance")
            importance_df = pd.DataFrame({
                'Feature': metrics['feature_importance'].keys(),
                'Importance': metrics['feature_importance'].values()
            }).sort_values('Importance', ascending=False)
            
            for _, row in importance_df.iterrows():
                st.sidebar.progress(row['Importance'], 
                                  text=f"{row['Feature']}: {row['Importance']:.3f}")
            
            # Make prediction
            prediction = predictor.predict(merged_df)
            
            # Show prediction with confidence
            pred_text = "Up" if prediction[1] > 0.5 else "Down"
            conf = max(prediction)
            st.sidebar.metric(
                "Tomorrow's Prediction",
                pred_text,
                f"Confidence: {conf:.1%}"
            )
        
        # Create visualizations
        create_plots(merged_df)
        
        # Show raw data if requested
        if st.checkbox("Show raw data"):
            st.dataframe(merged_df)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")