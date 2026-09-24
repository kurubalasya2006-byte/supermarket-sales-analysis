"""Beginner-friendly supermarket sales analysis using the supplied CSV file."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


DATA_FILE = Path(__file__).with_name("supermarket_sales.csv")
CHART_DIR = Path(__file__).with_name("charts")
REQUIRED_COLUMNS = [
    "Invoice ID", "Date", "Branch", "City", "Customer Type", "Gender",
    "Product", "Category", "Quantity", "Unit Price", "Payment", "Rating", "Sales",
]


def money(value: float) -> str:
    """Format monetary values consistently for the report."""
    return f"Rs {value:,.2f}"


def section(title: str) -> None:
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")


def save_and_show_chart(filename: str) -> None:
    """Save every chart and display it during a local VS Code run."""
    plt.tight_layout()
    plt.savefig(CHART_DIR / filename, dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()


def load_and_clean() -> pd.DataFrame:
    """Load the CSV, inspect its quality, and retain valid transactions."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Place supermarket_sales.csv in {DATA_FILE.parent}")

    df = pd.read_csv(DATA_FILE)
    section("1. LOAD DATASET")
    print(f"File: {DATA_FILE}")
    print(f"Dataset shape: {df.shape}")
    print("\nFirst five rows:")
    print(df.head().to_string(index=False))

    section("2. DATA QUALITY CHECKS")
    print("Column names:", list(df.columns))
    print("\nDataFrame information:")
    df.info()
    print("\nMissing values:")
    print(df.isnull().sum().to_string())
    print(f"\nDuplicate records: {df.duplicated().sum()}")

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    for column in ["Quantity", "Unit Price", "Rating", "Sales"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    invalid_counts = {
        "invalid_dates": int(df["Date"].isna().sum()),
        "non_positive_quantities": int((df["Quantity"] <= 0).sum()),
        "non_positive_unit_prices": int((df["Unit Price"] <= 0).sum()),
        "ratings_outside_0_to_10": int((~df["Rating"].between(0, 10)).sum()),
        "negative_sales": int((df["Sales"] < 0).sum()),
    }
    print("\nInvalid or inconsistent value checks:")
    for check, count in invalid_counts.items():
        print(f"{check}: {count}")

    original_rows = len(df)
    df = df.drop_duplicates().copy()
    valid_rows = df["Date"].notna()
    valid_rows &= df["Quantity"].gt(0)
    valid_rows &= df["Unit Price"].gt(0)
    valid_rows &= df["Rating"].between(0, 10)
    valid_rows &= df["Sales"].ge(0)
    df = df.loc[valid_rows].copy()
    for column in ["Product", "Category", "Payment"]:
        df[column] = df[column].astype(str).str.strip()
    print(f"\nRows after cleaning: {len(df)} (removed {original_rows - len(df)})")
    return df


def verify_sales(df: pd.DataFrame) -> None:
    """Check the supplied Sales column against Quantity multiplied by Unit Price."""
    section("3. SALES VERIFICATION")
    calculated_sales = df["Quantity"] * df["Unit Price"]
    difference = (df["Sales"] - calculated_sales).abs()
    mismatch_count = int((difference > 0.01).sum())
    print(f"Formula mismatches above Rs 0.01: {mismatch_count}")
    if mismatch_count:
        print(df.loc[difference > 0.01, ["Invoice ID", "Quantity", "Unit Price", "Sales"]].head(10).to_string(index=False))
    else:
        print("Sales = Quantity x Unit Price verified within rounding tolerance.")


def analyze(df: pd.DataFrame) -> dict[str, object]:
    """Calculate every requested statistic directly from the cleaned DataFrame."""
    section("4. EXPLORATORY DATA ANALYSIS")
    sales_by_product = df.groupby("Product")["Sales"].sum().sort_values(ascending=False)
    sales_by_branch = df.groupby("Branch")["Sales"].sum().sort_values(ascending=False)
    sales_by_city = df.groupby("City")["Sales"].sum().sort_values(ascending=False)
    sales_by_category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    quantity_by_product = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False)
    payment_counts = df["Payment"].value_counts()
    customer_average = df.groupby("Customer Type")["Sales"].mean().sort_values(ascending=False)
    customer_sales = df.groupby("Customer Type")["Sales"].sum().sort_values(ascending=False)
    branch_average = df.groupby("Branch")["Sales"].mean().sort_values(ascending=False)
    rating_by_branch = df.groupby("Branch")["Rating"].mean().sort_values(ascending=False)
    monthly_data = df.assign(Month=df["Date"].dt.to_period("M"))
    monthly_sales = monthly_data.groupby("Month")["Sales"].sum()
    monthly_transactions = monthly_data.groupby("Month").size()

    findings = {
        "df": df,
        "sales_by_product": sales_by_product,
        "sales_by_branch": sales_by_branch,
        "sales_by_city": sales_by_city,
        "sales_by_category": sales_by_category,
        "quantity_by_product": quantity_by_product,
        "payment_counts": payment_counts,
        "customer_average": customer_average,
        "customer_sales": customer_sales,
        "branch_average": branch_average,
        "rating_by_branch": rating_by_branch,
        "monthly_sales": monthly_sales,
        "monthly_transactions": monthly_transactions,
        "total_sales": df["Sales"].sum(),
        "total_transactions": len(df),
        "average_transaction": df["Sales"].mean(),
        "total_quantity": df["Quantity"].sum(),
        "average_rating": df["Rating"].mean(),
    }

    section("KEY PERFORMANCE INDICATORS")
    print(f"Total Sales: {money(findings['total_sales'])}")
    print(f"Total Transactions: {findings['total_transactions']}")
    print(f"Average Transaction Value: {money(findings['average_transaction'])}")
    print(f"Total Quantity Sold: {findings['total_quantity']}")
    print(f"Average Customer Rating: {findings['average_rating']:.2f}/10")

    print("\nAdditional findings:")
    print(f"Highest-selling product: {sales_by_product.index[0]} ({money(sales_by_product.iloc[0])})")
    print(f"Highest-performing branch: {sales_by_branch.index[0]} ({money(sales_by_branch.iloc[0])})")
    print(f"Highest-performing city: {sales_by_city.index[0]} ({money(sales_by_city.iloc[0])})")
    print(f"Highest-selling category: {sales_by_category.index[0]} ({money(sales_by_category.iloc[0])})")
    print(f"Most popular payment method: {payment_counts.index[0]} ({payment_counts.iloc[0]} transactions)")
    print("\nAverage transaction value by customer type:")
    print(customer_average.map(money).to_string())
    print("\nTotal sales by customer type:")
    print(customer_sales.map(money).to_string())
    print("\nMonthly sales:")
    print(monthly_sales.map(money).to_string())
    print("\nMonthly transaction counts:")
    print(monthly_transactions.to_string())
    return findings


