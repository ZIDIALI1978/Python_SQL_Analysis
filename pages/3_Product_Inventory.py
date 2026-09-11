import streamlit as st
import pandas as pd
import os


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Product & Inventory",
    page_icon="📦",
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
# CHECK FILE
# ============================================================

if not os.path.exists(excel_file):

    st.error(
        "Retail_ECommerce_Final_Portfolio.xlsx not found."
    )

    st.stop()


# ============================================================
# TITLE
# ============================================================

st.title("📦 Product & Inventory Intelligence")

st.caption(
    "Product performance, profitability, ABC analysis and inventory risk"
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def load_sheet(sheet_name, header=None):

    try:

        df = pd.read_excel(
            excel_file,
            sheet_name=sheet_name,
            header=header
        )

        df = df.dropna(
            axis=0,
            how="all"
        )

        df = df.dropna(
            axis=1,
            how="all"
        )

        return df

    except Exception as e:

        st.warning(
            f"Could not load '{sheet_name}': {e}"
        )

        return pd.DataFrame()


# ============================================================
# PRODUCT SCORECARD
# ============================================================

st.header("📊 Product Performance")

product_data = load_sheet(
    "Product Scorecard"
)

if not product_data.empty:

    product_data.columns = [
        str(col).strip()
        for col in product_data.columns
    ]

    st.dataframe(
        product_data,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # Find numeric columns
    # --------------------------------------------------------

    numeric_columns = product_data.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:

        # Try to identify revenue
        revenue_column = next(
            (
                col for col in numeric_columns
                if "revenue" in str(col).lower()
            ),
            None
        )

        # Try to identify profit
        profit_column = next(
            (
                col for col in numeric_columns
                if "profit" in str(col).lower()
            ),
            None
        )

        # Try to identify stock
        stock_column = next(
            (
                col for col in numeric_columns
                if "stock" in str(col).lower()
            ),
            None
        )

        # ----------------------------------------------------
        # KPI Cards
        # ----------------------------------------------------

        kpi1, kpi2, kpi3 = st.columns(3)

        with kpi1:

            if revenue_column:

                st.metric(
                    "💰 Total Revenue",
                    f"${product_data[revenue_column].sum():,.2f}"
                )

        with kpi2:

            if profit_column:

                st.metric(
                    "📈 Total Profit",
                    f"${product_data[profit_column].sum():,.2f}"
                )

        with kpi3:

            if stock_column:

                st.metric(
                    "📦 Total Stock",
                    f"{product_data[stock_column].sum():,.0f}"
                )


# ============================================================
# TOP REVENUE PRODUCTS
# ============================================================

st.divider()

st.header("🏆 Top Products by Revenue")

top_revenue = load_sheet(
    "Top Revenue Products_2"
)

if top_revenue.empty:

    # Fallback to original sheet
    top_revenue = load_sheet(
        "Top Revenue Products"
    )

if not top_revenue.empty:

    st.dataframe(
        top_revenue.head(10),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TOP PROFIT PRODUCTS
# ============================================================

st.divider()

st.header("💰 Top Products by Profit")

top_profit = load_sheet(
    "Top Profit Products_2"
)

if not top_profit.empty:

    st.dataframe(
        top_profit.head(10),
        use_container_width=True,
        hide_index=True
    )

    numeric_columns = top_profit.select_dtypes(
        include="number"
    ).columns.tolist()

    profit_column = next(
        (
            col for col in numeric_columns
            if "profit" in str(col).lower()
        ),
        None
    )

    if profit_column:

        chart_data = (
            top_profit
            .head(10)
            .copy()
        )

        # Try to find product name
        text_columns = chart_data.select_dtypes(
            exclude="number"
        ).columns.tolist()

        if text_columns:

            product_column = text_columns[0]

            chart_data = (
                chart_data[
                    [
                        product_column,
                        profit_column
                    ]
                ]
                .set_index(product_column)
            )

            st.bar_chart(
                chart_data
            )


# ============================================================
# SALES VELOCITY
# ============================================================

st.divider()

st.header("📈 Top Sales Velocity")

velocity_data = load_sheet(
    "Top Sales Velocity"
)

if not velocity_data.empty:

    st.dataframe(
        velocity_data.head(10),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ABC ANALYSIS
# ============================================================

st.divider()

st.header("🔤 ABC Analysis")

try:

    abc_raw = pd.read_excel(
        excel_file,
        sheet_name="ABC Analysis",
        header=None
    )

    abc_raw = abc_raw.dropna(
        axis=0,
        how="all"
    )

    abc_raw = abc_raw.dropna(
        axis=1,
        how="all"
    )

    header_row = None

    # Detect header row
    for i in range(
        min(20, len(abc_raw))
    ):

        row_text = (
            abc_raw.iloc[i]
            .astype(str)
            .str.strip()
            .str.lower()
            .tolist()
        )

        if any(
            "abc" in value
            for value in row_text
        ):

            header_row = i
            break

    if header_row is not None:

        abc_data = pd.read_excel(
            excel_file,
            sheet_name="ABC Analysis",
            header=header_row
        )

        abc_data = abc_data.dropna(
            axis=0,
            how="all"
        )

        abc_data = abc_data.dropna(
            axis=1,
            how="all"
        )

        abc_data.columns = [
            str(col).strip()
            for col in abc_data.columns
        ]

        st.dataframe(
            abc_data,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # Find ABC column
        # ----------------------------------------------------

        abc_column = None

        for column in abc_data.columns:

            values = (
                abc_data[column]
                .astype(str)
                .str.strip()
                .str.upper()
            )

            unique_values = set(
                values.dropna().unique()
            )

            if unique_values.intersection(
                {"A", "B", "C"}
            ):

                abc_column = column
                break

        if abc_column:

            abc_counts = (
                abc_data[abc_column]
                .astype(str)
                .str.strip()
                .str.upper()
                .value_counts()
                .reindex(
                    ["A", "B", "C"],
                    fill_value=0
                )
            )

            st.subheader(
                "Products by ABC Class"
            )

            st.bar_chart(
                abc_counts
            )

    else:

        st.warning(
            "ABC Analysis header could not be detected."
        )

except Exception as e:

    st.warning(
        f"ABC Analysis could not be loaded: {e}"
    )


# ============================================================
# INVENTORY RISK
# ============================================================

st.divider()

st.header("⚠️ Inventory Risk")

inventory_risk = load_sheet(
    "Inventory Risk"
)

if not inventory_risk.empty:

    st.dataframe(
        inventory_risk,
        use_container_width=True,
        hide_index=True
    )

    # Find risk/status column
    risk_column = None

    for column in inventory_risk.columns:

        column_text = (
            str(column)
            .strip()
            .lower()
        )

        if (
            "risk" in column_text
            or "status" in column_text
        ):

            risk_column = column
            break

    if risk_column:

        risk_counts = (
            inventory_risk[risk_column]
            .astype(str)
            .value_counts()
        )

        st.subheader(
            "Inventory Risk Distribution"
        )

        st.bar_chart(
            risk_counts
        )


# ============================================================
# LOW STOCK
# ============================================================

st.divider()

st.header("⚠️ Low Stock Products")

low_stock = load_sheet(
    "Low Stock"
)

if not low_stock.empty:

    st.dataframe(
        low_stock,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "No low-stock products identified."
    )


# ============================================================
# DEAD STOCK
# ============================================================

st.divider()

st.header("💤 Dead Stock")

dead_stock = load_sheet(
    "Dead Stock"
)

if not dead_stock.empty:

    st.dataframe(
        dead_stock,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "No dead-stock products identified."
    )


# ============================================================
# OVERSTOCK
# ============================================================

st.divider()

st.header("📦 Overstock Products")

overstock = load_sheet(
    "Overstock"
)

if not overstock.empty:

    st.dataframe(
        overstock,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No overstock products found."
    )


# ============================================================
# BUSINESS INTERPRETATION
# ============================================================

st.divider()

st.header("💡 Product & Inventory Insights")

st.info(
    """
**Product Performance**

Product-level analysis helps identify products generating
the highest revenue and profit.

**ABC Analysis**

ABC classification separates products according to their
contribution to business revenue.

**Inventory Risk**

Inventory risk highlights products that may require
management attention.

**Sales Velocity**

Sales velocity helps identify products moving quickly.

**Inventory Management**

Low-stock, dead-stock and overstock analysis can support
better purchasing and inventory decisions.
"""
)