import streamlit as st
import pandas as pd
import os


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Operations & Suppliers",
    page_icon="🚚",
    layout="wide"
)


# ============================================================
# PROJECT FILE
# ============================================================
base_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
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
# HELPER
# ============================================================

def load_sheet(sheet_name):

    try:

        df = pd.read_excel(
            excel_file,
            sheet_name=sheet_name
        )

        df = df.dropna(
            axis=0,
            how="all"
        )

        df = df.dropna(
            axis=1,
            how="all"
        )

        df.columns = [
            str(col).strip()
            for col in df.columns
        ]

        return df

    except Exception as e:

        st.warning(
            f"Could not load '{sheet_name}': {e}"
        )

        return pd.DataFrame()


# ============================================================
# TITLE
# ============================================================

st.title("🚚 Operations & Supplier Intelligence")

st.caption(
    "Supplier performance, delivery analysis and courier performance"
)


# ============================================================
# SUPPLIER SCORECARD
# ============================================================

st.header("🏭 Supplier Performance")

supplier_data = load_sheet(
    "Supplier Scorecard"
)

if not supplier_data.empty:

    st.dataframe(
        supplier_data,
        use_container_width=True,
        hide_index=True
    )

    numeric_columns = supplier_data.select_dtypes(
        include="number"
    ).columns.tolist()

    # --------------------------------------------------------
    # Supplier KPIs
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🏭 Suppliers",
            f"{len(supplier_data):,}"
        )

    with col2:

        if numeric_columns:

            first_numeric = numeric_columns[0]

            st.metric(
                "📊 Total",
                f"{supplier_data[first_numeric].sum():,.0f}"
            )

    with col3:

        if numeric_columns:

            first_numeric = numeric_columns[0]

            st.metric(
                "📈 Average",
                f"{supplier_data[first_numeric].mean():,.2f}"
            )


# ============================================================
# DELIVERY SUMMARY
# ============================================================

st.divider()

st.header("📦 Delivery Summary")

delivery_summary = load_sheet(
    "Delivery Summary"
)

if not delivery_summary.empty:

    st.dataframe(
        delivery_summary,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # Detect values
    # --------------------------------------------------------

    summary_dict = {}

    for _, row in delivery_summary.iterrows():

        if len(row) >= 2:

            key = str(row.iloc[0]).strip()

            value = row.iloc[1]

            summary_dict[key] = value

    # --------------------------------------------------------
    # KPI cards
    # --------------------------------------------------------

    total_shipments = summary_dict.get(
        "Total Shipments"
    )

    delivered = summary_dict.get(
        "Delivered"
    )

    pending = summary_dict.get(
        "Pending"
    )

    avg_delivery = summary_dict.get(
        "Average Delivery Days"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        if pd.notna(total_shipments):

            st.metric(
                "📦 Total Shipments",
                f"{float(total_shipments):,.0f}"
            )

    with col2:

        if pd.notna(delivered):

            st.metric(
                "✅ Delivered",
                f"{float(delivered):,.0f}"
            )

    with col3:

        if pd.notna(pending):

            st.metric(
                "⏳ Pending",
                f"{float(pending):,.0f}"
            )

    with col4:

        if pd.notna(avg_delivery):

            st.metric(
                "🚚 Avg Delivery Days",
                f"{float(avg_delivery):,.2f}"
            )


# ============================================================
# COURIER PERFORMANCE
# ============================================================

st.divider()

st.header("🚚 Courier Performance")

courier_data = load_sheet(
    "Courier Performance"
)

if not courier_data.empty:

    st.dataframe(
        courier_data,
        use_container_width=True,
        hide_index=True
    )

    numeric_columns = courier_data.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:

        # ----------------------------------------------------
        # Find delivery-days column
        # ----------------------------------------------------

        delivery_days_column = next(
            (
                col
                for col in numeric_columns
                if "delivery" in str(col).lower()
                and "day" in str(col).lower()
            ),
            None
        )

        if delivery_days_column is None:

            delivery_days_column = numeric_columns[-1]

        # ----------------------------------------------------
        # Find courier/name column
        # ----------------------------------------------------

        text_columns = courier_data.select_dtypes(
            exclude="number"
        ).columns.tolist()

        if text_columns:

            courier_column = text_columns[0]

            chart_data = (
                courier_data[
                    [
                        courier_column,
                        delivery_days_column
                    ]
                ]
                .set_index(courier_column)
            )

            st.subheader(
                "Average Delivery Days by Courier"
            )

            st.bar_chart(
                chart_data
            )


# ============================================================
# COURIER STATUS
# ============================================================

st.divider()

st.header("📊 Courier Status")

courier_status = load_sheet(
    "Courier Status"
)

if not courier_status.empty:

    st.dataframe(
        courier_status,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # Detect status column
    # --------------------------------------------------------

    status_column = None

    for column in courier_status.columns:

        column_text = (
            str(column)
            .strip()
            .lower()
        )

        if (
            "status" in column_text
            or "courier" in column_text
        ):

            status_column = column
            break

    if status_column:

        status_counts = (
            courier_status[status_column]
            .astype(str)
            .value_counts()
        )

        st.subheader(
            "Status Distribution"
        )

        st.bar_chart(
            status_counts
        )


# ============================================================
# OPERATIONS INSIGHTS
# ============================================================

st.divider()

st.header("💡 Operations Insights")

st.info(
    """
**Supplier Performance**

Supplier analysis helps identify suppliers contributing
significant inventory value.

**Delivery Performance**

Delivery analysis shows shipment volume, delivered orders,
pending shipments and average delivery time.

**Courier Performance**

Courier-level comparison helps identify faster and slower
delivery partners.

**Operational Decision Making**

These metrics can support supplier evaluation, courier
selection and logistics improvement.
"""
)


# ============================================================
# IMPORTANT DATA LIMITATION
# ============================================================

with st.expander("⚠️ Data Limitation"):

    st.write(
        """
The current shipment data contains ShippingDate and
DeliveryDate, but it does not contain an
ExpectedDeliveryDate.

Therefore, the dashboard does not calculate a true
On-Time Delivery percentage or Delay percentage.

Average delivery days and shipment status are reported
directly from the available data.
"""
    )