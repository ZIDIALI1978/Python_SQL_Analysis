import streamlit as st
import pandas as pd
import os


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Retail E-Commerce Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# FILE
# ============================================================

base_folder = os.path.dirname(os.path.abspath(__file__))

excel_file = os.path.join(
    base_folder,
    "Retail_ECommerce_Final_Portfolio.xlsx"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    sales = pd.read_excel(
        excel_file,
        sheet_name="Sales Master"
    )

    orders = pd.read_excel(
        excel_file,
        sheet_name="Orders"
    )

    customers = pd.read_excel(
        excel_file,
        sheet_name="Customers"
    )

    products = pd.read_excel(
        excel_file,
        sheet_name="Products"
    )

    return sales, orders, customers, products


if not os.path.exists(excel_file):

    st.error(
        "Retail_ECommerce_Final_Portfolio.xlsx not found."
    )

    st.stop()


sales, orders, customers, products = load_data()


# ============================================================
# TITLE
# ============================================================

st.title("📊 Retail E-Commerce Analytics Dashboard")

st.caption(
    "Interactive Business Intelligence Dashboard | "
    "Python + SQL Server + Pandas + Streamlit"
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Dashboard Filters")


# ------------------------------------------------------------
# Category Filter
# ------------------------------------------------------------

category_column = None

for column in [
    "CategoryName",
    "Category",
    "CategoryID"
]:

    if column in sales.columns:

        category_column = column
        break


if category_column:

    categories = sorted(
        sales[category_column]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_categories = st.sidebar.multiselect(
        "Category",
        categories,
        default=categories
    )

else:

    selected_categories = []


# ------------------------------------------------------------
# Payment Method Filter
# ------------------------------------------------------------

payment_column = None

for column in [
    "PaymentMethod",
    "Payment Method"
]:

    if column in sales.columns:

        payment_column = column
        break


if payment_column:

    payment_methods = sorted(
        sales[payment_column]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_payment_methods = st.sidebar.multiselect(
        "Payment Method",
        payment_methods,
        default=payment_methods
    )

else:

    selected_payment_methods = []


# ------------------------------------------------------------
# Order Status Filter
# ------------------------------------------------------------

status_column = None

for column in [
    "Status",
    "OrderStatus"
]:

    if column in orders.columns:

        status_column = column
        break


if status_column:

    statuses = sorted(
        orders[status_column]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_statuses = st.sidebar.multiselect(
        "Order Status",
        statuses,
        default=statuses
    )

else:

    selected_statuses = []


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_sales = sales.copy()

filtered_orders = orders.copy()


if category_column and selected_categories:

    filtered_sales = filtered_sales[
        filtered_sales[category_column]
        .astype(str)
        .isin(selected_categories)
    ]


if payment_column and selected_payment_methods:

    filtered_sales = filtered_sales[
        filtered_sales[payment_column]
        .astype(str)
        .isin(selected_payment_methods)
    ]


if status_column and selected_statuses:

    filtered_orders = filtered_orders[
        filtered_orders[status_column]
        .astype(str)
        .isin(selected_statuses)
    ]


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_revenue = (
    filtered_sales["Revenue"].sum()
    if "Revenue" in filtered_sales.columns
    else 0
)


total_profit = (
    filtered_sales["TotalProfit"].sum()
    if "TotalProfit" in filtered_sales.columns
    else 0
)

total_orders = (
    filtered_orders["OrderID"].nunique()
    if "OrderID" in filtered_orders.columns
    else 0
)


total_customers = (
    filtered_sales["CustomerID"].nunique()
    if "CustomerID" in filtered_sales.columns
    else 0
)


total_products = (
    filtered_sales["ProductID"].nunique()
    if "ProductID" in filtered_sales.columns
    else 0
)


aov = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)


# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📌 Executive Overview")


col1, col2, col3, col4, col5, col6 = st.columns(6)


with col1:

    st.metric(
        "💰 Revenue",
        f"${total_revenue:,.2f}"
    )


with col2:

    st.metric(
        "📈 Profit",
        f"${total_profit:,.2f}"
    )


with col3:

    st.metric(
        "🛒 Orders",
        f"{total_orders:,}"
    )


with col4:

    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )


with col5:

    st.metric(
        "📦 Products",
        f"{total_products:,}"
    )


with col6:

    st.metric(
        "💵 AOV",
        f"${aov:,.2f}"
    )


# ============================================================
# SALES ANALYSIS
# ============================================================

st.divider()

st.subheader("💰 Sales Performance")


left, right = st.columns(2)


# ============================================================
# MONTHLY REVENUE
# ============================================================

with left:

    if "OrderDate" in filtered_sales.columns:

        filtered_sales["OrderDate"] = pd.to_datetime(
            filtered_sales["OrderDate"],
            errors="coerce"
        )

        monthly = (
            filtered_sales
            .dropna(subset=["OrderDate"])
            .assign(
                Month=lambda x:
                x["OrderDate"].dt.to_period("M").astype(str)
            )
            .groupby("Month")["Revenue"]
            .sum()
            .reset_index()
        )

        st.markdown("### 📈 Monthly Revenue")

        st.line_chart(
            monthly.set_index("Month")["Revenue"]
        )

    else:

        st.info(
            "OrderDate column not available."
        )


# ============================================================
# CATEGORY REVENUE
# ============================================================

with right:

    if category_column:

        category_revenue = (
            filtered_sales
            .groupby(category_column)["Revenue"]
            .sum()
            .sort_values(ascending=False)
        )

        st.markdown("### 🏷️ Revenue by Category")

        st.bar_chart(
            category_revenue
        )

    else:

        st.info(
            "Category information not available."
        )


# ============================================================
# TOP PRODUCTS
# ============================================================

st.divider()

st.subheader("🏆 Top Products")


product_column = None

for column in [
    "ProductName",
    "Product"
]:

    if column in filtered_sales.columns:

        product_column = column
        break


if product_column:

    top_products = (
        filtered_sales
        .groupby(product_column)["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(
        top_products
    )

else:

    st.info(
        "Product name column not available."
    )


# ============================================================
# PROFIT ANALYSIS
# ============================================================

st.divider()

st.subheader("📈 Profit Analysis")


if product_column and "TotalProfit" in filtered_sales.columns:

    top_profit_products = (
        filtered_sales
        .groupby(product_column)["TotalProfit"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(
        top_profit_products
    )

else:

    st.info(
        "Profit/Product information not available."
    )


# ============================================================
# DATA SUMMARY
# ============================================================

st.divider()

st.subheader("📋 Filtered Sales Data")

st.dataframe(
    filtered_sales.head(100),
    use_container_width=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Retail E-Commerce Analytics | "
    "SQL Server • Python • Pandas • Streamlit"
)

# ============================================================
# CUSTOMER INTELLIGENCE
# ============================================================

st.divider()

st.header("👥 Customer Intelligence")


# ============================================================
# RFM ANALYSIS
# ============================================================

st.subheader("🎯 RFM Customer Segmentation")


rfm_sheet = "RFM Segment Counts"


try:

    rfm_data = pd.read_excel(
        excel_file,
        sheet_name=rfm_sheet
    )

    st.write(
        "Customer distribution across RFM segments:"
    )

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # RFM TABLE
    # --------------------------------------------------------

    with col1:

        st.dataframe(
            rfm_data,
            use_container_width=True,
            hide_index=True
        )


    # --------------------------------------------------------
    # RFM CHART
    # --------------------------------------------------------

    with col2:

        if len(rfm_data.columns) >= 2:

            rfm_chart_data = rfm_data.set_index(
                rfm_data.columns[0]
            )

            st.bar_chart(
                rfm_chart_data[
                    rfm_data.columns[1]
                ]
            )

except Exception as e:

    st.warning(
        f"RFM analysis could not be loaded: {e}"
    )


# ============================================================
# CLV ANALYSIS
# ============================================================

st.divider()

st.subheader("💎 Customer Lifetime Value")


try:

    clv_data = pd.read_excel(
        excel_file,
        sheet_name="Customer CLV"
    )

    st.write(
        "Top customers based on estimated baseline CLV:"
    )


    # Detect CLV column

    clv_column = None

    for column in [
        "CLV",
        "CustomerCLV",
        "EstimatedCLV",
        "BaselineCLV"
    ]:

        if column in clv_data.columns:

            clv_column = column
            break


    # Detect customer name

    customer_name_column = None

    for column in [
        "CustomerName",
        "Customer",
        "CustomerID"
    ]:

        if column in clv_data.columns:

            customer_name_column = column
            break


    if clv_column:

        top_clv = (
            clv_data
            .sort_values(
                clv_column,
                ascending=False
            )
            .head(10)
        )


        if customer_name_column:

            top_clv_chart = (
                top_clv[
                    [
                        customer_name_column,
                        clv_column
                    ]
                ]
                .set_index(
                    customer_name_column
                )
            )

            st.bar_chart(
                top_clv_chart
            )


        st.dataframe(
            top_clv,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "CLV column was not found in Customer CLV sheet."
        )


except Exception as e:

    st.warning(
        f"CLV analysis could not be loaded: {e}"
    )


# ============================================================
# COHORT RETENTION
# ============================================================

st.divider()

st.subheader("🔄 Cohort Customer Retention")


try:

    cohort_data = pd.read_excel(
        excel_file,
        sheet_name="Retention Matrix",
        index_col=0
    )


    # Remove completely empty columns

    cohort_data = cohort_data.dropna(
        axis=1,
        how="all"
    )


    # Remove completely empty rows

    cohort_data = cohort_data.dropna(
        axis=0,
        how="all"
    )


    st.write(
        "Customer retention percentage by cohort and month."
    )


    st.dataframe(
        cohort_data.style.format(
            "{:.1f}%"
        ),
        use_container_width=True
    )


except Exception as e:

    st.warning(
        f"Cohort retention could not be loaded: {e}"
    )


# ============================================================
# CUSTOMER INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Customer Insights")


st.info(
    """
    **RFM Analysis:** Customers are segmented according to
    Recency, Frequency and Monetary behavior.

    **CLV Analysis:** Customer Lifetime Value provides a
    baseline estimate of the economic value of customers.

    **Cohort Analysis:** Retention analysis shows how customer
    purchasing behavior changes after their first purchase.

    These three analyses can be used together to identify
    valuable customers, retention opportunities and customers
    requiring re-engagement.
    """
)



# ============================================================
# PRODUCT & INVENTORY INTELLIGENCE
# ============================================================

st.divider()

st.header("📦 Product & Inventory Intelligence")


# ============================================================
# PRODUCT SCORECARD
# ============================================================

st.subheader("🏆 Product Performance")


try:

    product_scorecard = pd.read_excel(
        excel_file,
        sheet_name="Product Scorecard"
    )

    st.dataframe(
        product_scorecard,
        use_container_width=True,
        hide_index=True
    )

except Exception as e:

    st.warning(
        f"Product Scorecard could not be loaded: {e}"
    )


# ============================================================
# ABC ANALYSIS
# ============================================================

st.divider()

st.subheader("📊 ABC Inventory Analysis")


try:

    # Read without assuming the first row is the header
    abc_raw = pd.read_excel(
        excel_file,
        sheet_name="ABC Analysis",
        header=None
    )

    # --------------------------------------------------------
    # Find the actual header row
    # --------------------------------------------------------

    header_row = None

    for i in range(
        min(len(abc_raw), 15)
    ):

        row_values = (
            abc_raw.iloc[i]
            .astype(str)
            .str.strip()
            .str.lower()
            .tolist()
        )

        if any(
            "abc" in value
            for value in row_values
        ):

            header_row = i
            break


    if header_row is None:

        st.warning(
            "ABC Analysis header row could not be detected."
        )

    else:

        # ----------------------------------------------------
        # Re-read using detected header
        # ----------------------------------------------------

        abc_data = pd.read_excel(
            excel_file,
            sheet_name="ABC Analysis",
            header=header_row
        )


        # Remove completely empty columns

        abc_data = abc_data.dropna(
            axis=1,
            how="all"
        )


        # Remove completely empty rows

        abc_data = abc_data.dropna(
            axis=0,
            how="all"
        )


        # Clean column names

        abc_data.columns = [
            str(column).strip()
            for column in abc_data.columns
        ]


        st.write(
            "ABC analysis based on product revenue contribution."
        )


        # ----------------------------------------------------
        # Find ABC column
        # ----------------------------------------------------

        abc_class_column = None

        for column in abc_data.columns:

            column_text = (
                str(column)
                .strip()
                .lower()
                .replace("_", " ")
            )

            if (
                column_text == "abc"
                or
                "abc class" in column_text
                or
                "abc_class" in column_text
                or
                column_text == "class"
            ):

                abc_class_column = column
                break


        # ----------------------------------------------------
        # If exact column still not found,
        # check first few columns
        # ----------------------------------------------------

        if abc_class_column is None:

            for column in abc_data.columns:

                values = (
                    abc_data[column]
                    .dropna()
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    .unique()
                    .tolist()
                )

                if any(
                    value in ["A", "B", "C"]
                    for value in values
                ):

                    abc_class_column = column
                    break


        # ----------------------------------------------------
        # Display ABC analysis
        # ----------------------------------------------------

        if abc_class_column:

            col1, col2 = st.columns(2)


            # ------------------------------------------------
            # TABLE
            # ------------------------------------------------

            with col1:

                st.markdown(
                    "### ABC Analysis Table"
                )

                st.dataframe(
                    abc_data,
                    use_container_width=True,
                    hide_index=True
                )


            # ------------------------------------------------
            # CHART
            # ------------------------------------------------

            with col2:

                st.markdown(
                    "### Products by ABC Class"
                )


                abc_counts = (
                    abc_data[
                        abc_class_column
                    ]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    .value_counts()
                    .reindex(
                        ["A", "B", "C"],
                        fill_value=0
                    )
                )


                st.bar_chart(
                    abc_counts
                )


            # ------------------------------------------------
            # ABC SUMMARY
            # ------------------------------------------------

            st.markdown(
                "### 📌 ABC Summary"
            )


            summary_cols = st.columns(3)


            for col, abc_class in zip(
                summary_cols,
                ["A", "B", "C"]
            ):

                count = int(
                    abc_counts.get(
                        abc_class,
                        0
                    )
                )

                with col:

                    st.metric(
                        f"Class {abc_class}",
                        f"{count:,} products"
                    )


        else:

            st.warning(
                "ABC class column could not be identified."
            )

            st.write(
                "Detected columns:"
            )

            st.write(
                abc_data.columns.tolist()
            )


except Exception as e:

    st.warning(
        f"ABC Analysis could not be loaded: {e}"
    )

# ============================================================
# INVENTORY RISK
# ============================================================

st.divider()

st.subheader("⚠️ Inventory Risk")


try:

    inventory_risk = pd.read_excel(
        excel_file,
        sheet_name="Inventory Risk"
    )

    col1, col2 = st.columns(2)


    with col1:

        st.dataframe(
            inventory_risk,
            use_container_width=True,
            hide_index=True
        )


    with col2:

        if len(inventory_risk.columns) >= 2:

            risk_column = inventory_risk.columns[0]

            product_count_column = (
                inventory_risk.columns[1]
            )

            risk_chart = (
                inventory_risk[
                    [
                        risk_column,
                        product_count_column
                    ]
                ]
                .set_index(
                    risk_column
                )
            )

            st.bar_chart(
                risk_chart
            )


except Exception as e:

    st.warning(
        f"Inventory Risk could not be loaded: {e}"
    )


# ============================================================
# TOP PROFIT PRODUCTS
# ============================================================

st.divider()

st.subheader("💰 Top Profit Products")


try:

    top_profit = pd.read_excel(
        excel_file,
        sheet_name="Top Profit Products_2"
    )

    st.dataframe(
        top_profit.head(10),
        use_container_width=True,
        hide_index=True
    )

except Exception as e:

    st.warning(
        f"Top Profit Products could not be loaded: {e}"
    )


# ============================================================
# TOP SALES VELOCITY
# ============================================================

st.divider()

st.subheader("🚀 Top Sales Velocity")


try:

    sales_velocity = pd.read_excel(
        excel_file,
        sheet_name="Top Sales Velocity"
    )

    st.dataframe(
        sales_velocity.head(10),
        use_container_width=True,
        hide_index=True
    )

except Exception as e:

    st.warning(
        f"Sales Velocity could not be loaded: {e}"
    )


# ============================================================
# LOW STOCK
# ============================================================

st.divider()

st.subheader("🚨 Low Stock Products")


try:

    low_stock = pd.read_excel(
        excel_file,
        sheet_name="Low Stock"
    )

    if low_stock.empty:

        st.success(
            "No low-stock products detected."
        )

    else:

        st.dataframe(
            low_stock,
            use_container_width=True,
            hide_index=True
        )

except Exception as e:

    st.warning(
        f"Low Stock analysis could not be loaded: {e}"
    )


# ============================================================
# DEAD STOCK
# ============================================================

st.divider()

st.subheader("💀 Dead Stock Products")


try:

    dead_stock = pd.read_excel(
        excel_file,
        sheet_name="Dead Stock"
    )

    if dead_stock.empty:

        st.success(
            "No dead-stock products detected."
        )

    else:

        st.dataframe(
            dead_stock,
            use_container_width=True,
            hide_index=True
        )

except Exception as e:

    st.warning(
        f"Dead Stock analysis could not be loaded: {e}"
    )


# ============================================================
# OVERSTOCK
# ============================================================

st.divider()

st.subheader("📦 Overstock Products")


try:

    overstock = pd.read_excel(
        excel_file,
        sheet_name="Overstock"
    )

    st.dataframe(
        overstock.head(20),
        use_container_width=True,
        hide_index=True
    )

except Exception as e:

    st.warning(
        f"Overstock analysis could not be loaded: {e}"
    )


# ============================================================
# PRODUCT & INVENTORY INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Product & Inventory Insights")


st.info(
    """
    **ABC Analysis:** Products are classified according to
    their contribution to revenue.

    **Inventory Risk:** Current inventory levels are evaluated
    to identify healthy, overstock and out-of-stock products.

    **Sales Velocity:** High-velocity products indicate items
    generating stronger sales activity.

    **Profit Analysis:** Top-profit products help identify
    products contributing strongly to business profitability.

    **Inventory Actions:** Low-stock, dead-stock and
    overstock analysis can support better purchasing and
    inventory management decisions.
    """
)



# ============================================================
# SUPPLIER & OPERATIONS INTELLIGENCE
# ============================================================

st.divider()

st.header("🚚 Supplier & Operations Intelligence")


# ============================================================
# SUPPLIER PERFORMANCE
# ============================================================

st.subheader("🏢 Supplier Performance")

try:

    supplier_data = pd.read_excel(
        excel_file,
        sheet_name="Supplier Scorecard"
    )

    st.dataframe(
        supplier_data,
        use_container_width=True,
        hide_index=True
    )

except Exception as e:

    st.warning(
        f"Supplier Scorecard could not be loaded: {e}"
    )


# ============================================================
# DELIVERY SUMMARY
# ============================================================

st.divider()

st.subheader("📦 Delivery Performance")

try:

    delivery_summary = pd.read_excel(
        excel_file,
        sheet_name="Delivery Summary"
    )

    # Display summary table

    st.dataframe(
        delivery_summary,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # Delivery KPIs
    # --------------------------------------------------------

    delivery_metrics = {}

    for _, row in delivery_summary.iterrows():

        if len(row) >= 2:

            metric = str(row.iloc[0]).strip()
            value = row.iloc[1]

            delivery_metrics[metric] = value


    col1, col2, col3 = st.columns(3)


    # Total Shipments

    total_shipments = delivery_metrics.get(
        "Total Shipments",
        0
    )

    with col1:

        st.metric(
            "📦 Total Shipments",
            f"{total_shipments:,.0f}"
            if pd.notna(total_shipments)
            else "0"
        )


        # Delivered

    delivered = delivery_metrics.get(
        "Delivered Shipments",
        0
    )

    with col2:
        st.metric(
            "✅ Delivered",
            f"{delivered:,.0f}"
            if pd.notna(delivered)
            else "0"
        )

    # Average Delivery Days

    avg_delivery = delivery_metrics.get(
        "Average Delivery Days",
        0
    )

    with col3:

        st.metric(
            "⏱️ Avg Delivery Days",
            f"{avg_delivery:.2f}"
            if pd.notna(avg_delivery)
            else "N/A"
        )


except Exception as e:

    st.warning(
        f"Delivery Summary could not be loaded: {e}"
    )


# ============================================================
# COURIER PERFORMANCE
# ============================================================

st.divider()

st.subheader("🚛 Courier Performance")

try:

    courier_data = pd.read_excel(
        excel_file,
        sheet_name="Courier Performance"
    )

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # Courier Table
    # --------------------------------------------------------

    with col1:

        st.dataframe(
            courier_data,
            use_container_width=True,
            hide_index=True
        )


    # --------------------------------------------------------
    # Courier Chart
    # --------------------------------------------------------

    with col2:

        if len(courier_data.columns) >= 3:

            courier_column = (
                courier_data.columns[0]
            )

            delivery_days_column = (
                courier_data.columns[2]
            )

            courier_chart = (
                courier_data[
                    [
                        courier_column,
                        delivery_days_column
                    ]
                ]
                .dropna()
                .set_index(
                    courier_column
                )
            )

            st.markdown(
                "### Average Delivery Days by Courier"
            )

            st.bar_chart(
                courier_chart
            )


except Exception as e:

    st.warning(
        f"Courier Performance could not be loaded: {e}"
    )


# ============================================================
# COURIER STATUS
# ============================================================

st.divider()

st.subheader("📊 Shipment Status")

try:

    courier_status = pd.read_excel(
        excel_file,
        sheet_name="Courier Status"
    )

    st.dataframe(
        courier_status,
        use_container_width=True,
        hide_index=True
    )


    if len(courier_status.columns) >= 2:

        status_column = (
            courier_status.columns[0]
        )

        count_column = (
            courier_status.columns[1]
        )

        status_chart = (
            courier_status[
                [
                    status_column,
                    count_column
                ]
            ]
            .dropna()
            .set_index(
                status_column
            )
        )

        st.bar_chart(
            status_chart
        )


except Exception as e:

    st.warning(
        f"Courier Status could not be loaded: {e}"
    )


# ============================================================
# OPERATIONS INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Operations Insights")

st.info(
    """
    **Supplier Performance:** Supplier scorecards provide
    visibility into product supply and inventory value.

    **Delivery Performance:** Shipment records show actual
    delivery activity and average delivery duration.

    **Courier Performance:** Courier-level analysis helps
    compare average delivery times.

    **Shipment Status:** Delivered and pending shipments
    provide visibility into current operational workload.

    **Important limitation:** Expected delivery dates are not
    available in the source shipment data, so on-time and
    delayed delivery percentages are not calculated.
    """
)