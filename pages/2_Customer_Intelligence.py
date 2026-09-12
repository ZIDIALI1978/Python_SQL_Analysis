import streamlit as st
import pandas as pd
import os


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Customer Intelligence",
    page_icon="👥",
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
# TITLE
# ============================================================

st.title("👥 Customer Intelligence")

st.caption(
    "RFM segmentation, Customer Lifetime Value and cohort retention"
)


# ============================================================
# RFM ANALYSIS
# ============================================================

st.header("🎯 RFM Customer Segmentation")


try:

    rfm_data = pd.read_excel(
        excel_file,
        sheet_name="RFM Segment Counts"
    )


    # --------------------------------------------------------
    # Clean data
    # --------------------------------------------------------

    rfm_data = rfm_data.dropna(
        axis=1,
        how="all"
    )

    rfm_data = rfm_data.dropna(
        axis=0,
        how="all"
    )

    rfm_data.columns = [
        str(column).strip()
        for column in rfm_data.columns
    ]


    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    if len(rfm_data.columns) >= 2:

        segment_column = rfm_data.columns[0]
        count_column = rfm_data.columns[1]


        col1, col2 = st.columns(2)


        # ----------------------------------------------------
        # RFM TABLE
        # ----------------------------------------------------

        with col1:

            st.subheader("Customer Segments")

            st.dataframe(
                rfm_data,
                use_container_width=True,
                hide_index=True
            )


        # ----------------------------------------------------
        # RFM CHART
        # ----------------------------------------------------

        with col2:

            st.subheader(
                "Customers by RFM Segment"
            )

            rfm_chart = (
                rfm_data[
                    [
                        segment_column,
                        count_column
                    ]
                ]
                .set_index(
                    segment_column
                )
            )

            st.bar_chart(
                rfm_chart
            )


        # ----------------------------------------------------
        # RFM KPI CARDS
        # ----------------------------------------------------

        st.subheader("📌 Segment Overview")

        kpi_columns = st.columns(
            min(len(rfm_data), 5)
        )


        for index, (_, row) in enumerate(
            rfm_data.iterrows()
        ):

            if index >= 5:
                break

            segment = str(
                row.iloc[0]
            )

            count = row.iloc[1]


            with kpi_columns[index]:

                st.metric(
                    segment,
                    f"{count:,.0f}"
                )


except Exception as e:

    st.warning(
        f"RFM analysis could not be loaded: {e}"
    )


# ============================================================
# CLV ANALYSIS
# ============================================================

st.divider()

st.header("💎 Customer Lifetime Value")


try:

    clv_data = pd.read_excel(
        excel_file,
        sheet_name="Customer CLV"
    )


    # --------------------------------------------------------
    # Clean
    # --------------------------------------------------------

    clv_data = clv_data.dropna(
        axis=1,
        how="all"
    )

    clv_data = clv_data.dropna(
        axis=0,
        how="all"
    )


    clv_data.columns = [
        str(column).strip()
        for column in clv_data.columns
    ]


    # --------------------------------------------------------
    # Find CLV column
    # --------------------------------------------------------

    clv_column = None

    for column in clv_data.columns:

        column_text = (
            str(column)
            .strip()
            .lower()
            .replace("_", "")
            .replace(" ", "")
        )

        if (
            "clv" in column_text
            or
            "customervalifetimevalue"
            in column_text
        ):

            clv_column = column
            break


    # --------------------------------------------------------
    # Find customer column
    # --------------------------------------------------------

    customer_column = None

    for column in [
        "CustomerName",
        "Customer",
        "CustomerID"
    ]:

        if column in clv_data.columns:

            customer_column = column
            break


    if clv_column:

        # Convert CLV to numeric

        clv_data[clv_column] = pd.to_numeric(
            clv_data[clv_column],
            errors="coerce"
        )


        # ----------------------------------------------------
        # CLV KPIs
        # ----------------------------------------------------

        total_clv = clv_data[
            clv_column
        ].sum()

        average_clv = clv_data[
            clv_column
        ].mean()

        highest_clv = clv_data[
            clv_column
        ].max()


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "💰 Total Customer CLV",
                f"${total_clv:,.2f}"
            )


        with col2:

            st.metric(
                "📊 Average CLV",
                f"${average_clv:,.2f}"
            )


        with col3:

            st.metric(
                "🏆 Highest CLV",
                f"${highest_clv:,.2f}"
            )


        # ----------------------------------------------------
        # TOP CLV CUSTOMERS
        # ----------------------------------------------------

        st.subheader(
            "🏆 Top 10 Customers by CLV"
        )


        top_clv = (
            clv_data
            .sort_values(
                clv_column,
                ascending=False
            )
            .head(10)
        )


        if customer_column:

            clv_chart = (
                top_clv[
                    [
                        customer_column,
                        clv_column
                    ]
                ]
                .set_index(
                    customer_column
                )
            )

            st.bar_chart(
                clv_chart
            )


        st.dataframe(
            top_clv,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "CLV column could not be identified."
        )

        st.write(
            "Available columns:"
        )

        st.write(
            clv_data.columns.tolist()
        )


