
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Load cleaned expense data
df = pd.read_csv("cleaned_expenses.csv")

# Calculate total spending per category
category_totals = (
    df.groupby("Category")["Amount"]
    .sum()
    .sort_values(ascending=True)
)

# Create the chart
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(category_totals.index, category_totals.values)

# Add spending labels to each bar
for bar in bars:
    amount = bar.get_width()
    ax.text(
        amount + category_totals.max() * 0.01,
        bar.get_y() + bar.get_height() / 2,
        f"₹{amount:,.0f}",
        va="center"
    )

ax.set_title("Total Spending by Category", fontsize=16)
ax.set_xlabel("Total Amount (₹)")
ax.set_ylabel("Category")

# Display the horizontal axis in lakhs
ax.xaxis.set_major_formatter(
    FuncFormatter(lambda x, _: f"₹{x / 100000:.1f}L")
)

ax.set_xlim(0, category_totals.max() * 1.18)
ax.grid(axis="x", alpha=0.25)
ax.set_axisbelow(True)

plt.tight_layout()
plt.show()
