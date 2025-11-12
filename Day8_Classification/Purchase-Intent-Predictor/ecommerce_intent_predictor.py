import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt
import os

#load data
os.makedirs("visuals", exist_ok=True)
df = pd.read_csv("ecommerce_intent.csv")
print("Data Loaded Successfully!\n",df.head())

#check null values and remove
print("Check Null Values:\n",df.isnull().sum())
df.dropna(inplace=True)
print("Null Values Removed Successfully!\n")

#check duplicates and remove
print("Check Duplicates:\n",df.duplicated().sum())
df.drop_duplicates(inplace=True)
print("Duplicates Removed Successfully!\n")

#Label Encoding
le = LabelEncoder()
df['VisitorType'] = le.fit_transform(df['VisitorType'])
df["Weekend"] = le.fit_transform(df["Weekend"])

#split features
x = df.iloc[:,:-1]
y = df["Purchase"]

#train test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

#Feature Scaling
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

#Logistic Regression
lr = LogisticRegression()
lr.fit(x_train, y_train)
y_pred_log = lr.predict(x_test)

#Train Naive Bayes
nb = GaussianNB()
nb.fit(x_train, y_train)
y_pred_nb = nb.predict(x_test)

#both accuracy
print("Logistic Regression Accuracy:",accuracy_score(y_test, y_pred_log))
print("Naive Bayes Accuracy:",accuracy_score(y_test, y_pred_nb))

#confusion matrix
plt.figure(figsize=(8,6))
sns.heatmap(confusion_matrix(y_test,y_pred_log),annot=True,cmap="Blues")
plt.title("Confusion Matrix - Logistic Regression")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("visuals/confusion_matrix.png")
plt.close()

print("Are You Predict For New User By Command Line? (Y/N): ")
ans = input()
if ans == "Y" or ans == "y":
    #predict for new user
    print("\n Test New Visitor Input")
    visitor = int(input("Visitor Type (0=New, 1=Returning): "))
    time_on_site = float(input("Time on site (minutes): "))
    page_views = int(input("Page views: "))
    cart_adds = int(input("Items added to cart: "))
    bounce_rate = float(input("Bounce Rate (%): "))
    exit_rate = float(input("Exit Rate (%): "))
    weekend = int(input("Weekend (0=No, 1=Yes): "))

    user_df = pd.DataFrame([[visitor, time_on_site, page_views, cart_adds, bounce_rate, exit_rate, weekend]],
                        columns=x.columns)

    user_scaled = scaler.transform(user_df)
    pred = lr.predict(user_scaled)[0]

    if pred == 1:
        print("\nThe visitor is likely to PURCHASE ")
    else:
        print("\nThe visitor is NOT likely to purchase ")

else:
    print("Goodbye!")