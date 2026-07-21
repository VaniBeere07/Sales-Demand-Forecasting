import pandas as pd
import os

# Load the forecast
forecast = pd.read_csv('data/forecasts/90_day_forecast.csv')

# Generate report
report = []
report.append('='*60)
report.append('           BUSINESS FORECASTING REPORT')
report.append('='*60)
report.append('')
report.append('NEXT 90-DAY FORECAST SUMMARY')
report.append('-'*40)
report.append(f'Total predicted sales: ${forecast["Predicted_Sales"].sum():,.2f}')
report.append(f'Average daily sales:   ${forecast["Predicted_Sales"].mean():,.2f}')
report.append(f'Maximum daily sales:    ${forecast["Predicted_Sales"].max():,.2f}')
report.append(f'Minimum daily sales:    ${forecast["Predicted_Sales"].min():,.2f}')
report.append('')
report.append('MONTHLY FORECAST BREAKDOWN')
report.append('-'*40)
monthly = forecast.groupby('Month')['Predicted_Sales'].sum()
for month, sales in monthly.items():
    report.append(f'{month}: ${sales:,.2f}')
report.append('')
report.append('WEEKLY FORECAST BREAKDOWN')
report.append('-'*40)
weekly = forecast.groupby('Week')['Predicted_Sales'].sum()
for week, sales in weekly.head(10).items():
    report.append(f'Week {int(week)}: ${sales:,.2f}')
if len(weekly) > 10:
    report.append(f'... and {len(weekly) - 10} more weeks')
report.append('')
report.append('KEY INSIGHTS')
report.append('-'*40)
best_day = forecast.loc[forecast['Predicted_Sales'].idxmax()]
worst_day = forecast.loc[forecast['Predicted_Sales'].idxmin()]
report.append(f'* Best day: {best_day["Day_Name"]} ({best_day["Date"]}) - ${best_day["Predicted_Sales"]:,.2f}')
report.append(f'* Worst day: {worst_day["Day_Name"]} ({worst_day["Date"]}) - ${worst_day["Predicted_Sales"]:,.2f}')
report.append('')
report.append('BUSINESS RECOMMENDATIONS')
report.append('-'*40)
report.append('1. Inventory Planning:')
report.append(f'   - Plan for ${forecast["Predicted_Sales"].mean():,.2f} in average daily sales')
report.append(f'   - Peak day requires ${forecast["Predicted_Sales"].max():,.2f} in inventory')
report.append('2. Staffing:')
report.append(f'   - Allocate more staff on {best_day["Day_Name"]}s')
report.append(f'   - Reduce staffing on {worst_day["Day_Name"]}s')
report.append('3. Marketing:')
report.append('   - Run promotions during low-sales periods')
report.append('   - Prepare for seasonal campaigns')
report.append('')
report.append('='*60)
report.append('Report generated for Future Interns - Sales & Demand Forecasting')
report.append('='*60)

# Save report
os.makedirs('reports', exist_ok=True)
with open('reports/business_report.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print('\n'.join(report))
print('\n✅ Report saved to reports/business_report.txt')