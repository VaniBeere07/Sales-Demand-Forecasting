"""
Random Forest Forecasting Model
Ensemble method for sales prediction
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from loguru import logger
from .base_model import BaseModel

class RandomForestModel(BaseModel):
    """Random Forest implementation for sales forecasting"""
    
    def __init__(self, model_params=None):
        super().__init__('random_forest', model_params)
        self.scaler = StandardScaler()
        
        # Default parameters
        default_params = {
            'n_estimators': 100,
            'max_depth': 10,
            'min_samples_split': 5,
            'min_samples_leaf': 2,
            'random_state': 42,
            'n_jobs': -1
        }
        
        if model_params:
            default_params.update(model_params)
        
        self.model = RandomForestRegressor(**default_params)
        logger.info("Random Forest model initialized")
    
    def train(self, X_train, y_train):
        """Train the Random Forest model"""
        logger.info("Training Random Forest model...")
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        self.feature_names = X_train.columns.tolist()
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True
        
        logger.success("Random Forest training complete")
        
        # Feature importance
        importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        logger.info(f"Top 5 features:\n{importance.head(5)}")
        return importance
    
    def predict(self, X):
        """Make predictions"""
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def forecast_future(self, future_features):
        """Generate future forecast"""
        return self.predict(future_features)