import pytest
from src.sentiment_analysis import SentimentAnalyzer
import pandas as pd

def test_sentiment_scoring():
    analyzer = SentimentAnalyzer()
    test_posts = ["This is great!", "This is terrible."]
    scores = analyzer.analyze_posts(test_posts)
    
    assert len(scores) == len(test_posts)
    assert all(-1 <= score <= 1 for score in scores)

def test_sentiment_analyzer_initialization():
    """Test analyzer initialization"""
    analyzer = SentimentAnalyzer()
    assert isinstance(analyzer, SentimentAnalyzer)

def test_analyze_posts():
    """Test sentiment analysis of posts"""
    analyzer = SentimentAnalyzer()
    posts = [
        "This is great news for the company! 🚀",
        "Terrible earnings report, stock will crash",
        "Not sure about this one, could go either way",
        "Amazing product launch today!"
    ]
    
    scores = analyzer.analyze_posts(posts)
    assert len(scores) == len(posts)
    assert all(-1 <= score <= 1 for score in scores)
    
    # Test empty posts list
    assert analyzer.analyze_posts([]) == []

def test_analyze_and_merge():
    """Test merging sentiment with stock data"""
    analyzer = SentimentAnalyzer()
    
    # Create sample data with index as dates
    dates = pd.date_range(start='2024-01-01', periods=3)
    stock_data = pd.DataFrame({
        'Date': dates,
        'Close': [100, 101, 102],
        'Volume': [1000, 1100, 1200]
    })
    stock_data.set_index('Date', inplace=True) 
    
    posts = [
        "Great news!",
        "Bad results",
        "Exciting development"
    ]
    
    # First check if analyze_posts works
    scores = analyzer.analyze_posts(posts)
    assert len(scores) == len(posts)
    
    # Then test the merge
    merged_df = analyzer.analyze_and_merge(stock_data, posts)
    assert 'sentiment' in merged_df.columns