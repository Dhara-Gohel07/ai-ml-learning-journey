import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import os

if not os.path.exists("visuals"):
    os.makedirs("visuals", exist_ok=True)


df = pd.read_csv('customer_lifestyle.csv')

df['purchase_categories'] = df['purchase_categories'].apply(lambda x: ast.literal_eval(x))

all_items = sorted({item for sublist in df['purchase_categories'] for item in sublist})

for item in all_items:
    df[item] = df['purchase_categories'].apply(lambda x: 1 if item in x else 0)

#frequency plot
plt.figure(figsize=(8,5))
df[all_items].sum().sort_values(ascending=False).plot(kind='bar')
plt.title("Item Frequency")
plt.tight_layout()
plt.savefig("visuals/item_frequency.png")
plt.close()

# Apriori Algorithm
frequent_items = apriori(df[all_items], min_support=0.05, use_colnames=True)

rules = association_rules(frequent_items, metric="lift", min_threshold=1.2)
rules = rules.sort_values(by='lift', ascending=False)

rules.to_csv("rules_apriori.csv")

# FP-GROWTH
fp_items = fpgrowth(df[all_items], min_support=0.01, use_colnames=True)
fp_rules = association_rules(fp_items, metric="confidence", min_threshold=0.4)
fp_rules = fp_rules.sort_values(by='lift', ascending=False)

fp_rules.to_csv("rules_fpgrowth.csv")

# Heatmap of Support vs Lift
plt.figure(figsize=(10,6))
sns.scatterplot(x=rules['support'], y=rules['lift'])
plt.title("Support vs Lift")
plt.tight_layout()
plt.savefig("visuals/top_rules.png")
plt.close()

print("Top Apriori Rules:\n", rules.head())
print("Top FP-Growth Rules:\n", fp_rules.head())

def summarize_results(df, apriori_rules, fpgrowth_rules, output_file="analysis_summary.txt"):
    with open(output_file, "w") as f:
        f.write("=== DATASET SUMMARY ===\n")
        f.write(f"Total Rows: {len(df)}\n")
        f.write(f"Total Unique Items: {len(all_items)}\n\n")

        # Top Item Frequency
        f.write("\n=== TOP ITEM FREQUENCIES ===\n")
        top_items = df[all_items].sum().sort_values(ascending=False).head(10)
        for item, count in top_items.items():
            f.write(f"{item}: {count}\n")

        # Apriori Summary
        f.write("\n\n=== APRIORI RULES SUMMARY ===\n")
        f.write(f"Total Apriori Rules: {len(apriori_rules)}\n")

        if not apriori_rules.empty:
            f.write("Top 5 Apriori Rules:\n")
            for _, row in apriori_rules.head().iterrows():
                f.write(
                    f"{list(row['antecedents'])} -> {list(row['consequents'])} | "
                    f"Lift={row['lift']:.3f}, Confidence={row['confidence']:.3f}\n"
                )

        # FP-Growth Summary
        f.write("\n\n=== FP-GROWTH RULES SUMMARY ===\n")
        f.write(f"Total FP-Growth Rules: {len(fpgrowth_rules)}\n")

        if not fpgrowth_rules.empty:
            f.write("Top 5 FP-Growth Rules:\n")
            for _, row in fpgrowth_rules.head().iterrows():
                f.write(
                    f"{list(row['antecedents'])} -> {list(row['consequents'])} | "
                    f"Lift={row['lift']:.3f}, Confidence={row['confidence']:.3f}\n"
                )

        # Insights
        f.write("\n\n=== INSIGHTS ===\n")
        f.write("- Higher LIFT means strong association between items.\n")
        f.write("- Confidence shows reliability of the rule.\n")
        f.write("- FP-Growth may generate fewer rules if confidence threshold is high.\n")
        f.write("- Items with high frequency appear more often in rules.\n")

    print("\nSummary saved successfully →", output_file)


summarize_results(df, rules, fp_rules, output_file="visuals/analysis_summary.txt")