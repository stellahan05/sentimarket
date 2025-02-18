import pytest
from src.data_collection import DataCollector
import pandas as pd
from unittest.mock import patch, MagicMock

# Mock Reddit credentials for all tests in this file
@pytest.fixture(autouse=True)
def mock_reddit_credentials():
    with patch.dict('os.environ', {
        'REDDIT_CLIENT_ID': 'fake_client_id',
        'REDDIT_CLIENT_SECRET': 'fake_client_secret',
        'REDDIT_USER_AGENT': 'fake_user_agent'
    }):
        yield

def test_data_collector_initialization():
    """Test if DataCollector initializes correctly"""
    with patch('praw.Reddit') as mock_reddit:
        collector = DataCollector()
        assert collector.reddit is not None
        assert isinstance(collector.stock_subreddits, dict)

@patch('praw.Reddit')
def test_get_relevant_subreddits(mock_reddit):
    """Test subreddit mapping for different stocks"""
    collector = DataCollector()
    
    # Test known stock
    tesla_subs = collector.get_relevant_subreddits('TSLA')
    assert 'teslamotors' in tesla_subs
    assert 'teslainvestorsclub' in tesla_subs
    
    # Test unknown stock falls back to default
    unknown_subs = collector.get_relevant_subreddits('UNKNOWN')
    assert 'stocks' in unknown_subs
    assert 'wallstreetbets' in unknown_subs

@patch('yfinance.Ticker')
def test_get_stock_data(mock_ticker):
    """Test stock data collection"""
    # Mock the stock data
    mock_history = pd.DataFrame({
        'Close': [100, 101, 102],
        'Volume': [1000, 1100, 1200],
    }, index=pd.date_range(start='2024-01-01', periods=3))
    
    mock_ticker.return_value.history.return_value = mock_history
    
    with patch('praw.Reddit') as mock_reddit:
        collector = DataCollector()
        stock_data = collector.get_stock_data('AAPL', period='3d')
        
        assert isinstance(stock_data, pd.DataFrame)
        assert 'Close' in stock_data.columns
        assert 'Volume' in stock_data.columns
        assert len(stock_data) == 3

@patch('praw.Reddit')
def test_get_reddit_posts(mock_reddit):
    """Test Reddit post collection"""
    # Mock Reddit posts
    mock_posts = []
    for i in range(3):
        post = MagicMock()
        post.title = f"Test post {i}"
        post.created_utc = 1677666000 + i*3600  # Some timestamp
        post.score = 100 + i
        mock_posts.append(post)
    
    mock_subreddit = MagicMock()
    mock_subreddit.search.return_value = mock_posts
    mock_reddit.return_value.subreddit.return_value = mock_subreddit
    
    collector = DataCollector()
    posts = collector.get_reddit_posts('AAPL', limit=3)
    
    assert isinstance(posts, list)
    assert len(posts) > 0
    assert all(isinstance(post, str) for post in posts)

def test_collect_all_data():
    """Test the complete data collection process"""
    with patch('praw.Reddit') as mock_reddit:
        with patch('src.data_collection.DataCollector.get_stock_data') as mock_stock:
            with patch('src.data_collection.DataCollector.get_reddit_posts') as mock_reddit_posts:
                # Mock stock data
                mock_stock.return_value = pd.DataFrame({
                    'Close': [100, 101, 102],
                    'Volume': [1000, 1100, 1200],
                }, index=pd.date_range(start='2024-01-01', periods=3))
                
                # Mock Reddit posts
                mock_reddit_posts.return_value = ["Post 1", "Post 2", "Post 3"]
                
                collector = DataCollector()
                stock_data, reddit_posts = collector.collect_all_data('AAPL', '3d')
                
                assert isinstance(stock_data, pd.DataFrame)
                assert isinstance(reddit_posts, list)
                assert len(stock_data) == 3
                assert len(reddit_posts) == 3

def test_error_handling():
    """Test error handling in data collection"""
    with patch('praw.Reddit') as mock_reddit:
        collector = DataCollector()
        
        # Test with invalid stock symbol
        with patch('src.data_collection.DataCollector.get_stock_data') as mock_stock:
            # Match the actual error message from your implementation
            mock_stock.side_effect = ValueError("No data found for symbol")
            
            with pytest.raises(ValueError):  # Remove specific message match
                collector.collect_all_data('THISISNOTAREALSTOCKSYMBOL', '1d')
