"""
Test script to verify setup
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from loguru import logger

logger.info("Testing setup...")

try:
    # Test imports
    from src.data.loader import DataLoader
    from src.data.cleaner import DataCleaner
    from src.data.feature_engineering import FeatureEngineer
    from src.models.random_forest import RandomForestModel
    from src.evaluation.metrics import ModelEvaluator
    from src.visualization.plots import SalesVisualizer
    
    logger.success("✅ All imports successful!")
    
    # Test DataLoader
    logger.info("Testing DataLoader...")
    loader = DataLoader()
    df = loader.load_data_with_date_parsing()
    print(f"   ✅ Data loaded: {len(df):,} rows")
    
    # Test DataCleaner
    logger.info("Testing DataCleaner...")
    cleaner = DataCleaner()
    clean_df = cleaner.clean_sales_data(df)
    print(f"   ✅ Data cleaned: {len(clean_df):,} rows")
    
    # Test FeatureEngineer
    logger.info("Testing FeatureEngineer...")
    engineer = FeatureEngineer()
    daily_df = engineer.aggregate_daily_sales(clean_df)
    print(f"   ✅ Features created: {len(daily_df)} daily records")
    
    logger.success("\n✅ All tests passed! Setup is complete and ready to run.")
    print("\n🚀 Run the pipeline with: python scripts/run_pipeline.py")
    
except Exception as e:
    logger.error(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()