def add_bar_labels(axis: plt.Axes, monetary: bool = False, decimals: int = 0) -> None:
    """Add readable values to bars in the current chart."""
    for bar in axis.patches:
        value = bar.get_width() if bar.get_width() > bar.get_height() else bar.get_height()
        label = money(value) if monetary else f"{value:,.{decimals}f}"
        if bar.get_width() > bar.get_height():
            axis.text(value, bar.get_y() + bar.get_height() / 2, f" {label}", va="center", fontsize=9)
        else:
            axis.text(bar.get_x() + bar.get_width() / 2, value, label, ha="center", va="bottom", fontsize=9)


def visualizations(f: dict[str, object]) -> None:
    """Create the requested focused charts with titles, labels, and data labels."""
    section("5. VISUALIZATIONS")
    CHART_DIR.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid", palette="deep")

    for series_name, title, xlabel, filename in [
        ("sales_by_product", "Sales by Product", "Product", "sales_by_product.png"),
        ("sales_by_branch", "Sales by Branch", "Branch", "sales_by_branch.png"),
        ("sales_by_city", "Sales by City", "City", "sales_by_city.png"),
        ("sales_by_category", "Sales by Category", "Category", "sales_by_category.png"),
    ]:
        figure, axis = plt.subplots(figsize=(10, 6))
        series = f[series_name].sort_values()
        series.plot(kind="barh", ax=axis, color="#457b9d")
        axis.set_title(title)
        axis.set_xlabel("Total Sales (Rs)")
        axis.set_ylabel(xlabel)
        add_bar_labels(axis, monetary=True)
        save_and_show_chart(filename)

    figure, axis = plt.subplots(figsize=(8, 6))
    f["customer_sales"].plot(kind="bar", ax=axis, color="#2a9d8f")
    axis.set_title("Member vs Normal Customer Sales")
    axis.set_xlabel("Customer Type")
    axis.set_ylabel("Total Sales (Rs)")
    axis.tick_params(axis="x", rotation=0)
    add_bar_labels(axis, monetary=True)
    save_and_show_chart("member_vs_normal_sales.png")

    figure, axis = plt.subplots(figsize=(8, 6))
    f["customer_average"].sort_index().plot(kind="bar", ax=axis, color="#e76f51")
    axis.set_title("Average Transaction Value: Member vs Normal")
    axis.set_xlabel("Customer Type")
    axis.set_ylabel("Average Sales (Rs)")
    axis.tick_params(axis="x", rotation=0)
    add_bar_labels(axis, monetary=True)
    save_and_show_chart("average_transaction_member_vs_normal.png")

    figure, axis = plt.subplots(figsize=(8, 6))
    f["payment_counts"].sort_values().plot(kind="bar", ax=axis, color="#f4a261")
    axis.set_title("Payment Method Distribution")
    axis.set_xlabel("Payment Method")
    axis.set_ylabel("Number of Transactions")
    axis.tick_params(axis="x", rotation=25)
    add_bar_labels(axis)
    save_and_show_chart("payment_method_distribution.png")

    figure, axis = plt.subplots(figsize=(8, 6))
    f["rating_by_branch"].plot(kind="bar", ax=axis, color="#6a994e")
    axis.set_title("Average Rating by Branch")
    axis.set_xlabel("Branch")
    axis.set_ylabel("Average Rating")
    axis.tick_params(axis="x", rotation=0)
    rating_values = f["rating_by_branch"]
    axis.set_ylim(rating_values.min() - 0.10, rating_values.max() + 0.10)
    add_bar_labels(axis, decimals=2)
    save_and_show_chart("average_rating_by_branch.png")

    figure, axis = plt.subplots(figsize=(10, 6))
    f["monthly_sales"].plot(kind="line", marker="o", linewidth=2, ax=axis, color="#264653")
    axis.set_title("Monthly Sales Trend")
    axis.set_xlabel("Month")
    axis.set_ylabel("Total Sales (Rs)")
    axis.tick_params(axis="x", rotation=45)
    save_and_show_chart("monthly_sales_trend.png")
    print(f"Charts saved in {CHART_DIR}")


