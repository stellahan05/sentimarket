import pytest
from src.model import SentimentPredictor

def test_model_initialization():
    """Test if model initializes correctly"""
    predictor = SentimentPredictor()
    assert predictor.model is not None
    assert isinstance(predictor.features, list)

def test_prepare_features(sample_merged_data):
    """Test feature preparation"""
    predictor = SentimentPredictor()
    X, y = predictor.prepare_features(sample_merged_data)
    
    # Check if features are created correctly
    assert not X.isnull().any().any()
    assert all(feature in X.columns for feature in predictor.features)
    assert len(X) == len(y)

def test_model_training(sample_merged_data):
    """Test model training"""
    predictor = SentimentPredictor()
    metrics = predictor.train(sample_merged_data)
    
    # Check if metrics dictionary contains expected keys
    assert isinstance(metrics, dict)
    assert 'best_accuracy' in metrics
    assert 'cv_mean' in metrics
    assert 'cv_std' in metrics
    assert 'best_params' in metrics
    assert 'feature_importance' in metrics
    
    # Check if values are valid
    assert 0 <= metrics['best_accuracy'] <= 1
    assert 0 <= metrics['cv_mean'] <= 1
    assert isinstance(metrics['best_params'], dict)

def test_model_prediction(sample_merged_data):
    """Test model prediction"""
    predictor = SentimentPredictor()
    predictor.train(sample_merged_data)
    prediction = predictor.predict(sample_merged_data)
    
    assert len(prediction) == 2  # Binary classification probabilities
    assert 0 <= prediction[0] <= 1
    assert 0 <= prediction[1] <= 1
    assert abs(prediction[0] + prediction[1] - 1.0) < 1e-6  # Sum should be 1
