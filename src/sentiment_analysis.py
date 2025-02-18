from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np

class SentimentAnalyzer:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
    
    def analyze_posts(self, posts):
        """Analyze sentiment of posts"""
        if posts is None:
            raise ValueError("Posts cannot be None")
        if not isinstance(posts, list):
            raise TypeError("Posts must be a list")
            
        sentiment_scores = []
        for post in posts:
            if not isinstance(post, str):
                raise TypeError("Each post must be a string")
            scores = self.vader.polarity_scores(post)
            sentiment_scores.append(scores['compound'])
        
        return sentiment_scores
    
    def analyze_and_merge(self, stock_data, posts):
        """Merge sentiment scores with stock data"""
        if stock_data is None or posts is None:
            raise ValueError("Stock data and posts cannot be None")
            
        # Calculate sentiment scores
        sentiment_scores = self.analyze_posts(posts)
        
        # Create sentiment DataFrame
        sentiment_df = pd.DataFrame({
            'Date': stock_data.index,
            'sentiment': np.mean(sentiment_scores)  # Use mean sentiment for each day
        })
        
        # Merge with stock data
        stock_data = stock_data.reset_index()
        stock_data.rename(columns={'index': 'Date'}, inplace=True)
        merged_df = pd.merge(stock_data, sentiment_df, on='Date', how='left')
        
        # Fill any missing sentiment values
        merged_df['sentiment'].fillna(method='ffill', inplace=True)
        
        return merged_df