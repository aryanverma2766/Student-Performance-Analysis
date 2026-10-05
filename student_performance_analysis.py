"""
Student Performance Data Analysis
BCA Mini Project

Libraries:
- Pandas
- NumPy
- Matplotlib
- Seaborn

Run:
    pip install -r requirements.txt
    python src/student_performance_analysis.py
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "student_performance.csv"
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")

# -------------------------------------------------
# 1. Load dataset
# -------------------------------------------------
df = pd.read_csv(DATA_FILE)

print("\n=== DATASET OVERVIEW ===")
print(f"Records: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(df.head())

# -------------------------------------------------
# 2. Data cleaning
# -------------------------------------------------
df["Category"] = df["Category"].astype(str).str.strip().str.title()

numeric_columns = [
    "Attendance_Percent",
    "Python",
    "DBMS",
    "Web_Design",
    "Data_Structures",
    "Mathematics"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

print("\nMissing values before cleaning:")
print(df[numeric_columns].isna().sum())

duplicate_count = df.duplicated().sum()
df = df.drop_duplicates()

# Median imputation
df[numeric_columns] = df[numeric_columns].fillna(
    df[numeric_columns].median()
)

# Recalculate derived columns
subjects = [
    "Python",
    "DBMS",
    "Web_Design",
    "Data_Structures",
    "Mathematics"
]

df["Overall_Percentage"] = df[subjects].mean(axis=1).round(2)
df["Result"] = np.where(
    df["Overall_Percentage"] >= 40,
    "Pass",
    "Fail"
)

print(f"\nDuplicate rows removed: {duplicate_count}")
print("Missing values after cleaning:")
print(df[numeric_columns].isna().sum())

# Save cleaned data
df.to_csv(OUTPUT_DIR / "cleaned_student_performance.csv", index=False)

# -------------------------------------------------
# 3. Descriptive statistics
# -------------------------------------------------
analysis_columns = ["Attendance_Percent"] + subjects + ["Overall_Percentage"]

statistics = df[analysis_columns].agg(
    ["mean", "median", "std", "min", "max"]
).T

statistics.to_csv(OUTPUT_DIR / "descriptive_statistics.csv")

print("\n=== DESCRIPTIVE STATISTICS ===")
print(statistics.round(2))

# -------------------------------------------------
# 4. Grouping and aggregation
# -------------------------------------------------
category_analysis = (
    df.groupby("Category")
      .agg(
          Students=("Student_ID", "count"),
          Average_Attendance=("Attendance_Percent", "mean"),
          Average_Percentage=("Overall_Percentage", "mean")
      )
      .round(2)
)

gender_analysis = (
    df.groupby("Gender")
      .agg(
          Students=("Student_ID", "count"),
          Average_Attendance=("Attendance_Percent", "mean"),
          Average_Percentage=("Overall_Percentage", "mean")
      )
      .round(2)
)

category_analysis.to_csv(OUTPUT_DIR / "category_analysis.csv")
gender_analysis.to_csv(OUTPUT_DIR / "gender_analysis.csv")

# -------------------------------------------------
# 5. Sorting and filtering
# -------------------------------------------------
top_students = df.sort_values(
    "Overall_Percentage", ascending=False
).head(5)

at_risk_students = df[
    (df["Overall_Percentage"] < 50) |
    (df["Attendance_Percent"] < 65)
].sort_values("Overall_Percentage")

top_students.to_csv(OUTPUT_DIR / "top_5_students.csv", index=False)
at_risk_students.to_csv(
    OUTPUT_DIR / "students_requiring_attention.csv",
    index=False
)

# -------------------------------------------------
# 6. Correlation
# -------------------------------------------------
correlation = df["Attendance_Percent"].corr(
    df["Overall_Percentage"]
)

correlation_table = pd.DataFrame({
    "Variable_1": ["Attendance_Percent"],
    "Variable_2": ["Overall_Percentage"],
    "Pearson_Correlation": [round(correlation, 3)]
})

correlation_table.to_csv(
    OUTPUT_DIR / "attendance_correlation.csv",
    index=False
)

print(f"\nAttendance vs Overall Percentage correlation: {correlation:.3f}")

# -------------------------------------------------
# 7. Matplotlib - Bar chart
# -------------------------------------------------
subject_means = df[subjects].mean().sort_values(ascending=False)

plt.figure(figsize=(9, 5))
subject_means.plot(kind="bar")
plt.title("Average Marks by Subject")
plt.xlabel("Subject")
plt.ylabel("Average Marks")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_average_marks_by_subject.png", dpi=180)
plt.close()

# -------------------------------------------------
# 8. Matplotlib - Scatter plot
# -------------------------------------------------
plt.figure(figsize=(8, 5))
plt.scatter(
    df["Attendance_Percent"],
    df["Overall_Percentage"],
    alpha=0.75
)

z = np.polyfit(
    df["Attendance_Percent"],
    df["Overall_Percentage"],
    1
)
p = np.poly1d(z)
x_line = np.linspace(
    df["Attendance_Percent"].min(),
    df["Attendance_Percent"].max(),
    100
)

plt.plot(x_line, p(x_line), linewidth=2)
plt.title("Attendance vs Overall Percentage")
plt.xlabel("Attendance (%)")
plt.ylabel("Overall Percentage")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "02_attendance_vs_performance.png", dpi=180)
plt.close()

# -------------------------------------------------
# 9. Matplotlib - Histogram
# -------------------------------------------------
plt.figure(figsize=(8, 5))
plt.hist(
    df["Overall_Percentage"],
    bins=8,
    edgecolor="black"
)
plt.title("Distribution of Overall Percentage")
plt.xlabel("Overall Percentage")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "03_overall_percentage_distribution.png", dpi=180)
plt.close()

# -------------------------------------------------
# 10. Matplotlib - Pie chart
# -------------------------------------------------
result_counts = df["Result"].value_counts()

plt.figure(figsize=(6, 6))
plt.pie(
    result_counts.values,
    labels=result_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Pass vs Fail Distribution")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "04_pass_fail_distribution.png", dpi=180)
plt.close()

# -------------------------------------------------
# 11. Seaborn - Box plot
# -------------------------------------------------
plt.figure(figsize=(9, 5))
sns.boxplot(data=df[subjects])
plt.title("Subject-wise Marks Distribution")
plt.xlabel("Subject")
plt.ylabel("Marks")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "05_subject_boxplot.png", dpi=180)
plt.close()

# -------------------------------------------------
# 12. Seaborn - Heatmap
# -------------------------------------------------
corr_matrix = df[
    ["Attendance_Percent"] + subjects + ["Overall_Percentage"]
].corr()

plt.figure(figsize=(9, 7))
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f"
)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "06_correlation_heatmap.png", dpi=180)
plt.close()

# -------------------------------------------------
# 13. Matplotlib - Gender comparison
# -------------------------------------------------
gender_means = df.groupby("Gender")["Overall_Percentage"].mean()

plt.figure(figsize=(7, 5))
gender_means.plot(kind="bar")
plt.title("Average Overall Percentage by Gender")
plt.xlabel("Gender")
plt.ylabel("Average Overall Percentage")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "07_gender_comparison.png", dpi=180)
plt.close()

# -------------------------------------------------
# 14. Final summary
# -------------------------------------------------
best_subject = subject_means.idxmax()
lowest_subject = subject_means.idxmin()
pass_percentage = (df["Result"].eq("Pass").mean()) * 100

print("\n=== FINAL PROJECT SUMMARY ===")
print(f"Clean records: {len(df)}")
print(f"Average overall percentage: {df['Overall_Percentage'].mean():.2f}%")
print(f"Average attendance: {df['Attendance_Percent'].mean():.2f}%")
print(f"Best average subject: {best_subject}")
print(f"Lowest average subject: {lowest_subject}")
print(f"Pass percentage: {pass_percentage:.2f}%")
print(f"Attendance-performance correlation: {correlation:.3f}")

print("\nAnalysis completed successfully.")
print(f"Charts and result files are available in: {OUTPUT_DIR}")
