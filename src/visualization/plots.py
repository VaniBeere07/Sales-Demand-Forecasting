"""
Visualization Module
Creates business-friendly plots and charts
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from loguru import logger
import matplotlib.dates as mdates

class SalesVisualizer:
    """Creates visualizations for sales forecasting"""
    
    def __init__(self, style='seaborn-v0_8-darkgrid'):
        self.style = style
        plt.style.use(style)
        logger.info("SalesVisualizer initialized")
    
    def plot_sales_trend(self, df, date_column='Order Date', sales_column='Sales', title="Sales Trend Over Time"):
        """Plot sales trend over time"""
        fig, ax = plt.subplots(figsize=(14, 6))
        
        ax.plot(df[date_column], df[sales_column], linewidth=2, color='blue')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Sales ($)')
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        return fig
    
    def plot_seasonality(self, df, date_column='Order Date', sales_column='Sales'):
        """Plot seasonality patterns"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. Monthly seasonality
        monthly = df.groupby(df[date_column].dt.month)[sales_column].mean()
        axes[0, 0].bar(monthly.index, monthly.values, color='skyblue')
        axes[0, 0].set_title('Average Sales by Month')
        axes[0, 0].set_xlabel('Month')
        axes[0, 0].set_ylabel('Average Sales ($)')
        
        # 2. Day of week seasonality
        dow = df.groupby(df[date_column].dt.dayofweek)[sales_column].mean()
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        axes[0, 1].bar(days, dow.values, color='coral')
        axes[0, 1].set_title('Average Sales by Day of Week')
        axes[0, 1].set_xlabel('Day')
        axes[0, 1].set_ylabel('Average Sales ($)')
        
        # 3. Quarterly seasonality
        quarterly = df.groupby(df[date_column].dt.quarter)[sales_column].mean()
        axes[1, 0].bar(quarterly.index, quarterly.values, color='lightgreen')
        axes[1, 0].set_title('Average Sales by Quarter')
        axes[1, 0].set_xlabel('Quarter')
        axes[1, 0].set_ylabel('Average Sales ($)')
        
        # 4. Year over year comparison
        df['year'] = df[date_column].dt.year
        pivot = df.pivot_table(values=sales_column, index=df[date_column].dt.month, columns='year', aggfunc='mean')
        pivot.plot(ax=axes[1, 1], marker='o')
        axes[1, 1].set_title('Year-over-Year Comparison')
        axes[1, 1].set_xlabel('Month')
        axes[1, 1].set_ylabel('Average Sales ($)')
        axes[1, 1].legend(title='Year')
        
        plt.tight_layout()
        return fig
    
    def plot_forecast(self, actual_df, forecast_df, actual_col='Sales', forecast_col='Predicted_Sales'):
        """Plot actual vs forecast"""
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Plot actual
        ax.plot(actual_df['Order Date'], actual_df[actual_col], 
                label='Actual Sales', linewidth=2, color='blue')
        
        # Plot forecast
        ax.plot(forecast_df['Date'], forecast_df[forecast_col], 
                label='Forecast', linewidth=2, color='red', linestyle='--')
        
        ax.set_title('Sales Forecast vs Actual', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Sales ($)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_model_performance(self, y_true, y_pred, title="Model Performance"):
        """Plot model performance metrics"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 1. Actual vs Predicted
        axes[0, 0].scatter(y_true, y_pred, alpha=0.5)
        axes[0, 0].plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 
                       'r--', linewidth=2)
        axes[0, 0].set_title('Actual vs Predicted')
        axes[0, 0].set_xlabel('Actual Sales')
        axes[0, 0].set_ylabel('Predicted Sales')
        
        # 2. Residuals
        residuals = y_true - y_pred
        axes[0, 1].scatter(y_pred, residuals, alpha=0.5)
        axes[0, 1].axhline(y=0, color='r', linestyle='--')
        axes[0, 1].set_title('Residuals vs Predicted')
        axes[0, 1].set_xlabel('Predicted Sales')
        axes[0, 1].set_ylabel('Residuals')
        
        # 3. Residual distribution
        axes[1, 0].hist(residuals, bins=30, edgecolor='black', alpha=0.7)
        axes[1, 0].axvline(x=0, color='r', linestyle='--')
        axes[1, 0].set_title('Residual Distribution')
        axes[1, 0].set_xlabel('Residuals')
        axes[1, 0].set_ylabel('Frequency')
        
        # 4. Percentage errors
        pct_errors = ((y_true - y_pred) / y_true) * 100
        axes[1, 1].hist(pct_errors, bins=30, edgecolor='black', alpha=0.7)
        axes[1, 1].axvline(x=0, color='r', linestyle='--')
        axes[1, 1].set_title('Percentage Error Distribution')
        axes[1, 1].set_xlabel('Error (%)')
        axes[1, 1].set_ylabel('Frequency')
        
        plt.suptitle(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        return fig
    
    def save_figure(self, fig, filename, dpi=150):
        """Save figure to file"""
        fig.savefig(f'reports/figures/{filename}', dpi=dpi, bbox_inches='tight')
        logger.info(f"Figure saved: reports/figures/{filename}")