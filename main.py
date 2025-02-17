import streamlit as st
from src.data_collection import DataCollector
from src.sentiment_analysis import SentimentAnalyzer
from src.model import SentimentPredictor
from app.dashboard import create_dashboard
from app.plots import create_plots

def main():
    st.title("Stock Sentiment Analysis Dashboard")
    create_dashboard()

if __name__ == "__main__":
    main()