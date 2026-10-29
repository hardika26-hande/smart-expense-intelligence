import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Smart Expense Intelligence",
    page_icon="💸",
    layout="wide"
)

st.title("💸 Smart Expense Intelligence")
st.write("Explore your spending and understand where your money goes.")

# Load your cleaned dataset
file_path = Path("cleaned_expenses.csv")

if not file_path.exists():
    st.error("Could not find cleaned_expenses.csv. Make sure it is in your Expenses folder.")
    st.stop()

df = pd.read_csv(file_path)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
df = df.dropna(subset=["Date", "Amount", "Category"])

# Sidebar filters
st.sidebar.header("Filter expenses")

categories = sorted(df["Category"].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Choose categories", categories, default=categories
)

payment_modes = sorted(df["Payment_Mode"].dropna().unique())
selected_modes = st.sidebar.multiselect(
    "Payment mode", payment_modes, default=payment_modes
)

filtered = df[
    df["Category"].isin(selected_categories)
    & df["Payment_Mode"].isin(selected_modes)
].copy()

# Summary cards
total = filtered["Amount"].sum()
average = filtered["Amount"].mean() if not filtered.empty else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total spending", f"₹{total:,.0f}")
col2.metric("Average transaction", f"₹{average:,.0f}")
col3.metric("Transactions", f"{len(filtered):,}")

st.divider()

if filtered.empty:
    st.info("No expenses match your filters. Select more categories or payment modes.")
    st.stop()

# Spending by category
st.subheader("Spending by category")

category_totals = (
    filtered.groupby("Category", as_index=False)["Amount"]
    .sum()
    .sort_values("Amount", ascending=False)
)

fig_category = px.bar(
    category_totals,
    x="Category",
    y="Amount",
    color="Category",
    title="Total spending by category",
    labels={"Amount": "Amount (₹)"}
)

st.plotly_chart(fig_category, use_container_width=True)

# Monthly spending
st.subheader("Monthly spending")

filtered["Month"] = filtered["Date"].dt.to_period("M").astype(str)

monthly = (
    filtered.groupby("Month", as_index=False)["Amount"]
    .sum()
    .sort_values("Month")
)

fig_month = px.line(
    monthly,
    x="Month",
    y="Amount",
    markers=True,
    title="Spending trend over time",
    labels={"Amount": "Amount (₹)"}
)

st.plotly_chart(fig_month, use_container_width=True)

# Transaction table
st.subheader("Expense transactions")

st.dataframe(
    filtered.sort_values("Date", ascending=False),
    use_container_width=True,
    hide_index=True
)
