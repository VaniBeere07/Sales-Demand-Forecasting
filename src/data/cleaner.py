"""
Data Cleaner Module
Handles missing values, duplicates, and data quality issues
"""

import pandas as pd
import numpy as np
from loguru import logger

class DataCleaner:
    """Cleans and prepares sales data for analysis"""
    
    def __init__(self):
        self.cleaning_report = {}
        logger.info("DataCleaner initialized")
    
    def clean_sales_data(self, df):
        """
        Complete data cleaning pipeline
        """
        logger.info("Starting data cleaning process...")
        
        # Make a copy to avoid modifying original
        df_clean = df.copy()
        original_shape = df_clean.shape
        
        # Step 1: Remove duplicates
        duplicates_before = df_clean.duplicated().sum()
        df_clean = df_clean.drop_duplicates()
        duplicates_after = df_clean.duplicated().sum()
        if duplicates_before > 0:
            logger.info(f"Removed {duplicates_before} duplicate rows")
        
        # Step 2: Handle missing values
        missing_before = df_clean.isnull().sum().sum()
        df_clean = self._handle_missing_values(df_clean)
        missing_after = df_clean.isnull().sum().sum()
        if missing_before > 0:
            logger.info(f"Handled {missing_before - missing_after} missing values")
        
        # Step 3: Remove negative sales (if any)
        if 'Sales' in df_clean.columns:
            negative_sales = (df_clean['Sales'] < 0).sum()
            if negative_sales > 0:
                df_clean = df_clean[df_clean['Sales'] >= 0]
                logger.info(f"Removed {negative_sales} rows with negative sales")
        
        # Step 4: Remove outliers (optional - use IQR method)
        if 'Sales' in df_clean.columns and len(df_clean) > 0:
            df_clean = self._remove_outliers(df_clean, 'Sales')
        
        # Step 5: Ensure date column is datetime
        if 'Order Date' in df_clean.columns:
            df_clean['Order Date'] = pd.to_datetime(df_clean['Order Date'])
        
        final_shape = df_clean.shape
        logger.success(f"Cleaning complete: {original_shape} → {final_shape}")
        
        # Store cleaning report
        self.cleaning_report = {
            'original_rows': original_shape[0],
            'final_rows': final_shape[0],
            'rows_removed': original_shape[0] - final_shape[0]
        }
        
        return df_clean
    
    def _handle_missing_values(self, df):
        """Handle missing values based on column type"""
        df_clean = df.copy()
        
        for col in df_clean.columns:
            if df_clean[col].isnull().sum() > 0:
                if df_clean[col].dtype in ['float64', 'int64']:
                    # Fill numeric with median
                    median_val = df_clean[col].median()
                    df_clean[col].fillna(median_val, inplace=True)
                    logger.debug(f"Filled {col} missing values with median: {median_val:.2f}")
                else:
                    # Fill categorical with mode
                    mode_val = df_clean[col].mode()[0] if not df_clean[col].mode().empty else "Unknown"
                    df_clean[col].fillna(mode_val, inplace=True)
                    logger.debug(f"Filled {col} missing values with mode: {mode_val}")
        
        return df_clean
    
    def _remove_outliers(self, df, column, method='iqr'):
        """Remove outliers using IQR method"""
        if method == 'iqr' and len(df) > 0:
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            
            if IQR > 0:
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = ((df[column] < lower_bound) | (df[column] > upper_bound)).sum()
                if outliers > 0:
                    df_clean = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
                    logger.info(f"Removed {outliers} outliers from {column}")
                    return df_clean
        
        return df
    
    def get_cleaning_report(self):
        """Return summary of cleaning operations"""
        return self.cleaning_report