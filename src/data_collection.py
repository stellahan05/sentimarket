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
        
        # Map stock symbols to relevant subreddits
        self.stock_subreddits = {
            'TSLA': ['teslamotors', 'teslainvestorsclub'],
            'AAPL': ['apple', 'AAPL'],
            'GOOGL': ['google', 'alphabet'],
            'MSFT': ['microsoft', 'MicrosoftStock'],
            'META': ['facebook', 'metastock'],
            'AMZN': ['amazon', 'AmazonStock'],
            'NVDA': ['nvidia', 'NVDA_Stock'],
            'default': ['stocks', 'wallstreetbets']  # Default subreddits for any stock
        }
    
    def get_relevant_subreddits(self, symbol):
        """Get list of relevant subreddits for a stock symbol"""
        # Get specific subreddits for the symbol, or use default
        specific_subs = self.stock_subreddits.get(symbol, [])
        default_subs = self.stock_subreddits['default']
        
        return specific_subs + default_subs
    
    def get_reddit_posts(self, symbol='TSLA', limit=100):
        """Get posts from relevant subreddits for the given stock symbol"""
        subreddits = self.get_relevant_subreddits(symbol)
        all_posts = []
        
        for subreddit_name in subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                # Search for posts containing the stock symbol
                search_query = f"{symbol}"
                posts = subreddit.search(search_query, limit=limit//len(subreddits))
                
                for post in posts:
                    all_posts.append({
                        'title': post.title,
                        'subreddit': subreddit_name,
                        'created_utc': datetime.fromtimestamp(post.created_utc),
                        'score': post.score
                    })
            except Exception as e:
                print(f"Error fetching from r/{subreddit_name}: {str(e)}")
                continue
        
        # Convert to DataFrame for easier handling
        posts_df = pd.DataFrame(all_posts)
        if not posts_df.empty:
            posts_df = posts_df.sort_values('created_utc', ascending=False)
        
        return posts_df['title'].tolist() if not posts_df.empty else []
    
    def get_stock_data(self, symbol='TSLA', period='30d'):
        """Get stock price data"""
        stock = yf.Ticker(symbol)
        return stock.history(period=period, end=datetime.now())
    
    def collect_all_data(self, symbol='TSLA', period='30d'):
        """Collect both stock and Reddit data"""
        try:
            stock_data = self.get_stock_data(symbol, period)
            if stock_data.empty:
                raise ValueError(f"No stock data found for {symbol}")
            
            reddit_posts = self.get_reddit_posts(symbol)
            if not reddit_posts:
                raise ValueError(f"No Reddit posts found for {symbol}")
            
            return stock_data, reddit_posts
        except Exception as e:
            raise ValueError(f"Error collecting data for {symbol}: {str(e)}")