import praw
import yfinance as yf
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os

class DataCollector:
    def __init__(self):
        load_dotenv()
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        
    def get_reddit_posts(self, subreddit_name='teslamotors', limit=100):
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = subreddit.hot(limit=limit)
        return [post.title for post in posts]
    
    def get_stock_data(self, symbol='TSLA', period='30d'):
        stock = yf.Ticker(symbol)
        return stock.history(period=period, end=datetime.now())
    
    def collect_all_data(self, symbol='TSLA', period='30d', subreddit='teslamotors'):
        """Collect both stock and Reddit data"""
        stock_data = self.get_stock_data(symbol, period)
        reddit_posts = self.get_reddit_posts(subreddit)
        return stock_data, reddit_posts