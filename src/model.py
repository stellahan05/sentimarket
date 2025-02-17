from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

class SentimentPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        # Add more features
        self.features = [
            'sentiment',
            'sentiment_ma7',
            'sentiment_ma14',  # Longer-term sentiment
            'Volume',
            'volume_ma7',
            'price_ma7',
            'price_ma14',
            'rsi',            # Relative Strength Index
            'price_change',   # Daily price change
            'sentiment_change' # Daily sentiment change
        ]
        
    def prepare_features(self, merged_df):
        """Prepare features for model training and prediction"""
        df = merged_df.copy()
        
        # Technical indicators
        df['sentiment_ma7'] = df['sentiment'].rolling(window=7).mean()
        df['sentiment_ma14'] = df['sentiment'].rolling(window=14).mean()
        df['price_ma7'] = df['Close'].rolling(window=7).mean()
        df['price_ma14'] = df['Close'].rolling(window=14).mean()
        df['volume_ma7'] = df['Volume'].rolling(window=7).mean()
        
        # Price changes
        df['price_change'] = df['Close'].pct_change()
        df['sentiment_change'] = df['sentiment'].diff()
        
        # RSI (14-day)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Target variable
        df['next_day_return'] = df['Close'].pct_change().shift(-1)
        df['price_up'] = (df['next_day_return'] > 0).astype(int)
        
        # Drop NaN values
        df = df.dropna()
        
        # Select features and target
        X = df[self.features]
        y = df['price_up']
        
        return X, y
    
    def train(self, merged_df):
        """Train the model with cross-validation and hyperparameter tuning"""
        X, y = self.prepare_features(merged_df)
        
        if len(X) < 10:
            raise ValueError("Not enough data for training. Need at least 10 samples.")
        
        # Define parameter grid
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [5, 10, 15],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        # Perform grid search
        grid_search = GridSearchCV(
            RandomForestClassifier(random_state=42),
            param_grid,
            cv=5,
            scoring='accuracy',
            n_jobs=-1
        )
        
        grid_search.fit(X, y)
        self.model = grid_search.best_estimator_
        
        # Get cross-validation score
        cv_scores = cross_val_score(self.model, X, y, cv=5)
        
        return {
            'best_accuracy': grid_search.best_score_,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'best_params': grid_search.best_params_,
            'feature_importance': dict(zip(self.features, 
                                        self.model.feature_importances_))
        }
    
    def predict(self, merged_df):
        """Make prediction for the latest data point"""
        # Prepare features
        X, _ = self.prepare_features(merged_df)
        
        # Get the latest data point
        latest_features = X.iloc[-1:]
        
        # Make prediction
        return self.model.predict_proba(latest_features)[0]