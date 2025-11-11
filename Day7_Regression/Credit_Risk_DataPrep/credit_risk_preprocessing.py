import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

os.makedirs("visuals", exist_ok=True)

df = pd.read_csv("UCI_Credit_Card.csv")
print("Load Sample Data:\n", df.head(), "\n")

df.columns = df.columns.str.strip()  

# Some CSVs use lowercase or extra dots/spaces — normalize it
for col in df.columns:
    if "default" in col.lower() and "month" in col.lower():
        df.rename(columns={col: "Default"}, inplace=True)

# Drop ID column if exists
if "ID" in df.columns:
    df.drop(columns=["ID"], inplace=True)

print("Find Null and remove it:\n")
df.dropna(inplace=True)


categorical_cols = ['SEX', 'EDUCATION', 'MARRIAGE']
for col in categorical_cols:
    if col in df.columns:
        df[col] = df[col].astype('category')

#  Feature and Target Split 
if "Default" not in df.columns:
    raise ValueError("Target column 'Default' not found! Check dataset headers manually.")
X = df.drop(columns=["Default"])
y = df["Default"]

#  Train-Test Split 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
print("Train-Test Split Done!")
print(f"Train Samples: {X_train.shape[0]}, Test Samples: {X_test.shape[0]}\n")

#  Feature Scaling 
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

pd.DataFrame(X_train_scaled, columns=X.columns).to_csv("train_scaled.csv", index=False)
pd.DataFrame(X_test_scaled, columns=X.columns).to_csv("test_scaled.csv", index=False)

#  Default Distribution 
plt.figure(figsize=(7, 5))
sns.countplot(x="Default", data=df)
plt.title("Customer Default Distribution")
plt.tight_layout()
plt.savefig("visuals/default_distribution.png")
plt.close()

# Education vs Default 
if "EDUCATION" in df.columns:
    plt.figure(figsize=(8, 6))
    sns.barplot(x="EDUCATION", y="Default", data=df, hue="EDUCATION", palette="viridis", legend=False, estimator=lambda x: sum(x)/len(x))
    plt.title("Default Rate by Education Level")
    plt.tight_layout()
    plt.savefig("visuals/default_by_education.png")
    plt.close()

#  Correlation Heatmap 
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr().abs().nlargest(10, "Default"), annot=True, cmap="YlGnBu")
plt.title("Top Correlated Features with Default")
plt.tight_layout()
plt.savefig("visuals/correlation_heatmap.png")
plt.close()

