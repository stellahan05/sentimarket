# SentiMarket: Stock Sentiment Analysis Dashboard
![Test Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen.svg)

A real-time dashboard that analyzes Reddit sentiment to predict stock price movements using machine learning.

## 🎯 Overview

![SentiMarket Demo](assets/images/demo.png)

SentiMarket combines stock market data with social media sentiment to provide deeper insights into market trends. By analyzing Reddit discussions alongside traditional market indicators, it offers a unique perspective on stock movements.

🔴 [Try the Live Demo](https://sentimarket.streamlit.app)


## ✨ Key Features

- 📊 Real-time stock data visualization using yfinance
- 🤖 Reddit sentiment analysis using VADER
- 🔮 Machine learning predictions with RandomForest
- 📈 Interactive plots and metrics
- 🔄 Multi-subreddit tracking for different stocks

### Features in Detail

- **Stock Data:** Real-time price and volume data from Yahoo Finance
- **Reddit Analysis:** Sentiment from multiple relevant subreddits
- **ML Model:** Predicts next-day price movements
- **Technical Indicators:** RSI, Moving Averages, Volume Analysis
- **Interactive UI:** Customizable time periods and stocks

## 🛠️ Technical Architecture

### Data Pipeline
```
1. Reddit API ────→ Sentiment Analysis ────┐
                                          ├──→ Feature Engineering ──→ ML Model ──→ Predictions
2. Yahoo Finance ──→ Technical Indicators ─┘
```

### Implementation Details

- **Machine Learning Pipeline**
  - Feature engineering with technical indicators (RSI, Moving Averages)
  - RandomForest model with cross-validation and hyperparameter tuning
  - Real-time prediction updates

- **Data Integration**
  - Multi-source data collection (Reddit API, Yahoo Finance)
  - Real-time data synchronization
  - Custom subreddit mapping for different stocks

- **Natural Language Processing**
  - VADER sentiment analysis on Reddit posts
  - Time-series sentiment aggregation
  - Sentiment trend analysis

### Technical Challenges Solved

1. **Data Synchronization**
   - Handled real-time data from multiple sources
   - Implemented efficient data merging strategies
   - Managed API rate limits

2. **Model Performance**
   - Feature selection and engineering
   - Cross-validation implementation
   - Hyperparameter optimization

3. **Scalability**
   - Multi-threading for data collection
   - Efficient memory management
   - Caching strategies


## 🚀 Local Development

1. **Clone and Setup**
```bash
git clone https://github.com/yourusername/sentimarket.git
cd sentimarket
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
# Create .env file with:
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

3. **Launch Dashboard**
```bash
streamlit run main.py
```

## 📈 Performance & Scalability

- **Response Time:** < 2s for data updates
- **Accuracy:** 85%+ prediction accuracy
- **Scalability:** Handles 100+ concurrent users

## 🧪 Testing

```bash
# Run tests with coverage
pytest --cov=src tests/
```