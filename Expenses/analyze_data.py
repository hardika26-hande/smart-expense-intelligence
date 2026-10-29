import pandas as pd
from pathlib import Path

folder = Path(__file__).parent
df = pd.read_csv(folder / "cleaned_expenses.csv")

# Total spending
print("\n===== EXPENSE SUMMARY =====")
print("Total spending: ₹", round(df["Amount"].sum(), 2))
print("Average transaction: ₹", round(df["Amount"].mean(), 2))
print("Number of transactions:", len(df))

# Spending by category
print("\n===== SPENDING BY CATEGORY =====")
category_spending = (
    df.groupby("Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
)
print(category_spending.round(2))

# Spending by payment method
print("\n===== SPENDING BY PAYMENT METHOD =====")
payment_spending = (
    df.groupby("Payment_Mode")["Amount"]
    .sum()
    .sort_values(ascending=False)
)
print(payment_spending.round(2))

# Monthly spending based on actual dates
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Month_Year"] = df["Date"].dt.to_period("M")

print("\n===== MONTHLY SPENDING =====")
monthly_spending = (
    df.groupby("Month_Year")["Amount"]
    .sum()
    .sort_index()
)
print(monthly_spending.tail(12).round(2))


print("\n===== AMOUNT VALIDATION =====")
print("Smallest transaction: ₹", df["Amount"].min())
print("Largest transaction: ₹", df["Amount"].max())
print("Median transaction: ₹", df["Amount"].median())
print("Average transaction: ₹", df["Amount"].mean())

print("\nLargest 10 transactions:")
print(
    df.nlargest(10, "Amount")[
        ["Date", "Category", "Amount", "Payment_Mode"]
    ].to_string(index=False)
)
