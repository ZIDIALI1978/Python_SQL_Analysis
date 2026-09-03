import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment


# =========================================================
# STEP 1: DATABASE CONNECTION
# =========================================================

server = r"ZUBAIR\SQLEXPRESS"
database = "RetailECommerceDB"
driver = "ODBC Driver 17 for SQL Server"

connection_string = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
)

params = quote_plus(connection_string)

engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={params}"
)

print("Database connection created successfully.")


# =========================================================
# STEP 2: LOAD ORDERS
# =========================================================

orders_query = """
SELECT
    OrderID,
    CustomerID,
    OrderDate,
    Status
FROM Sales.Orders
"""

orders = pd.read_sql(orders_query, engine)

print("\nOrders Loaded:", len(orders))
print(orders.head())


# =========================================================
# STEP 3: LOAD ORDER ITEMS
# =========================================================

order_items_query = """
SELECT
    OrderItemID,
    OrderID,
    ProductID,
    Quantity,
    UnitPrice
FROM Sales.OrderItems
"""

order_items = pd.read_sql(order_items_query, engine)

print("\nOrder Items Loaded:", len(order_items))
print(order_items.head())


# =========================================================
# STEP 4: LOAD CUSTOMERS
# =========================================================

customers_query = """
SELECT
    CustomerID,
    FirstName,
    LastName,
    Email
FROM Sales.Customers
"""

customers = pd.read_sql(customers_query, engine)

print("\nCustomers Loaded:", len(customers))
print(customers.head())


# =========================================================
# STEP 5: CREATE CUSTOMER NAME
# =========================================================

customers["FirstName"] = customers["FirstName"].fillna("")
customers["LastName"] = customers["LastName"].fillna("")

customers["CustomerName"] = (
    customers["FirstName"] + " " + customers["LastName"]
).str.strip()

print("\nCustomer names created successfully.")


# =========================================================
# STEP 6: DATA TYPE VALIDATION
# =========================================================

orders["OrderDate"] = pd.to_datetime(
    orders["OrderDate"],
    errors="coerce"
)

order_items["Quantity"] = pd.to_numeric(
    order_items["Quantity"],
    errors="coerce"
)

order_items["UnitPrice"] = pd.to_numeric(
    order_items["UnitPrice"],
    errors="coerce"
)

print("\n================================")
print("DATA VALIDATION")
print("================================")

print("\nOrder Date Range:")
print("Minimum:", orders["OrderDate"].min())
print("Maximum:", orders["OrderDate"].max())

print("\nMissing Order Dates:")
print(orders["OrderDate"].isna().sum())

print("\nMissing Quantities:")
print(order_items["Quantity"].isna().sum())

print("\nMissing Unit Prices:")
print(order_items["UnitPrice"].isna().sum())


# =========================================================
# STEP 7: REMOVE INVALID RECORDS
# =========================================================

orders = orders.dropna(
    subset=["CustomerID", "OrderDate"]
)

order_items = order_items.dropna(
    subset=["OrderID", "Quantity", "UnitPrice"]
)

print("\nInvalid records removed successfully.")


# =========================================================
# STEP 8: CALCULATE REVENUE
# =========================================================

order_items["Revenue"] = (
    order_items["Quantity"] *
    order_items["UnitPrice"]
)

print("\nRevenue calculated successfully.")

print(
    order_items[
        [
            "OrderID",
            "Quantity",
            "UnitPrice",
            "Revenue"
        ]
    ].head()
)


# =========================================================
# STEP 9: MERGE ORDERS WITH ORDER ITEMS
# =========================================================

sales = orders.merge(
    order_items,
    on="OrderID",
    how="inner"
)

print("\nSales Data Created")
print("Rows:", len(sales))

print(
    sales[
        [
            "OrderID",
            "CustomerID",
            "OrderDate",
            "Quantity",
            "UnitPrice",
            "Revenue"
        ]
    ].head()
)


# =========================================================
# STEP 10: MERGE CUSTOMER INFORMATION
# =========================================================

sales = sales.merge(
    customers[
        [
            "CustomerID",
            "FirstName",
            "LastName",
            "CustomerName",
            "Email"
        ]
    ],
    on="CustomerID",
    how="left"
)

print("\nCustomer information merged.")

print(
    sales[
        [
            "CustomerID",
            "FirstName",
            "LastName",
            "CustomerName",
            "OrderDate",
            "Quantity",
            "Revenue"
        ]
    ].head()
)


# =========================================================
# STEP 11: DEFINE ANALYSIS DATE
# =========================================================

analysis_date = (
    sales["OrderDate"].max()
    + pd.Timedelta(days=1)
)

print("\nAnalysis Date:")
print(analysis_date)


# =========================================================
# STEP 12: RFM CUSTOMER ANALYSIS
# =========================================================