def business_insights(f: dict[str, object]) -> None:
    """Print findings, interpretations, and cautious recommendations."""
    section("6. BUSINESS INSIGHTS")
    print("Product Insight")
    print(f"Finding: {f['sales_by_product'].index[0]} has the highest total sales ({money(f['sales_by_product'].iloc[0])}).")
    print("Interpretation: This product is the strongest revenue contributor in the recorded transactions.")
    print("Recommendation: Review its inventory levels and margin before planning replenishment or promotion.")

    print("\nBranch Insight")
    print(f"Finding: Branch {f['sales_by_branch'].index[0]} has the highest sales ({money(f['sales_by_branch'].iloc[0])}).")
    print("Interpretation: It is the strongest branch by recorded revenue.")
    print("Recommendation: Study its measurable sales practices for ideas that may help other branches.")

    print("\nCategory Insight")
    print(f"Finding: {f['sales_by_category'].index[0]} has the highest category sales ({money(f['sales_by_category'].iloc[0])}).")
    print("Interpretation: This category contributes the most recorded revenue.")
    print("Recommendation: Include demand for this category in stock planning, subject to profitability checks.")

    print("\nPayment Insight")
    print(f"Finding: {f['payment_counts'].index[0]} is most frequently used ({f['payment_counts'].iloc[0]} transactions).")
    print("Interpretation: It is the most common payment choice in this dataset.")
    print("Recommendation: Keep this payment option reliable while retaining alternatives.")

    print("\nCustomer Insight")
    higher_customer = f["customer_average"].index[0]
    print(f"Finding: {higher_customer} customers have the higher average transaction value ({money(f['customer_average'].iloc[0])}).")
    print("Interpretation: Average transaction value, rather than total sales alone, is the appropriate comparison because customer counts can differ.")
    print(f"Recommendation: Test targeted offers for {higher_customer} customers and measure the resulting transaction value.")

    print("\nRating Insight")
    print(f"Finding: {f['rating_by_branch'].index[0]} has the highest average rating ({f['rating_by_branch'].iloc[0]:.2f}/10).")
    print("Interpretation: Ratings vary by branch in the recorded data.")
    print("Recommendation: Review branch-level service practices before making customer-satisfaction changes.")

    print("\nMonthly Insight")
    last_date = f["df"]["Date"].max()
    last_month = last_date.to_period("M")
    last_month_count = f["monthly_transactions"].iloc[-1]
    print(f"Finding: The data runs through {last_date.date()}, and {last_month} contains {last_month_count} recorded transactions.")
    if last_date.day < last_date.days_in_month:
        july_is_lowest = f["monthly_sales"].loc[last_month] == f["monthly_sales"].min()
        fewer_than_other_months = last_month_count < f["monthly_transactions"].drop(last_month).min()
        if last_month.month == 7 and july_is_lowest and fewer_than_other_months:
            print("Interpretation: July recorded the lowest sales in the available dataset; however, the number of recorded July transactions is lower than the other months, so July should not be directly compared with complete months.")
        else:
            print("Interpretation: The final month is partial, so its lower or higher sales should not be compared as a complete-month result.")
        print("Recommendation: Wait for a complete month or compare normalized daily performance before making a monthly decision.")
    else:
        print("Interpretation: The available months end on a complete calendar month in this file.")
        print("Recommendation: Use the monthly pattern as a starting point and continue monitoring future complete months.")


