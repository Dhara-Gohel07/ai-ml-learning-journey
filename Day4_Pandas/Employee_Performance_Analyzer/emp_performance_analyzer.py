import pandas as pd

df = pd.read_csv('D:/ai-ml-learning-journey/Day4_Pandas/Employee_Performance_Analyzer/employee_performance.csv')
print("\n Data info \n",df.info())

print("Dataset Preview:\n")
print(df.head(),"\n")

print("Summary Statistics:",df.describe(), "\n")
print("Check for missing values:", df.isnull().sum(), "\n")

df = df.drop_duplicates()
df = df.dropna()

# --- ANALYSIS 1: Average salary and performance by department ---

avg_sal_perf = df.groupby('Department')[['MonthlySalary','PerformanceScore']].mean()
print("Average Salary and Performance by Department:\n", avg_sal_perf, "\n")

# --- ANALYSIS 2: Top 5 employees by performance score ---
top_performers = df.sort_values(by='PerformanceScore', ascending=False).head(5)
print("Top 5 Employees by Performance Score:\n", top_performers[['Name','Department','PerformanceScore','Bonus']], "\n")

# --- ANALYSIS 3: Employees with low attendance ---
Low_attendance = df[df['Attendance(%)']<90]
print("Employees with Attendance below 90%:\n", Low_attendance[['Name','Department','Attendance(%)']], "\n")

# --- ANALYSIS 4: Correlation between  Salary , Performance and Bonus ---
correlation = df[['MonthlySalary','PerformanceScore','Bonus']].corr()
print("Correlation between Monthly Salary, Performance Score and Bonus:\n", correlation, "\n")

# --- ANALYSIS 5: Department-wise average experience ---
avg_experience = df.groupby('Department')['Experience(Years)'].mean()
print("Average Experience by Department:\n", avg_experience, "\n")

avg_sal_perf.to_csv("dept_summary.csv")
top_performers.to_csv("top_performers.csv")
print("\n  Summary files saved: dept_summary.csv, top_performers.csv")

