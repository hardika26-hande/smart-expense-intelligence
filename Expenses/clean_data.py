import pandas as pd
from pathlib import Path

folder = Path(__file__).parent
file_path = folder / "personal_expense_dataset.csv"

df = pd.read_csv(file_path)

# Remove accidental spaces from column names
df.columns = df.columns.str.strip()

# Convert columns to suitable data types
df["Date"] = pd.to_datetime(
    df["Date"], errors="coerce", format="mixed"
)
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

# Check data quality
print("Original rows:", len(df))
print("Duplicate rows:", df.duplicated().sum())
print("Invalid dates:", df["Date"].isna().sum())
print("Invalid amounts:", df["Amount"].isna().sum())
print("Zero or negative amounts:", (df["Amount"] <= 0).sum())

# Check whether Month matches Date
expected_month = df["Date"].dt.month_name()
month_matches = (
    expected_month.str.lower()
    == df["Month"].astype(str).str.strip().str.lower()
)

print("Month mismatches:", (~month_matches & df["Date"].notna()).sum())

print("\nPayment methods:")
print(df["Payment_Mode"].value_counts())

print("\nCategories:")
print(df["Category"].value_counts())

print("\nDate range:")
print(df["Date"].min(), "to", df["Date"].max())

# Save a cleaned copy without changing the original
cleaned = df.drop_duplicates().copy()
cleaned = cleaned.dropna(subset=["Date", "Category", "Amount"])
cleaned = cleaned[cleaned["Amount"] > 0]

cleaned.to_csv(folder / "cleaned_expenses.csv", index=False)

print("\nCleaned rows:", len(cleaned))
print("Saved as cleaned_expenses.csv")
