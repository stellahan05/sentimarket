import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

@pytest.fixture
def sample_stock_data():
    """Create sample stock data for testing"""
    dates = pd.date_range(start='2024-01-01', periods=100)
    return pd.DataFrame({
        'Close': np.random.randn(100) * 100 + 1000,  # Realistic stock prices
        'Volume': np.random.randint(1000, 10000, 100),
        'time': dates
    })

@pytest.fixture
def sample_reddit_posts():
    """Create sample Reddit posts for testing"""
    return [
        "This stock is going to the moon! 🚀",
        "Terrible earnings report, selling everything",
        "Neutral news about the company",
        "Great product launch today!"
    ]

@pytest.fixture
def sample_merged_data():
    """Create sample merged data with sentiment"""
    dates = pd.date_range(start='2024-01-01', periods=100)
    return pd.DataFrame({
        'Close': np.random.randn(100) * 100 + 1000,
        'Volume': np.random.randint(1000, 10000, 100),
        'sentiment': np.random.randn(100) * 0.5,  # Sentiment scores between -1 and 1
        'time': dates
    })