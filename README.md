# Supermarket Sales Analysis

This beginner-friendly Python project analyzes `supermarket_sales.csv`. It calculates findings from the CSV at runtime and does not hard-code analysis results.

## Run in VS Code

Open this folder in VS Code and run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python analyze_sales.py
```

If PowerShell blocks activation, use:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe analyze_sales.py
```

The terminal prints inspection, validation, requested answers, insights, recommendations, and comparisons with the previously quoted values. Charts open with `plt.show()` and are saved under `charts`.

## Project summary

Problem Statement: Analyze supermarket transactions to understand revenue, product demand, branch and city performance, customer behavior, payment usage, and customer satisfaction.

Dataset: The CSV contains invoice, date, location, customer, product, quantity, price, payment, rating, and sales fields.

Methodology: The program loads data with Pandas, checks quality, removes invalid records when needed, verifies `Sales = Quantity * Unit Price`, groups data for the business questions, and creates focused Matplotlib/Seaborn charts.

Key Findings, Business Insights, Recommendations, and Conclusion: These are generated from the current CSV when the program runs so that the report cannot contain stale or invented values.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Key Features

- Loads and analyzes supermarket transaction data
- Performs data inspection and validation
- Checks for missing and duplicate values
- Verifies sales calculations using Quantity × Unit Price
- Analyzes product-wise sales
- Compares branch and city performance
- Analyzes category-wise sales
- Compares Member and Normal customers
- Analyzes payment method usage
- Analyzes customer ratings
- Identifies monthly sales trends
- Generates visualizations automatically
- Saves generated charts in the `charts/` directory
- Generates findings and recommendations directly from the dataset

## Visualizations

The project generates the following charts:

- Sales by Product
- Sales by Branch
- Sales by City
- Sales by Category
- Member vs Normal Customer Sales
- Average Transaction Value: Member vs Normal
- Payment Method Distribution
- Average Rating by Branch
- Monthly Sales Trend

All generated charts are stored in the `charts/` directory.

## Project Structure

```text
supermarket-sales-analysis/
│
├── charts/
│   ├── average_rating_by_branch.png
│   ├── average_transaction_member_vs_normal.png
│   ├── member_vs_normal_sales.png
│   ├── monthly_sales_trend.png
│   ├── payment_method_distribution.png
│   ├── sales_by_branch.png
│   ├── sales_by_category.png
│   ├── sales_by_city.png
│   └── sales_by_product.png
│
├── analyze_sales.py
├── supermarket_sales.csv
├── requirements.txt
├── README.md
└── .gitignore
```

## Key Learning Outcomes

- Data cleaning and validation
- Exploratory Data Analysis (EDA)
- Data aggregation using Pandas
- Data visualization
- Business-oriented data analysis
- Generating insights from structured data
- Automating analysis using Python

## Author

Lasya

Computer Science & Engineering Student