def final_project_summary(f: dict[str, object]) -> None:
    """Print the concise summary requested for project evaluation."""
    section("7. FINAL PROJECT SUMMARY")
    print("Problem Statement")
    print("Analyze supermarket sales to identify patterns in products, branches, cities, categories, customers, payment methods, sales, and ratings.")
    print("\nDataset")
    print("The CSV contains invoice ID, date, branch, city, customer type, gender, product, category, quantity, unit price, payment, rating, and sales columns.")
    print("\nMethodology")
    print("1. Loaded the supplied CSV. 2. Inspected shape, columns, types, missing values, duplicates, and invalid values. 3. Verified the sales formula. 4. Cleaned only invalid records. 5. Grouped data for exploratory analysis. 6. Created focused charts. 7. Interpreted findings and recommendations.")
    print("\nKey Findings")
    print(f"Total sales: {money(f['total_sales'])}; transactions: {f['total_transactions']}; average transaction: {money(f['average_transaction'])}; quantity sold: {f['total_quantity']}; average rating: {f['average_rating']:.2f}/10.")
    print(f"Top product: {f['sales_by_product'].index[0]}; top branch: {f['sales_by_branch'].index[0]}; top city: {f['sales_by_city'].index[0]}; top category: {f['sales_by_category'].index[0]}; most popular payment: {f['payment_counts'].index[0]}.")
    print(f"Member average transaction: {money(f['customer_average'].get('Member', 0))}; Normal average transaction: {money(f['customer_average'].get('Normal', 0))}.")
    print("\nBusiness Insights")
    print("The findings identify where revenue and demand are concentrated, which payment method is most common, how customer types differ by average transaction value, and how ratings vary across branches.")
    print("\nRecommendations")
    print("Use high-demand products and categories in inventory planning, learn from the strongest branch, maintain the most-used payment option, test evidence-based membership offers, and monitor branch ratings.")
    print("\nConclusion")
    print("Data analytics turns transaction records into measurable evidence for inventory, branch operations, payment support, customer strategy, and service improvement decisions.")


def main() -> None:
    df = load_and_clean()
    verify_sales(df)
    findings = analyze(df)
    visualizations(findings)
    business_insights(findings)
    final_project_summary(findings)


if __name__ == "__main__":
    main()
