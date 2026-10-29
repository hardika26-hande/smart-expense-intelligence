import pandas as pd
from pathlib import Path

# Find the CSV file in this project folder
file_path = Path(__file__).parent / "personal_expense_dataset.csv"

# Load the dataset
df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 transactions:")
print(df.head())

print("\nMissing values in each column:")
print(df.isnull().sum())
