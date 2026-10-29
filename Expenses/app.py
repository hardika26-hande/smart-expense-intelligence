import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Smart Expense Intelligence",
    page_icon="💸",
    layout="wide"
)

st.title("💸 Smart Expense Intelligence")
st.write("Explore your spending and understand where your money goes.")

# Load your cleaned dataset
import random
from datetime import datetime, timedelta

random.seed(42)

if "Date" not in st.session_state:
    categories = [
        "Food", "Transport", "Shopping",
        "Entertainment", "Health", "Rent", "Utilities"
    ]

    payment_modes = ["Cash", "Card", "Online"]
    expenses = []

    for i in range(200):
        expenses.append({
            "Date": datetime.today() - timedelta(days=random.randint(0, 365)),
            "Category": random.choice(categories),
            "Amount": random.randint(50, 2000),
            "Payment_Mode": random.choice(payment_modes),
        })

    st.session_state["Date"] = expenses

df = pd.DataFrame(st.session_state["Date"])
df["Date"] = pd.to_datetime(df["Date"])

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
