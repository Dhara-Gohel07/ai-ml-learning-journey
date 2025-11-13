import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import warnings
warnings.filterwarnings("ignore")

#Load Data

def load_or_create_dataset():
    try:
        df = pd.read_csv("stress_data.csv")
        print("Load Data :\n",df.head())
        return df
    except FileNotFoundError:
        print("\n Stress Data File Not Found...")

# FUNCTION: Train ML models
def train_models(df):
    le = LabelEncoder()
    df["stress_encoded"] = le.fit_transform(df["stress_level"])

    x = df.drop(["stress_level", "stress_encoded"], axis=1)
    y = df["stress_encoded"]

    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.25,random_state=42)

    models = {
        "DecisionTree" : DecisionTreeClassifier(),
        "KNN" : KNeighborsClassifier(),
        "SVM": SVC()
    }

    model_result = {}

    print("Training Models...\n")

    for name,model in models.items():
        model.fit(x_train, y_train)
        pred = model.predict(x_test)
        acc = accuracy_score(y_test, pred)
        model_result[name] = (model, acc)

        print(f"\n{name} Accuracy: {acc:.4f}")

    best_model_name = max(model_result, key=lambda x: model_result[x][1])
    best_model = model_result[best_model_name][0]

    print(f"\nBest Model: {best_model_name} (Accuracy: {model_result[best_model_name][1]:.4f})")

    return best_model, le

# FUNCTION: Manual prediction mode
def manual_test(best_model,le):
    print("\n  Manual Stress Prediction Mode\n")
    sleep = float(input("Hours slept last night (4-10): "))
    meetings = int(input("Number of meetings today (0-8): "))
    tasks = int(input("Tasks completed (0-6): "))
    screen = float(input("Total screen hours (3-12): "))
    breaks = int(input("Breaks taken (0-5): "))
    mood = int(input("Mood score (1-5): "))

    user_data = np.array([[sleep, meetings, tasks, screen, breaks, mood]])

    prediction = best_model.predict(user_data)[0]
    stress_label = le.inverse_transform([prediction])[0]

    print(f"\n **Predicted Stress Level: {stress_label}**\n")

# MAIN PROGRAM

if __name__ == "__main__":
    print("  WORK-DAY STRESS CLASSIFIER")
    df = load_or_create_dataset()

    best_model, encoder = train_models(df)

    print("\nDo you want to test with your own input?")
    choice = input("Type yes/no: ").lower()

    if choice == "yes":
        manual_test(best_model, encoder)
    else:
        print("\n✔ Program finished. Model trained successfully.")



