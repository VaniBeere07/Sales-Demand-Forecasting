"""
Data Loader Module
Handles loading and basic validation of sales data
"""

import pandas as pd
import yaml
from pathlib import Path
from loguru import logger

class DataLoader:
    """Handles loading sales data from various sources"""
    
    def __init__(self, config_path="config/config.yaml"):
        """Initialize with configuration"""
        self.config_path = config_path
        self.config = self._load_config()
        logger.info("DataLoader initialized successfully")
    
    def _load_config(self):
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.warning(f"Config file not found at {self.config_path}, using defaults")
            return {
                'data': {
                    'raw_path': 'data/raw/',
                    'filename': 'superstore_sales.csv',
                    'date_column': 'Order Date',
                    'target_column': 'Sales'
                }
            }
    
    def load_superstore_data(self):
        """Load the Superstore dataset with automatic encoding detection"""
        raw_path = self.config['data']['raw_path']
        filename = self.config['data']['filename']
        file_path = Path(raw_path) / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found at {file_path}")
        
        logger.info(f"Loading data from {file_path}")
        
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-16']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                logger.info(f"✅ Successfully loaded with encoding: {encoding}")
                break
            except (UnicodeDecodeError, ValueError):
                continue
        
        if df is None:
            # Last resort: try with error handling
            try:
                df = pd.read_csv(file_path, encoding='utf-8', errors='ignore')
                logger.warning("Loaded with errors='ignore' - some characters may be missing")
            except Exception as e:
                raise ValueError(f"Could not read file: {e}")
        
        logger.success(f"Loaded {len(df):,} records with {len(df.columns)} columns")
        return df
    
    def load_data_with_date_parsing(self):
        """Load data and parse dates automatically"""
        df = self.load_superstore_data()
        
        # Convert date column to datetime
        date_col = self.config['data']['date_column']
        
        # Try to find the date column if it doesn't exist
        if date_col not in df.columns:
            # Look for columns that might contain dates
            for col in df.columns:
                if 'date' in col.lower() or 'Date' in col:
                    date_col = col
                    logger.info(f"Using '{date_col}' as date column")
                    break
        
        if date_col in df.columns:
            try:
                df[date_col] = pd.to_datetime(df[date_col])
                logger.info(f"Date range: {df[date_col].min()} to {df[date_col].max()}")
            except Exception as e:
                logger.warning(f"Could not parse dates: {e}")
        else:
            logger.warning(f"Date column not found in data. Available columns: {df.columns.tolist()}")
        
        return df

# Test the loader
if __name__ == "__main__":
    loader = DataLoader()
    df = loader.load_data_with_date_parsing()
    print(df.head())
    print(df.info())