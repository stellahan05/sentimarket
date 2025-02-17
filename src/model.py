from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

class SentimentPredictor:
    def __init__(self):
        self.model = RandomForestClassifier()
        self.features = ['sentiment', 'sentiment_ma7', 'Volume', 'price_ma7']
        
    def prepare_features(self, merged_df):
        """Prepare features for model training and prediction"""
        # Create a copy to avoid modifying the original
        df = merged_df.copy()
        
        # Create features
        df['sentiment_ma7'] = df['sentiment'].rolling(window=7).mean()
        df['price_ma7'] = df['Close'].rolling(window=7).mean()
        df['next_day_return'] = df['Close'].pct_change().shift(-1)
        
        # Create target
        df['price_up'] = (df['next_day_return'] > 0).astype(int)
        
        # Drop any rows with NaN values
        df = df.dropna()
        
        # Select features and target
        X = df[self.features]
        y = df['price_up']
        
        return X, y
    
    def train(self, merged_df):
        """Train the model and return accuracy"""
        # Prepare features and target
        X, y = self.prepare_features(merged_df)

        # Check if we have enough data
        if len(X) < 10:  # Minimum required samples
            raise ValueError("Not enough data for training. Need at least 10 samples.")
        
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # Fit the model
        self.model.fit(X_train, y_train)
        
        return self.model.score(X_test, y_test)
    
    def predict(self, merged_df):
        """Make prediction for the latest data point"""
        # Prepare features
        X, _ = self.prepare_features(merged_df)
        
        # Get the latest data point
        latest_features = X.iloc[-1:]
        
        # Make prediction
        return self.model.predict_proba(latest_features)[0]