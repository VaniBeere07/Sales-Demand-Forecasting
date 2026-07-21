"""
Model Evaluation Module
Comprehensive metrics and validation for forecasting models
"""

import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error, r2_score
from sklearn.model_selection import TimeSeriesSplit
from loguru import logger
import matplotlib.pyplot as plt

class ModelEvaluator:
    """Evaluate and compare forecasting models"""
    
    def __init__(self):
        self.results = {}
        logger.info("ModelEvaluator initialized")
    
    def calculate_metrics(self, y_true, y_pred):
        """Calculate comprehensive set of metrics"""
        metrics = {
            'mae': mean_absolute_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'mape': mean_absolute_percentage_error(y_true, y_pred) * 100,
            'r2': r2_score(y_true, y_pred)
        }
        
        # Additional metrics
        mape_accuracy = 100 - metrics['mape']
        metrics['accuracy'] = max(0, mape_accuracy)
        
        # Calculate bias (mean of residuals)
        residuals = y_true - y_pred
        metrics['bias'] = np.mean(residuals)
        metrics['std_residuals'] = np.std(residuals)
        
        return metrics
    
    def evaluate_model(self, model, X_test, y_test, model_name=None):
        """Evaluate a single model"""
        logger.info(f"Evaluating {model_name or 'model'}...")
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        metrics = self.calculate_metrics(y_test, y_pred)
        
        # Store results
        name = model_name or model.name
        self.results[name] = metrics
        
        logger.success(f"{name}: MAE={metrics['mae']:.2f}, RMSE={metrics['rmse']:.2f}, MAPE={metrics['mape']:.2f}%")
        
        return metrics, y_pred
    
    def compare_models(self, models, X_test, y_test):
        """Compare multiple models"""
        logger.info("Comparing models...")
        
        for model in models:
            name = model.name
            self.evaluate_model(model, X_test, y_test, name)
        
        # Create comparison DataFrame
        comparison_df = pd.DataFrame(self.results).T
        comparison_df = comparison_df.sort_values('mae')
        
        logger.info("\nModel Comparison:")
        print(comparison_df)
        
        return comparison_df
    
    def time_series_cv(self, model, X, y, n_splits=5, verbose=True):
        """Time Series Cross Validation"""
        logger.info(f"Performing time series CV with {n_splits} splits...")
        
        tscv = TimeSeriesSplit(n_splits=n_splits)
        
        scores = []
        for fold, (train_idx, val_idx) in enumerate(tscv.split(X), 1):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
            
            # Train model
            model.train(X_train, y_train)
            
            # Evaluate
            metrics = model.evaluate(X_val, y_val)
            scores.append(metrics['mae'])
            
            if verbose:
                logger.info(f"Fold {fold}: MAE={metrics['mae']:.2f}")
        
        logger.info(f"Average CV MAE: {np.mean(scores):.2f} (+/- {np.std(scores):.2f})")
        
        return {
            'scores': scores,
            'mean': np.mean(scores),
            'std': np.std(scores)
        }
    
    def plot_comparison(self, comparison_df, metric='mae'):
        """Visualize model comparison"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        comparison_df[metric].sort_values().plot(kind='bar', ax=ax)
        ax.set_title(f'Model Comparison - {metric.upper()}')
        ax.set_xlabel('Model')
        ax.set_ylabel(metric.upper())
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig