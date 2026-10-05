# Student Performance Data Analysis

## BCA Mini Project – Data Science Using Python

### Selected Topic
**Student Performance Data Analysis**

This topic is included in the shared list as:

> Student Performance Data Analysis – Marks, attendance, subject-wise performance.

### Objective
The project analyzes student marks and attendance to identify academic performance patterns using:

- Pandas
- NumPy
- Matplotlib
- Seaborn

### Assignment Requirements Covered

1. Problem statement
2. Dataset description
3. Data cleaning using Pandas
   - Missing values
   - Duplicate records
   - Incorrect data types
   - Inconsistent values
4. Data analysis using NumPy & Pandas
   - Mean
   - Median
   - Standard deviation
   - Grouping and aggregation
   - Sorting and filtering
   - Correlation
5. Data visualization
   - Matplotlib: bar chart, scatter plot, histogram, pie chart
   - Seaborn: box plot and heatmap
6. 5–8 findings
7. Conclusion

### Project Structure

```text
Student_Performance_Data_Analysis_Project/
│
├── data/
│   └── student_performance.csv
│
├── src/
│   └── student_performance_analysis.py
│
├── output/
│   └── Generated charts and analysis files
│
├── requirements.txt
├── README.md
└── Student_Performance_Data_Analysis_Mini_Project.docx
```

### How to Run

Open Command Prompt/Terminal in the project folder.

```bash
pip install -r requirements.txt
python src/student_performance_analysis.py
```

The program reads the CSV from the `data` folder, cleans the dataset, performs the analysis, and generates charts/results in the `output` folder.

### Dataset

The included dataset is an academic/synthetic dataset prepared for this educational mini project. It should be treated as a demonstration dataset rather than real institutional student data.

### Expected Outputs

The program generates:

- Average marks by subject
- Attendance vs performance scatter plot
- Overall percentage histogram
- Pass/fail pie chart
- Subject-wise box plot
- Correlation heatmap
- Gender comparison chart
- Descriptive statistics CSV
- Category analysis CSV
- Gender analysis CSV
- Top 5 students CSV
- Students requiring attention CSV
- Attendance correlation CSV
- Cleaned dataset CSV

### Academic Note

The project demonstrates association and descriptive patterns. Correlation does not prove that attendance alone causes changes in academic performance.