rfm = (
    sales
    .groupby("CustomerID")
    .agg(
        Recency=(
            "OrderDate",
            lambda x: (analysis_date - x.max()).days
        ),

        Frequency=(
            "OrderID",
            "nunique"
        ),

        Monetary=(
            "Revenue",
            "sum"
        ),

        FirstOrderDate=(
            "OrderDate",
            "min"
        ),

        LastOrderDate=(
            "OrderDate",
            "max"
        )
    )
    .reset_index()
)

print("\nRFM Data Created")
print(rfm.head())


# =========================================================
# STEP 13: CUSTOMER AOV
# =========================================================

rfm["AOV"] = (
    rfm["Monetary"] /
    rfm["Frequency"]
)

print("\nCustomer AOV calculated.")

print(rfm.head())


# =========================================================
# STEP 14: ADD CUSTOMER DETAILS
# =========================================================

rfm = rfm.merge(
    customers[
        [
            "CustomerID",
            "FirstName",
            "LastName",
            "CustomerName",
            "Email"
        ]
    ],
    on="CustomerID",
    how="left"
)

print("\nCustomer details added.")

print(
    rfm[
        [
            "CustomerID",
            "FirstName",
            "LastName",
            "CustomerName",
            "Recency",
            "Frequency",
            "Monetary",
            "AOV"
        ]
    ].head(10)
)


# =========================================================
# STEP 15: RFM SCORES
# =========================================================

# Recency:
# Lower recency is better.
# Therefore scores go from 5 (best) to 1 (worst).

rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    5,
    labels=[5, 4, 3, 2, 1]
).astype(int)


# Frequency:
# Higher frequency is better.

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)


# Monetary:
# Higher monetary value is better.

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)


print("\nRFM Scores Created.")

print(
    rfm[
        [
            "CustomerID",
            "CustomerName",
            "Recency",
            "Frequency",
            "Monetary",
            "R_Score",
            "F_Score",
            "M_Score"
        ]
    ].head(10)
)


# =========================================================
# STEP 16: OVERALL RFM SCORE
# =========================================================

rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)

print("\nRFM Score Created:")

print(
    rfm[
        [
            "CustomerID",
            "RFM_Score"
        ]
    ].head(10)
)


# =========================================================
# STEP 17: CUSTOMER SEGMENTATION
# =========================================================

def assign_segment(row):

    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]

    # Best customers
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    # Loyal customers
    elif r >= 3 and f >= 4:
        return "Loyal"

    # New / recent customers
    elif r >= 4 and f <= 2:
        return "New"

    # At risk customers
    elif r <= 2 and f >= 3:
        return "At Risk"

    # Lost / low engagement customers
    else:
        return "Lost"


rfm["Segment"] = rfm.apply(
    assign_segment,
    axis=1
)

print("\nCustomer Segments Created.")

print(
    rfm[
        [
            "CustomerID",
            "CustomerName",
            "R_Score",
            "F_Score",
            "M_Score",
            "RFM_Score",
            "Segment"
        ]
    ].head(20)
)


# =========================================================
# STEP 18: SEGMENT SUMMARY
# =========================================================

segment_summary = (
    rfm
    .groupby("Segment")
    .agg(
        Customers=("CustomerID", "count"),
        Revenue=("Monetary", "sum"),
        AverageRevenue=("Monetary", "mean"),
        AverageFrequency=("Frequency", "mean"),
        AverageRecency=("Recency", "mean"),
        AverageAOV=("AOV", "mean")
    )
    .reset_index()
)

print("\n================================")
print("RFM SEGMENT SUMMARY")
print("================================")

print(segment_summary)


# =========================================================
# STEP 19: CUSTOMER PERCENTAGE
# =========================================================

total_customers = segment_summary["Customers"].sum()
total_revenue = segment_summary["Revenue"].sum()

segment_summary["CustomerPercentage"] = (
    segment_summary["Customers"] /
    total_customers
) * 100

segment_summary["RevenuePercentage"] = (
    segment_summary["Revenue"] /
    total_revenue
) * 100

print("\nSegment percentages calculated.")

print(segment_summary)


# =========================================================
# STEP 20: TOP CHAMPIONS
# =========================================================

top_champions = (
    rfm[
        rfm["Segment"] == "Champions"
    ]
    .sort_values(
        "Monetary",
        ascending=False
    )
    .head(10)
)

print("\n================================")
print("TOP 10 CHAMPIONS")
print("================================")

print(
    top_champions[
        [
            "CustomerID",
            "CustomerName",
            "Recency",
            "Frequency",
            "Monetary",
            "AOV",
            "RFM_Score"
        ]
    ]
)


# =========================================================
# STEP 21: TOP AT-RISK CUSTOMERS
# =========================================================

at_risk = (
    rfm[
        rfm["Segment"] == "At Risk"
    ]
    .sort_values(
        "Monetary",
        ascending=False
    )
    .head(10)
)

print("\n================================")
print("TOP AT-RISK CUSTOMERS")
print("================================")

print(
    at_risk[
        [
            "CustomerID",
            "CustomerName",
            "Recency",
            "Frequency",
            "Monetary",
            "AOV",
            "RFM_Score"
        ]
    ]
)


# =========================================================
# STEP 22: SEGMENT CUSTOMER COUNTS
# =========================================================

