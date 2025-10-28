import pandas as pd

df = pd.read_csv('D:/ai-ml-learning-journey/Day4_Pandas/Sales_Data_Analyzer/sales_data.csv')


print("\n Data info \n",df.info())

print("Dataset Preview:")
print(df.head(),"\n")

df['Date'] = pd.to_datetime(df['Date'])

print("Check for missing values:", df.isnull().sum(), "\n")

print("Summary Statistics:")
print(df.describe(), "\n")

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
print(f"Total Sales: {total_sales}")
print(f"Total Profit: {total_profit}\n")

sales_by_region = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
print("Sales by Region:", sales_by_region, "\n")

sales_by_category = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
print("Sales by Category:", sales_by_category, "\n")

df['Profit_Margin'] = round(df['Profit'] / df['Sales'] * 100, 2)  
print("\n Profit Margin Added : \n",df[['Product','Profit_Margin']])

top_products = df.sort_values(by="Profit", ascending=False).head(5)
print("\n Top 5 Products by Profit : \n",top_products[['Product','Profit']])

