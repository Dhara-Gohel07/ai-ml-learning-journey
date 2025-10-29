import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Create Output Folders ---
os.makedirs("visuals", exist_ok=True)
os.makedirs("insights", exist_ok=True)

# --- Load Data ---
df = pd.read_csv("sales_performance.csv")

# --- Data Cleaning ---
df.dropna(inplace=True)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Profit_Margin'] = round((df['Profit'] / df['Revenue']) * 100, 2)

print(" Data Loaded & Cleaned Successfully!\n")
print(" Data Summary:\n", df.describe())


#  SALES TREND OVER TIME

plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='Date', y='Revenue', marker='o', hue='Region', palette='tab10')
plt.title('Sales Trend Over Time', fontsize=14, weight='bold')
plt.xlabel('Date')
plt.ylabel('Revenue')
plt.legend(title="Region")
plt.tight_layout()
plt.savefig('visuals/sales_trend_over_time.png')
plt.close()


# REGION-WISE PERFORMANCE

region_perf = (
    df.groupby('Region')[['Revenue', 'Profit']]
    .sum()
    .sort_values(by='Revenue', ascending=False)
)

plt.figure(figsize=(8, 6))
sns.barplot(
    x=region_perf.index,
    y=region_perf["Revenue"],
    hue=region_perf.index,
    palette="coolwarm",
    legend=False
)

plt.title("Total Revenue by Region", fontsize=14, weight='bold')
plt.xlabel("Region")
plt.ylabel("Total Revenue")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("visuals/region_performance.png")
plt.close()

# PROFIT MARGIN HEATMAP

pivot_table = df.pivot_table(
    values='Profit_Margin',
    index='Region',
    columns='Category',
    aggfunc='mean'
)

plt.figure(figsize=(8, 6))
sns.heatmap(pivot_table, annot=True, cmap="YlGnBu", fmt=".2f")
plt.title("Average Profit Margin by Region & Category", fontsize=14, weight='bold')
plt.tight_layout()
plt.savefig("visuals/profit_margin_heatmap.png")
plt.close()


insights = f"""
Business Sales Analytics Insights
----------------------------------
• Total Revenue: ${df['Revenue'].sum():,.2f}
• Total Profit: ${df['Profit'].sum():,.2f}
• Average Profit Margin: {df['Profit_Margin'].mean():.2f}%

Key Observations:
- {region_perf.index[0]} region generated the highest revenue (${region_perf['Revenue'].iloc[0]:,.0f})
- Profit margin varies significantly by product category and region
- Clear seasonal and regional sales trends visible across timelines
"""

with open("insights/report.txt", "w", encoding="utf-8") as f:
    f.write(insights)

print("\nAnalysis Completed Successfully!")
print(insights)
print("\nVisuals saved in 'visuals/' folder and insights in 'insights/report.txt'")
