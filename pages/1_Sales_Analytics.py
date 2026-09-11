import streamlit as st
import pandas as pd
import os


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Sales Analytics",
    page_icon="💰",
    layout="wide"
)


# ============================================================
# PROJECT FILE
# ============================================================

base_folder = r"C:\Users\win\Desktop\sql\Python_SQL_Analysis"

excel_file = os.path.join(
    base_folder,
    "Retail_ECommerce_Final_Portfolio.xlsx"
)


# ============================================================
# CHECK EXCEL FILE
# ============================================================

if not os.path.exists(excel_file):

    st.error(
        "Retail_ECommerce_Final_Portfolio.xlsx not found."
    )

    st.stop()


# ============================================================
# LOAD SALES DATA
# ============================================================

@st.cache_data
def load_sales_data():

    return pd.read_excel(
        excel_file,
        sheet_name="Sales Master"
    )


sales = load_sales_data()


# ============================================================
# PAGE TITLE
# ============================================================

st.title("💰 Sales Analytics")

st.caption(
    "Revenue, profit and product sales performance"
)


# ============================================================
# DATE FILTER
# ============================================================

if "OrderDate" in sales.columns:

    sales["OrderDate"] = pd.to_datetime(
        sales["OrderDate"],
        errors="coerce"
    )

    min_date = sales["OrderDate"].min()
    max_date = sales["OrderDate"].max()

    if pd.notna(min_date) and pd.notna(max_date):

        selected_dates = st.date_input(
            "📅 Select Date Range",
            value=(
                min_date.date(),
                max_date.date()
            )
        )

        if len(selected_dates) == 2:

            start_date = pd.Timestamp(
                selected_dates[0]
            )

            end_date = pd.Timestamp(
                selected_dates[1]
            )

            filtered_sales = sales[
                (
                    sales["OrderDate"] >= start_date
                )
                &
                (
                    sales["OrderDate"] <= end_date
                )
            ].copy()

        else:

            filtered_sales = sales.copy()

    else:

        filtered_sales = sales.copy()

else:

    filtered_sales = sales.copy()


# ============================================================
# KPI CALCULATIONS
# ============================================================

revenue = 0

if "Revenue" in filtered_sales.columns:

    revenue = filtered_sales["Revenue"].sum()


profit = 0

if "Profit" in filtered_sales.columns:

    profit = filtered_sales["Profit"].sum()


quantity = 0

if "Quantity" in filtered_sales.columns:

    quantity = filtered_sales["Quantity"].sum()


orders = 0

if "OrderID" in filtered_sales.columns:

    orders = filtered_sales["OrderID"].nunique()


aov = 0

if orders > 0:

    aov = revenue / orders


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📌 Sales Overview")


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "💰 Revenue",
        f"${revenue:,.2f}"
    )


with col2:

    st.metric(
        "📈 Profit",
        f"${profit:,.2f}"
    )


with col3:

    st.metric(
        "🛒 Orders",
        f"{orders:,}"
    )


with col4:

    st.metric(
        "📦 Quantity Sold",
        f"{quantity:,}"
    )


with col5:

    st.metric(
        "💵 AOV",
        f"${aov:,.2f}"
    )


# ============================================================
# MONTHLY REVENUE
# ============================================================

st.divider()

st.subheader("📈 Monthly Revenue")


if (
    "OrderDate" in filtered_sales.columns
    and
    "Revenue" in filtered_sales.columns
):

    monthly_revenue = (
        filtered_sales
        .dropna(subset=["OrderDate"])
        .assign(
            Month=lambda x:
            x["OrderDate"]
            .dt
            .to_period("M")
            .astype(str)
        )
        .groupby("Month")["Revenue"]
        .sum()
        .reset_index()
    )

    st.line_chart(
        monthly_revenue.set_index("Month")
    )

else:

    st.info(
        "OrderDate or Revenue column is not available."
    )


# ============================================================
# REVENUE BY CATEGORY
# ============================================================

st.divider()

st.subheader("🏷️ Revenue by Category")


category_column = None

for column in [
    "CategoryName",
    "Category",
    "CategoryID"
]:

    if column in filtered_sales.columns:

        category_column = column
        break


if (
    category_column
    and
    "Revenue" in filtered_sales.columns
):

    category_revenue = (
        filtered_sales
        .groupby(category_column)["Revenue"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    st.bar_chart(
        category_revenue
    )

else:

    st.info(
        "Category or Revenue column is not available."
    )


# ============================================================
# TOP PRODUCTS BY REVENUE
# ============================================================

st.divider()

st.subheader("🏆 Top 10 Products by Revenue")


product_column = None

for column in [
    "ProductName",
    "Product"
]:

    if column in filtered_sales.columns:

        product_column = column
        break


if (
    product_column
    and
    "Revenue" in filtered_sales.columns
):

    top_products = (
        filtered_sales
        .groupby(product_column)["Revenue"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    st.bar_chart(
        top_products
    )

else:

    st.info(
        "Product or Revenue column is not available."
    )


# ============================================================
# TOP PRODUCTS BY PROFIT
# ============================================================

st.divider()

st.subheader("💎 Top 10 Products by Profit")


if (
    product_column
    and
    "Profit" in filtered_sales.columns
):

    top_profit = (
        filtered_sales
        .groupby(product_column)["Profit"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    st.bar_chart(
        top_profit
    )

else:

    st.info(
        "Product or Profit column is not available."
    )


# ============================================================
# SALES DATA
# ============================================================

st.divider()

st.subheader("📋 Sales Details")


st.dataframe(
    filtered_sales,
    use_container_width=True,
    hide_index=True
)