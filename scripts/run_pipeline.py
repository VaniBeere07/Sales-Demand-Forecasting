#!/usr/bin/env python
"""
Complete pipeline runner for sales forecasting
Run this script to execute the entire forecasting pipeline
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from loguru import logger
from src.data.loader import DataLoader
from src.data.cleaner import DataCleaner
from src.data.feature_engineering import FeatureEngineer
from src.models.random_forest import RandomForestModel
from src.evaluation.metrics import ModelEvaluator
from src.visualization.plots import SalesVisualizer
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def main():
    """Run complete pipeline"""
    logger.info("="*60)
    logger.info("SALES FORECASTING PIPELINE")
    logger.info("="*60)
    
    try:
        # 1. Load configuration
        logger.info("\n📁 1. Loading data...")
        loader = DataLoader()
        df = loader.load_data_with_date_parsing()
        print(f"   ✅ Loaded {len(df):,} records")
        
        # 2. Clean data
        logger.info("\n🧹 2. Cleaning data...")
        cleaner = DataCleaner()
        clean_df = cleaner.clean_sales_data(df)
        print(f"   ✅ Cleaned data: {len(clean_df):,} records")
        print(f"   📊 Cleaning report: {cleaner.get_cleaning_report()}")
        
        # 3. Feature engineering
        logger.info("\n🔧 3. Engineering features...")
        engineer = FeatureEngineer()
        daily_df = engineer.aggregate_daily_sales(clean_df)
        print(f"   ✅ Created daily aggregation: {len(daily_df)} days")
        print(f"   📊 Features created: {len(engineer.feature_columns)}")
        
        # 4. Prepare features for model
        logger.info("\n📊 4. Preparing features...")
        X_train, X_test, y_train, y_test, feature_cols = engineer.prepare_features_for_model(daily_df)
        print(f"   ✅ Training set: {len(X_train)} samples")
        print(f"   ✅ Test set: {len(X_test)} samples")
        
        # 5. Train Random Forest model
        logger.info("\n🤖 5. Training Random Forest model...")
        rf_model = RandomForestModel()
        feature_importance = rf_model.train(X_train, y_train)
        print(f"   ✅ Model training complete")
        print(f"   📊 Top features:")
        for i, row in feature_importance.head(3).iterrows():
            print(f"      - {row['feature']}: {row['importance']*100:.1f}%")
        
        # 6. Evaluate model
        logger.info("\n📈 6. Evaluating model...")
        evaluator = ModelEvaluator()
        metrics, y_pred = evaluator.evaluate_model(rf_model, X_test, y_test)
        print(f"   ✅ MAE: ${metrics['mae']:,.2f}")
        print(f"   ✅ RMSE: ${metrics['rmse']:,.2f}")
        print(f"   ✅ MAPE: {metrics['mape']:.2f}%")
        print(f"   ✅ Accuracy: {metrics['accuracy']:.2f}%")
        
        # 7. Generate future forecast (next 90 days)
        logger.info("\n🔮 7. Generating 90-day forecast...")
        future_forecast = generate_future_forecast(rf_model, daily_df, engineer, days=90)
        print(f"   ✅ Generated forecast for {len(future_forecast)} days")
        print(f"   📊 Total predicted sales: ${future_forecast['Predicted_Sales'].sum():,.2f}")
        print(f"   📊 Average daily sales: ${future_forecast['Predicted_Sales'].mean():,.2f}")
        
        # 8. Create visualizations
        logger.info("\n📊 8. Creating visualizations...")
        visualizer = SalesVisualizer()
        
        # Create figures directory if it doesn't exist
        Path("reports/figures").mkdir(parents=True, exist_ok=True)
        
        # Plot sales trend
        fig1 = visualizer.plot_sales_trend(daily_df)
        visualizer.save_figure(fig1, 'sales_trend.png')
        print("   ✅ Saved: sales_trend.png")
        
        # Plot seasonality
        fig2 = visualizer.plot_seasonality(daily_df)
        visualizer.save_figure(fig2, 'seasonality.png')
        print("   ✅ Saved: seasonality.png")
        
        # Plot model performance
        fig3 = visualizer.plot_model_performance(y_test, y_pred)
        visualizer.save_figure(fig3, 'model_performance.png')
        print("   ✅ Saved: model_performance.png")
        
        # Plot forecast
        fig4 = visualizer.plot_forecast(daily_df, future_forecast)
        visualizer.save_figure(fig4, 'forecast.png')
        print("   ✅ Saved: forecast.png")
        
        # 9. Save results
        logger.info("\n💾 9. Saving results...")
        
        # Save forecast
        Path("data/forecasts").mkdir(parents=True, exist_ok=True)
        future_forecast.to_csv('data/forecasts/90_day_forecast.csv', index=False)
        print("   ✅ Saved: data/forecasts/90_day_forecast.csv")
        
        # Save model
        Path("models").mkdir(parents=True, exist_ok=True)
        rf_model.save()
        print("   ✅ Saved: models/random_forest.pkl")
        
        # Save feature importance
        Path("reports").mkdir(parents=True, exist_ok=True)
        feature_importance.to_csv('reports/feature_importance.csv', index=False)
        print("   ✅ Saved: reports/feature_importance.csv")
        
        # 10. Generate business report
        logger.info("\n📄 10. Generating business report...")
        generate_business_report(daily_df, future_forecast, metrics, feature_importance)
        print("   ✅ Saved: reports/business_report.txt")
        
        logger.info("\n" + "="*60)
        logger.success("✅ PIPELINE COMPLETED SUCCESSFULLY!")
        logger.info("="*60)
        
        # Print final summary
        print("\n" + "="*60)
        print("📊 FORECASTING SUMMARY")
        print("="*60)
        print(f"✅ Model: Random Forest")
        print(f"✅ MAE: ${metrics['mae']:,.2f}")
        print(f"✅ RMSE: ${metrics['rmse']:,.2f}")
        print(f"✅ MAPE: {metrics['mape']:.2f}%")
        print(f"✅ Accuracy: {metrics['accuracy']:.2f}%")
        print(f"✅ Total predicted sales (90 days): ${future_forecast['Predicted_Sales'].sum():,.2f}")
        print(f"✅ Average daily sales (forecast): ${future_forecast['Predicted_Sales'].mean():,.2f}")
        print("="*60)
        
        print("\n📁 Output files saved:")
        print("  📊 data/forecasts/90_day_forecast.csv")
        print("  🤖 models/random_forest.pkl")
        print("  📈 reports/figures/*.png")
        print("  📄 reports/feature_importance.csv")
        print("  📄 reports/business_report.txt")
        
    except Exception as e:
        logger.error(f"❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        raise

def generate_future_forecast(model, daily_df, engineer, days=90):
    """
    Generate future sales forecast
    """
    # Create future dates
    last_date = daily_df['Order Date'].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=days)
    
    # Create feature dataframe for future
    future_df = pd.DataFrame({'Order Date': future_dates})
    
    # Add time features
    future_df = engineer.create_time_features(future_df)
    
    # Prepare features
    exclude_cols = ['Order Date', 'Sales', 'Quantity', 'day_name', 'month_name']
    feature_cols = [col for col in future_df.columns if col not in exclude_cols]
    X_future = future_df[feature_cols]
    
    # Make predictions
    future_predictions = model.predict(X_future)
    
    # Create result dataframe
    forecast_df = pd.DataFrame({
        'Date': future_dates,
        'Predicted_Sales': future_predictions
    })
    
    # Add business insights
    forecast_df['Week'] = forecast_df['Date'].dt.isocalendar().week
    forecast_df['Day_Name'] = forecast_df['Date'].dt.day_name()
    forecast_df['Month'] = forecast_df['Date'].dt.month_name()
    forecast_df['Quarter'] = forecast_df['Date'].dt.quarter
    
    return forecast_df

def generate_business_report(daily_df, future_forecast, metrics, feature_importance):
    """
    Generate business-friendly report
    """
    report = []
    report.append("="*60)
    report.append("           BUSINESS FORECASTING REPORT")
    report.append("="*60)
    report.append("")
    
    report.append("FORECAST ACCURACY")
    report.append("-"*40)
    report.append(f"Mean Absolute Error (MAE):     ${metrics['mae']:,.2f}")
    report.append(f"Root Mean Square Error (RMSE): ${metrics['rmse']:,.2f}")
    report.append(f"Mean Absolute % Error (MAPE):  {metrics['mape']:.2f}%")
    report.append(f"Forecast Accuracy:              {metrics['accuracy']:.2f}%")
    report.append("")
    
    report.append("KEY BUSINESS INSIGHTS")
    report.append("-"*40)
    
    # Seasonality insights
    monthly_avg = daily_df.groupby('month')['Sales'].mean()
    best_month = monthly_avg.idxmax()
    worst_month = monthly_avg.idxmin()
    
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                   5: 'May', 6: 'June', 7: 'July', 8: 'August',
                   9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    
    report.append(f"* Best performing month: {month_names[best_month]}")
    report.append(f"* Worst performing month: {month_names[worst_month]}")
    
    # Weekly patterns
    dow_avg = daily_df.groupby('day_of_week')['Sales'].mean()
    best_day = dow_avg.idxmax()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    report.append(f"* Best day for sales: {days[best_day]}")
    report.append("")
    
    report.append("NEXT 90-DAY FORECAST")
    report.append("-"*40)
    total_forecast = future_forecast['Predicted_Sales'].sum()
    avg_daily = future_forecast['Predicted_Sales'].mean()
    report.append(f"* Total predicted sales: ${total_forecast:,.2f}")
    report.append(f"* Average daily sales:   ${avg_daily:,.2f}")
    report.append(f"* Forecast period:       {future_forecast['Date'].min().strftime('%Y-%m-%d')} to {future_forecast['Date'].max().strftime('%Y-%m-%d')}")
    report.append("")
    
    # Weekly forecast breakdown
    report.append("WEEKLY FORECAST BREAKDOWN")
    report.append("-"*40)
    weekly_forecast = future_forecast.groupby('Week')['Predicted_Sales'].sum().reset_index()
    for _, row in weekly_forecast.head(4).iterrows():
        report.append(f"  Week {int(row['Week'])}: ${row['Predicted_Sales']:,.2f}")
    if len(weekly_forecast) > 4:
        report.append(f"  ... and {len(weekly_forecast) - 4} more weeks")
    report.append("")
    
    report.append("TOP FEATURES IMPACTING SALES")
    report.append("-"*40)
    for i, row in feature_importance.head(5).iterrows():
        report.append(f"* {row['feature']}: {row['importance']*100:.1f}% importance")
    report.append("")
    
    report.append("RECOMMENDATIONS")
    report.append("-"*40)
    report.append(f"1. Inventory Planning:")
    report.append(f"   * Plan for ${avg_daily:,.2f} in daily sales")
    report.append(f"   * Stock up for {month_names[best_month]} seasonal peak")
    report.append("")
    report.append(f"2. Staffing:")
    report.append(f"   * Allocate more staff on {days[best_day]}s")
    report.append(f"   * Consider weekend staffing adjustments")
    report.append("")
    report.append("3. Marketing:")
    report.append("   * Target promotions during historically low periods")
    report.append("   * Prepare for seasonal campaigns")
    report.append("")
    
    report.append("="*60)
    report.append("Report generated for Future Interns - Sales & Demand Forecasting")
    report.append("="*60)
    
    # Save report with UTF-8 encoding
    import os
    os.makedirs('reports', exist_ok=True)
    with open('reports/business_report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    # Also print without emojis for terminal
    print('\n'.join(report))
    
    logger.info("Business report saved to reports/business_report.txt")
if __name__ == "__main__":
    main()