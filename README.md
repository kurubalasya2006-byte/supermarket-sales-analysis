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

**Problem Statement:** Analyze supermarket transactions to understand revenue, product demand, branch and city performance, customer behavior, payment usage, and customer satisfaction.

**Dataset:** The CSV contains invoice, date, location, customer, product, quantity, price, payment, rating, and sales fields.

**Methodology:** The program loads data with Pandas, checks quality, removes invalid records when needed, verifies `Sales = Quantity * Unit Price`, groups data for the business questions, and creates focused Matplotlib/Seaborn charts.

**Key Findings, Business Insights, Recommendations, and Conclusion:** These are generated from the current CSV when the program runs so that the report cannot contain stale or invented values.