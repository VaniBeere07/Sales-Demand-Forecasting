"""
Feature Engineering Module
Creates time-based features for forecasting
"""

import pandas as pd
import numpy as np
from loguru import logger

class FeatureEngineer:
    """Creates features for time series forecasting"""
    
    def __init__(self):
        self.feature_columns = []
        logger.info("FeatureEngineer initialized")
    
    def create_time_features(self, df, date_column='Order Date'):
        """
        Create comprehensive time-based features
        """
        logger.info("Creating time features...")
        df_featured = df.copy()
        
        # Extract date components
        df_featured['year'] = df_featured[date_column].dt.year
        df_featured['month'] = df_featured[date_column].dt.month
        df_featured['quarter'] = df_featured[date_column].dt.quarter
        df_featured['day_of_year'] = df_featured[date_column].dt.dayofyear
        df_featured['day_of_month'] = df_featured[date_column].dt.day
        df_featured['day_of_week'] = df_featured[date_column].dt.dayofweek
        df_featured['week_of_year'] = df_featured[date_column].dt.isocalendar().week
        
        # Weekend flag
        df_featured['is_weekend'] = (df_featured['day_of_week'] >= 5).astype(int)
        
        # Day name for readability
        df_featured['day_name'] = df_featured[date_column].dt.day_name()
        
        # Month name
        df_featured['month_name'] = df_featured[date_column].dt.month_name()
        
        # Is beginning/end of month
        df_featured['is_month_start'] = df_featured[date_column].dt.is_month_start.astype(int)
        df_featured['is_month_end'] = df_featured[date_column].dt.is_month_end.astype(int)
        
        # Seasonal features (sine/cosine transformations for seasonality)
        df_featured['month_sin'] = np.sin(2 * np.pi * df_featured['month'] / 12)
        df_featured['month_cos'] = np.cos(2 * np.pi * df_featured['month'] / 12)
        df_featured['day_sin'] = np.sin(2 * np.pi * df_featured['day_of_week'] / 7)
        df_featured['day_cos'] = np.cos(2 * np.pi * df_featured['day_of_week'] / 7)
        
        # Store feature columns
        self.feature_columns = [col for col in df_featured.columns if col not in 
                               ['Order Date', 'Sales', 'Quantity', 'day_name', 'month_name']]
        
        logger.success(f"Created {len(self.feature_columns)} time-based features")
        return df_featured
    
    def aggregate_daily_sales(self, df, date_column='Order Date', sales_column='Sales'):
        """
        Aggregate sales to daily level for time series analysis
        """
        logger.info("Aggregating to daily sales...")
        
        # Check if Quantity column exists
        if 'Quantity' in df.columns:
            daily = df.groupby(date_column).agg({
                sales_column: 'sum',
                'Quantity': 'sum'
            }).reset_index()
        else:
            daily = df.groupby(date_column).agg({
                sales_column: 'sum'
            }).reset_index()
            daily['Quantity'] = 1  # Placeholder
        
        # Rename columns
        daily.columns = [date_column, 'Sales', 'Quantity']
        
        # Add back time features
        daily = self.create_time_features(daily, date_column)
        
        logger.success(f"Created daily sales data: {len(daily)} days")
        return daily
    
    def aggregate_monthly_sales(self, df, date_column='Order Date', sales_column='Sales'):
        """Aggregate to monthly level"""
        df_copy = df.copy()
        df_copy['month'] = df_copy[date_column].dt.to_period('M')
        
        if 'Quantity' in df_copy.columns:
            monthly = df_copy.groupby('month').agg({
                sales_column: 'sum',
                'Quantity': 'sum'
            }).reset_index()
        else:
            monthly = df_copy.groupby('month').agg({
                sales_column: 'sum'
            }).reset_index()
            monthly['Quantity'] = 1
        
        monthly['month'] = monthly['month'].dt.to_timestamp()
        monthly.columns = ['Order Date', 'Sales', 'Quantity']
        
        return monthly
    
    def create_lag_features(self, df, target_column='Sales', lags=[1, 7, 14, 30]):
        """
        Create lag features for time series
        """
        logger.info(f"Creating lag features: {lags}")
        df_lagged = df.copy()
        
        for lag in lags:
            df_lagged[f'sales_lag_{lag}'] = df_lagged[target_column].shift(lag)
        
        # Create rolling statistics
        for window in [7, 14, 30]:
            if len(df_lagged) > window:
                df_lagged[f'sales_rolling_mean_{window}'] = df_lagged[target_column].rolling(window).mean()
                df_lagged[f'sales_rolling_std_{window}'] = df_lagged[target_column].rolling(window).std()
        
        # Remove rows with NaN (from lags)
        df_lagged = df_lagged.dropna()
        
        logger.success(f"Created lag features and rolling statistics")
        return df_lagged
    
    def prepare_features_for_model(self, daily_df):
        """
        Prepare features for model training
        """
        # Get features (exclude non-numeric and target)
        exclude_cols = ['Order Date', 'Sales', 'Quantity', 'day_name', 'month_name']
        feature_cols = [col for col in daily_df.columns if col not in exclude_cols]
        
        X = daily_df[feature_cols]
        y = daily_df['Sales']
        
        # Split data
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        logger.info(f"Training set: {len(X_train)} samples")
        logger.info(f"Test set: {len(X_test)} samples")
        
        return X_train, X_test, y_train, y_test, feature_cols

# Test the feature engineer
if __name__ == "__main__":
    from src.data.loader import DataLoader
    from src.data.cleaner import DataCleaner
    
    loader = DataLoader()
    df = loader.load_data_with_date_parsing()
    
    cleaner = DataCleaner()
    clean_df = cleaner.clean_sales_data(df)
    
    engineer = FeatureEngineer()
    daily_df = engineer.aggregate_daily_sales(clean_df)
    
    print(f"\nDaily sales data shape: {daily_df.shape}")
    print(daily_df.head())
    print(f"\nFeature columns: {engineer.feature_columns[:5]}...")