from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        
    def analyze_posts(self, posts):
        sentiment_scores = []
        for post in posts:
            scores = self.analyzer.polarity_scores(post)
            sentiment_scores.append(scores['compound'])
        return sentiment_scores
    
    def create_sentiment_df(self, sentiment_scores, stock_data):
        sentiment_df = pd.DataFrame({
            'sentiment': sentiment_scores,
            'time': pd.date_range(start=stock_data.index[0], 
                                end=stock_data.index[-1], 
                                periods=len(sentiment_scores))
        })
        sentiment_df['time'] = sentiment_df['time'].dt.normalize()
        return sentiment_df.groupby('time')['sentiment'].mean().reset_index()
    
    def analyze_and_merge(self, stock_data, reddit_posts):
        """Complete sentiment analysis pipeline"""
        # Analyze sentiment
        sentiment_scores = self.analyze_posts(reddit_posts)
        
        # Create sentiment DataFrame
        sentiment_df = self.create_sentiment_df(sentiment_scores, stock_data)
        
        # Merge with stock data
        merged_df = pd.merge(stock_data.reset_index(), 
                           sentiment_df,
                           left_on='Date',
                           right_on='time',
                           how='inner')
        
        return merged_df