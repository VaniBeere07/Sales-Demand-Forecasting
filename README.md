# 📊 Sales & Demand Forecasting System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-black.svg)](https://github.com/psf/black)

> An end-to-end machine learning solution that predicts 90 days of future sales with 91% accuracy, helping businesses optimize inventory, staffing, and marketing.

---

## 🎯 Project Overview

This project was developed as part of the **Future Interns Machine Learning Task 1 (2026)** . It demonstrates how Machine Learning can solve real business problems by forecasting sales and providing actionable insights.

### Business Problem
Companies struggle with:
- ❌ Overstocking or understocking inventory
- ❌ Inefficient staff scheduling
- ❌ Poor cash flow management
- ❌ Missing seasonal trends

### Solution
A complete sales forecasting system that:
- ✅ Cleans and prepares historical sales data
- ✅ Engineers time-based features (seasonality, trends)
- ✅ Trains ML models for accurate predictions
- ✅ Generates 90-day sales forecasts
- ✅ Provides an interactive dashboard with business insights

---

## 📊 Key Results

| Metric | Value |
|--------|-------|
| **Total 90-day Sales** | $50,989 |
| **Average Daily Sales** | $567 |
| **Peak Day** | $1,289 (December 31) |
| **Lowest Day** | $141 (February 28) |
| **Best Month** | March |
| **Best Day** | Sunday |
| **Model Accuracy** | 91.48% |

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| **Language** | Python 3.8+ |
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn (Random Forest) |
| **Time Series** | Prophet, Statsmodels |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **Dashboard** | Streamlit |
| **Development** | VS Code, Jupyter Notebook |
| **Version Control** | Git |

---

## 📁 Project Structure

```
sales-demand-forecasting/
│
├── 📂 data/                    # Data files
│   ├── raw/                    # Original datasets
│   ├── processed/              # Cleaned data
│   └── forecasts/              # 90-day predictions
│
├── 📂 src/                     # Source code
│   ├── data/                   # Data loading, cleaning, feature engineering
│   ├── models/                 # Random Forest, Prophet models
│   ├── evaluation/             # Metrics & validation
│   └── visualization/          # Charts & plotting functions
│
├── 📂 dashboard/               # Streamlit dashboard
│   └── app.py                  # Main dashboard file
│
├── 📂 reports/                 # Generated outputs
│   ├── figures/                # PNG visualizations
│   └── business_report.txt     # Business-friendly summary
│
├── 📂 models/                  # Saved trained models
├── 📂 scripts/                 # Pipeline runner
├── 📂 config/                  # Configuration files
├── 📂 notebooks/               # Jupyter notebooks
│
├── 📄 requirements.txt         # Python dependencies
├── 📄 README.md               # This file
└── 📄 LICENSE                 # MIT License
```

---

## 🔄 Complete Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                   1. DATA LOADING                          │
│   Load Superstore Sales Dataset (9,994 records)           │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   2. DATA CLEANING                         │
│   Remove duplicates, handle missing values, remove outliers│
│   Final: 8,827 clean records                             │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   3. FEATURE ENGINEERING                   │
│   Create 14 time-based features (month, day, seasonality) │
│   Aggregate to: 1,224 daily records                      │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   4. MODEL TRAINING                        │
│   Algorithm: Random Forest Regressor                      │
│   Train: 979 samples | Test: 245 samples                 │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   5. MODEL EVALUATION                      │
│   MAE: $450.24 | RMSE: $577.07 | MAPE: 8.52% | R²: 0.87 │
│   Accuracy: 91.48%                                        │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   6. 90-DAY FORECAST                       │
│   Total: $50,989.12 | Average: $566.55/day              │
│   Peak: $1,288.66 | Lowest: $140.51                     │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   7. DASHBOARD & REPORT                    │
│   Interactive Streamlit dashboard with clickable insights │
│   Business report with actionable recommendations        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git (optional)
- Internet connection (for downloading dataset)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/sales-demand-forecasting.git
cd sales-demand-forecasting
```

**2. Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Download the dataset**
- Option A: Download from [Kaggle Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
- Place the file as: `data/raw/superstore_sales.csv`

**Option B: Generate sample dataset (if no dataset available)**
```bash
python -c "
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='D')
np.random.seed(42)
trend = np.linspace(100, 200, len(dates))
seasonal = 50 * np.sin(2 * np.pi * dates.dayofyear / 365)
weekly = 20 * np.sin(2 * np.pi * dates.dayofweek / 7)
noise = np.random.normal(0, 20, len(dates))
sales = trend + seasonal + weekly + noise
sales = np.maximum(sales, 0)

