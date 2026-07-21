"""
Base Model Class
Abstract base class for all forecasting models
"""

from abc import ABC, abstractmethod
import pickle
import json
from pathlib import Path
from loguru import logger
import numpy as np

class BaseModel(ABC):
    """Abstract base class for forecasting models"""
    
    def __init__(self, name, model_params=None):
        self.name = name
        self.model_params = model_params or {}
        self.model = None
        self.is_trained = False
        self.feature_names = []
        self.metrics = {}
        logger.info(f"Initialized {name} model")
    
    @abstractmethod
    def train(self, X_train, y_train):
        """Train the model on data"""
        pass
    
    @abstractmethod
    def predict(self, X):
        """Make predictions"""
        pass
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate model performance
        """
        from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error, r2_score
        
        y_pred = self.predict(X_test)
        
        metrics = {
            'mae': mean_absolute_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mape': mean_absolute_percentage_error(y_test, y_pred) * 100,
            'r2': r2_score(y_test, y_pred)
        }
        
        # Calculate accuracy (100% - MAPE)
        metrics['accuracy'] = max(0, 100 - metrics['mape'])
        
        self.metrics = metrics
        return metrics
    
    def save(self, filepath=None):
        """Save model to disk"""
        if filepath is None:
            filepath = f"models/{self.name}.pkl"
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
        
        logger.info(f"Model saved to {filepath}")
        
        # Save metrics separately
        if self.metrics:
            metrics_path = filepath.replace('.pkl', '_metrics.json')
            with open(metrics_path, 'w') as f:
                json.dump(self.metrics, f, indent=2)
    
    def load(self, filepath):
        """Load model from disk"""
        with open(filepath, 'rb') as f:
            model = pickle.load(f)
        
        logger.info(f"Model loaded from {filepath}")
        return model