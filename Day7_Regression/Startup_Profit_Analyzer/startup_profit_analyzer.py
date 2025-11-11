import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import os

os.makedirs('visuals', exist_ok=True)

df = pd.read_csv('50_Startups.csv')
print(df.head())

print("Check it is null or not:",df.isnull().sum())

x = df[['R&D Spend', 'Administration', 'Marketing Spend']]
y = df['Profit']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

lr = LinearRegression()
lr.fit(x_train, y_train)

print("Data Split into Train & Test Successfully!")
print(f"Training Samples: {x_train.shape[0]}, Testing Samples: {x_train.shape[0]}\n")

#Feature Scaling
scaler = MinMaxScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

scaled_train = pd.DataFrame(x_train_scaled, columns=x_train.columns)
scaled_test = pd.DataFrame(x_test_scaled, columns=x_test.columns)

# Save Scaled Data
scaled_train.to_csv("scaled_train_data.csv", index=False)
scaled_test.to_csv("scaled_test_data.csv", index=False)

# --- Visualization 1: R&D Spend vs Profit ---
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='R&D Spend', y='Profit', hue='State', palette='cool')
plt.title("R&D Spend vs Profit by State", fontsize=14)
plt.tight_layout()
plt.savefig("visuals/rd_profit_relationship.png")
plt.close()

# --- Visualization 2: Marketing Spend vs Profit ---
plt.figure(figsize=(8, 6))
sns.regplot(data=df, x='Marketing Spend', y='Profit', color='teal')
plt.title("Marketing Spend vs Profit (Correlation View)", fontsize=14)
plt.tight_layout()
plt.savefig("visuals/marketing_profit_correlation.png")
plt.close()