except Exception as e:

    st.warning(
        f"CLV analysis could not be loaded: {e}"
    )


# ============================================================
# COHORT CUSTOMER RETENTION
# ============================================================

st.divider()

st.header("📅 Cohort Customer Retention")

try:

    # --------------------------------------------------------
    # Load Retention Matrix
    # --------------------------------------------------------

    retention_raw = pd.read_excel(
        excel_file,
        sheet_name="Retention Matrix",
        header=None
    )

    # Remove completely empty rows and columns
    retention_raw = retention_raw.dropna(
        how="all"
    )

    retention_raw = retention_raw.dropna(
        axis=1,
        how="all"
    )

    # --------------------------------------------------------
    # Detect header row
    # --------------------------------------------------------

    header_row = None

    for i in range(min(15, len(retention_raw))):

        row_values = (
            retention_raw.iloc[i]
            .astype(str)
            .str.strip()
            .str.lower()
            .tolist()
        )

        # Check for CohortIndex / Cohort / Month
        if (
            any("cohortindex" in value for value in row_values)
            or any("cohort index" in value for value in row_values)
            or any("cohort" in value for value in row_values)
            or any("month" in value for value in row_values)
        ):

            header_row = i
            break

    # --------------------------------------------------------
    # If header found
    # --------------------------------------------------------

    if header_row is not None:

        retention_data = pd.read_excel(
            excel_file,
            sheet_name="Retention Matrix",
            header=header_row,
            index_col=0
        )

        # Remove empty rows/columns
        retention_data = retention_data.dropna(
            axis=0,
            how="all"
        )

        retention_data = retention_data.dropna(
            axis=1,
            how="all"
        )

        # Clean column names
        retention_data.columns = [
            str(column).strip()
            for column in retention_data.columns
        ]

        # Remove unnamed columns
        retention_data = retention_data.loc[
            :,
            ~retention_data.columns.str.contains(
                "^Unnamed",
                case=False,
                regex=True
            )
        ]

        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        st.write(
            "Customer retention percentage by cohort month."
        )

        st.dataframe(
            retention_data.style.format(
                "{:.1f}%"
            ),
            use_container_width=True
        )

    else:

        st.warning(
            "Retention Matrix header could not be detected."
        )

except Exception as e:

    st.warning(
        f"Cohort retention could not be loaded: {e}"
    )
# ============================================================
# CUSTOMER INSIGHTS
# ============================================================

st.divider()

st.header("💡 Customer Insights")


st.info(
    """
    **RFM Segmentation** identifies customers according to
    Recency, Frequency and Monetary behavior.

    **Customer Lifetime Value** provides a baseline estimate
    of the economic value generated by customers.

    **Cohort Retention** shows how customer purchasing behavior
    changes after their first purchase.

    Together, these analyses help identify high-value customers,
    loyal customers, new customers and customers requiring
    re-engagement.
    """
)


# ============================================================
# METHODOLOGY
# ============================================================

with st.expander("📘 Customer Analytics Methodology"):

    st.write(
        """
        **RFM**

        - Recency = how recently a customer purchased
        - Frequency = number of customer orders
        - Monetary = customer revenue contribution


        **CLV**

        The project uses a transparent baseline CLV model
        based on average order value, purchase frequency,
        gross margin and an assumed customer lifespan.


        **Cohort Analysis**

        Customers are grouped according to their first
        purchase month and tracked across subsequent months
        to measure retention.
        """
    )