# SentiMarket: Stock Sentiment Analysis Dashboard

A real-time dashboard that analyzes Reddit sentiment to predict stock price movements using machine learning.

## Features

- 📊 Real-time stock data visualization
- 🤖 Reddit sentiment analysis using VADER
- 🔮 Machine learning predictions using Random Forest
- 📈 Interactive plots and metrics
- 🔄 Daily sentiment tracking

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sentimarket.git
cd sentimarket

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

## Usage

Run the dashboard:

```bash
streamlit run main.py
```

The dashboard will be available at `http://localhost:8501`