segment_counts = (
    rfm["Segment"]
    .value_counts()
    .reset_index()
)

segment_counts.columns = [
    "Segment",
    "Customers"
]

print("\n================================")
print("CUSTOMERS BY SEGMENT")
print("================================")

print(segment_counts)


# =========================================================
# STEP 23: EXPORT CSV FILES
# =========================================================

rfm.to_csv(
    "rfm_customer_analysis.csv",
    index=False
)

segment_summary.to_csv(
    "rfm_segment_summary.csv",
    index=False
)

segment_counts.to_csv(
    "rfm_segment_counts.csv",
    index=False
)

print("\nRFM CSV files exported successfully.")


# =========================================================
# STEP 24: UPDATE EXCEL WORKBOOK
# =========================================================

import os
import shutil

input_excel = "Retail_ECommerce_Final_With_Insights.xlsx"
output_excel = "Retail_ECommerce_Final_With_RFM.xlsx"

print("\nUpdating Excel workbook...")

# Check whether the original workbook exists
if not os.path.exists(input_excel):
    raise FileNotFoundError(
        f"Input Excel file not found: {input_excel}"
    )

# Copy the existing workbook first
# This preserves the Dashboard, Business Insights,
# and all existing sheets/charts.
shutil.copy2(
    input_excel,
    output_excel
)

print("Original workbook copied successfully.")

# Now open the copied workbook and add RFM sheets
with pd.ExcelWriter(
    output_excel,
    engine="openpyxl",
    mode="a",
    if_sheet_exists="replace"
) as writer:

    rfm.to_excel(
        writer,
        sheet_name="RFM Customers",
        index=False
    )

    segment_summary.to_excel(
        writer,
        sheet_name="RFM Segments",
        index=False
    )

    segment_counts.to_excel(
        writer,
        sheet_name="RFM Segment Counts",
        index=False
    )

print("RFM sheets added successfully.")
# =========================================================
# STEP 25: FORMAT EXCEL WORKBOOK
# =========================================================

wb = load_workbook(output_excel)


# =========================================================
# FORMAT RFM CUSTOMERS
# =========================================================

ws = wb["RFM Customers"]

ws.freeze_panes = "A2"
ws.auto_filter.ref = ws.dimensions

for cell in ws[1]:

    cell.font = Font(
        bold=True,
        color="FFFFFF"
    )

    cell.fill = PatternFill(
        "solid",
        fgColor="1F4E78"
    )

    cell.alignment = Alignment(
        horizontal="center"
    )


for column in ws.columns:

    max_length = 0

    column_letter = column[0].column_letter

    for cell in column:

        if cell.value is not None:

            max_length = max(
                max_length,
                len(str(cell.value))
            )

    ws.column_dimensions[
        column_letter
    ].width = min(
        max_length + 2,
        30
    )


# =========================================================
# FORMAT RFM SEGMENTS
# =========================================================

ws2 = wb["RFM Segments"]

ws2.freeze_panes = "A2"
ws2.auto_filter.ref = ws2.dimensions

for cell in ws2[1]:

    cell.font = Font(
        bold=True,
        color="FFFFFF"
    )

    cell.fill = PatternFill(
        "solid",
        fgColor="1F4E78"
    )

    cell.alignment = Alignment(
        horizontal="center"
    )


for column in ws2.columns:

    max_length = 0

    column_letter = column[0].column_letter

    for cell in column:

        if cell.value is not None:

            max_length = max(
                max_length,
                len(str(cell.value))
            )

    ws2.column_dimensions[
        column_letter
    ].width = min(
        max_length + 2,
        30
    )


# =========================================================
# FORMAT SEGMENT COUNTS
# =========================================================

ws3 = wb["RFM Segment Counts"]

ws3.freeze_panes = "A2"
ws3.auto_filter.ref = ws3.dimensions

for cell in ws3[1]:

    cell.font = Font(
        bold=True,
        color="FFFFFF"
    )

    cell.fill = PatternFill(
        "solid",
        fgColor="1F4E78"
    )

    cell.alignment = Alignment(
        horizontal="center"
    )


for column in ws3.columns:

    max_length = 0

    column_letter = column[0].column_letter

    for cell in column:

        if cell.value is not None:

            max_length = max(
                max_length,
                len(str(cell.value))
            )

    ws3.column_dimensions[
        column_letter
    ].width = min(
        max_length + 2,
        30
    )


# =========================================================
# SAVE WORKBOOK
# =========================================================

wb.save(output_excel)


# =========================================================
# FINAL MESSAGE
# =========================================================

print("\n========================================")
print("RFM ANALYSIS COMPLETED SUCCESSFULLY")
print("========================================")

print("\nFinal Excel File:")
print(output_excel)

print("\nCSV Files:")
print("rfm_customer_analysis.csv")
print("rfm_segment_summary.csv")
print("rfm_segment_counts.csv")

print("\nTotal Customers Analyzed:")
print(len(rfm))

print("\nSegments:")
print(rfm["Segment"].value_counts())