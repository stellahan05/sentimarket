# SentiMarket: Stock Sentiment Analysis Dashboard

A real-time dashboard that analyzes Reddit sentiment to predict stock price movements using machine learning.

## 🔴 [Live Demo](https://sentimarket.streamlit.app)

## Features

- 📊 Real-time stock data visualization using yfinance
- 🤖 Reddit sentiment analysis using VADER
- 🔮 Machine learning predictions with RandomForest
- 📈 Interactive plots and metrics
- 🔄 Multi-subreddit tracking for different stocks

## Tech Stack

- **Data Collection:** PRAW (Reddit API), yfinance
- **Analysis:** VADER Sentiment, scikit-learn
- **Visualization:** Plotly
- **Deployment:** Streamlit Cloud

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sentimarket.git
cd sentimarket
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Create a `.env` file in the root directory
- Add your Reddit API credentials:
```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

5. Run the dashboard:   
```bash
streamlit run main.py
```

## Features in Detail

- **Stock Data:** Real-time price and volume data from Yahoo Finance
- **Reddit Analysis:** Sentiment from multiple relevant subreddits
- **ML Model:** Predicts next-day price movements
- **Technical Indicators:** RSI, Moving Averages, Volume Analysis
- **Interactive UI:** Customizable time periods and stocks