df = pd.DataFrame({
    'Order Date': dates,
    'Sales': sales,
    'Quantity': np.random.randint(1, 20, len(dates)),
    'Category': np.random.choice(['Furniture', 'Office Supplies', 'Technology'], len(dates)),
    'Region': np.random.choice(['East', 'West', 'North', 'South'], len(dates))
})
df.to_csv('data/raw/superstore_sales.csv', index=False)
print('✅ Sample dataset created with', len(df), 'records')
"
```

---

## 🏃 Running the Project

### 1. Run the Complete Pipeline
```bash
python scripts/run_pipeline.py
```

This will:
- Load and clean data
- Engineer features
- Train the model
- Generate 90-day forecast
- Create visualizations
- Save results

### 2. Launch the Dashboard
```bash
streamlit run dashboard/app.py
```

The dashboard will open at: `http://localhost:8501`

### 3. Run Tests
```bash
python test_setup.py
```

---

## 📱 Dashboard Features

| Feature | Description |
|---------|-------------|
| **Clickable KPI Cards** | 8 metric cards with detailed summaries |
| **Business Insights** | Actionable recommendations on each card |
| **Date Filter** | Filter forecast by date range |
| **Confidence Bands** | Toggle prediction uncertainty |
| **Search** | Searchable forecast data table |
| **Export** | Download data as CSV |
| **Charts** | Sales trend, weekly breakdown, day pattern |

---

## 📊 Outputs

| File | Location | Description |
|------|----------|-------------|
| `90_day_forecast.csv` | `data/forecasts/` | 90-day predictions |
| `business_report.txt` | `reports/` | Business summary |
| `sales_trend.png` | `reports/figures/` | Historical sales trend |
| `seasonality.png` | `reports/figures/` | Seasonal patterns |
| `model_performance.png` | `reports/figures/` | Model accuracy |
| `forecast.png` | `reports/figures/` | 90-day forecast |
| `random_forest.pkl` | `models/` | Trained model |

---

## 💡 Business Insights

| Finding | Business Action |
|---------|-----------------|
| Sunday is peak day ($1,289) | Schedule more staff on Sundays |
| Wednesday is lowest ($141) | Run promotions on Wednesdays |
| March is best month | Plan inventory for seasonal peak |
| 90-day revenue: $50,989 | Plan cash flow accordingly |
| Average daily: $567 | Set daily sales targets |

---

## 🎓 Skills Demonstrated

- **Data Science**: End-to-end ML pipeline
- **Python Programming**: Pandas, Scikit-learn, Streamlit
- **Machine Learning**: Random Forest, Feature Engineering
- **Time Series Analysis**: Seasonality, Trend detection
- **Data Visualization**: Matplotlib, Seaborn, Plotly
- **Dashboard Development**: Interactive Streamlit app
- **Business Communication**: Actionable insights

---

## 🔮 Future Improvements

- [ ] Add external factors (holidays, weather, promotions)
- [ ] Try advanced models (XGBoost, LSTM, Prophet)
- [ ] Deploy dashboard on Streamlit Cloud / AWS
- [ ] Add real-time data updates
- [ ] Store-level and product-level forecasting
- [ ] User authentication for dashboard

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Future Interns** - For the project opportunity
- **Kaggle** - For the Superstore dataset
- **Open Source Community** - For amazing tools and libraries

---

## 📧 Contact

Vani Beere - [vanibeere07@gmail.com](mailto:vanibeere898@gmail.com)

Project Link: [https://github.com/VaniBeere07/sales-demand-forecasting](https://github.com/VaniBeere07/sales-demand-forecasting)

---

## ⭐ Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!

---

**Built with ❤️ using Python, Streamlit, and Machine Learning**