import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os


# ============================================================
# STEP 1: DATABASE CONNECTION
# ============================================================

server = r"ZUBAIR\SQLEXPRESS"
database = "RetailECommerceDB"

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

engine = create_engine(
    "mssql+pyodbc:///?odbc_connect="
    + quote_plus(connection_string)
)

print("Database connection created successfully.")


# ============================================================
# STEP 2: LOAD ORDERS
# ============================================================

orders_query = """
SELECT
    OrderID,
    CustomerID,
    OrderDate,
    Status
FROM Sales.Orders
"""

orders = pd.read_sql(
    orders_query,
    engine
)

print(
    "Orders Loaded:",
    len(orders)
)


# ============================================================
# STEP 3: DATA VALIDATION
# ============================================================

print()
print("=" * 60)
print("DATA VALIDATION")
print("=" * 60)

print(
    "Missing Customer IDs:",
    orders["CustomerID"].isna().sum()
)

print(
    "Missing Order Dates:",
    orders["OrderDate"].isna().sum()
)

print(
    "Duplicate Order IDs:",
    orders["OrderID"].duplicated().sum()
)


# ============================================================
# STEP 4: REMOVE INVALID RECORDS
# ============================================================

orders = orders.dropna(
    subset=[
        "CustomerID",
        "OrderDate"
    ]
).copy()


orders["OrderDate"] = pd.to_datetime(
    orders["OrderDate"]
)


# ============================================================
# STEP 5: CREATE ORDER MONTH
# ============================================================

orders["OrderMonth"] = (
    orders["OrderDate"]
    .dt.to_period("M")
)


# ============================================================
# STEP 6: FIND FIRST PURCHASE MONTH
# ============================================================

customer_first_purchase = (
    orders
    .groupby("CustomerID")["OrderMonth"]
    .min()
    .reset_index()
)


customer_first_purchase.columns = [
    "CustomerID",
    "CohortMonth"
]


print()
print(
    "Customer cohorts created successfully."
)

print(
    "Total customers with orders:",
    len(customer_first_purchase)
)


# ============================================================
# STEP 7: MERGE COHORT INFORMATION
# ============================================================

cohort_data = orders.merge(
    customer_first_purchase,
    on="CustomerID",
    how="left"
)


# ============================================================
# STEP 8: CALCULATE MONTHS SINCE FIRST PURCHASE
# ============================================================

cohort_data["CohortIndex"] = (
    (
        cohort_data["OrderMonth"]
        - cohort_data["CohortMonth"]
    )
    .apply(lambda x: x.n)
    + 1
)


print()
print(
    "Cohort index calculated successfully."
)


# ============================================================
# STEP 9: REMOVE DUPLICATE CUSTOMER-MONTH RECORDS
# ============================================================

customer_months = (
    cohort_data[
        [
            "CustomerID",
            "CohortMonth",
            "OrderMonth",
            "CohortIndex"
        ]
    ]
    .drop_duplicates()
)


print(
    "Unique customer-month records:",
    len(customer_months)
)


# ============================================================
# STEP 10: CREATE COHORT RETENTION MATRIX
# ============================================================

cohort_counts = (
    customer_months
    .groupby(
        [
            "CohortMonth",
            "CohortIndex"
        ]
    )["CustomerID"]
    .nunique()
    .reset_index()
)


cohort_matrix = (
    cohort_counts
    .pivot(
        index="CohortMonth",
        columns="CohortIndex",
        values="CustomerID"
    )
)


# ============================================================
# STEP 11: CALCULATE RETENTION %
# ============================================================

retention_matrix = (
    cohort_matrix
    .divide(
        cohort_matrix.iloc[:, 0],
        axis=0
    )
    * 100
)


print()
print("=" * 60)
print("COHORT CUSTOMER RETENTION %")
print("=" * 60)

print(
    retention_matrix.round(2)
)


# ============================================================
# STEP 12: SAVE COHORT OUTPUTS
# ============================================================

cohort_matrix.to_csv(
    "cohort_customer_counts.csv"
)


retention_matrix.to_csv(
    "cohort_retention_matrix.csv"
)


customer_months.to_csv(
    "customer_cohort_data.csv",
    index=False
)


print()
print(
    "Cohort CSV files exported successfully."
)


# ============================================================
# STEP 13: BASIC COHORT SUMMARY
# ============================================================

cohort_summary = (
    customer_first_purchase
    .groupby("CohortMonth")["CustomerID"]
    .nunique()
    .reset_index()
)


cohort_summary.columns = [
    "CohortMonth",
    "Customers"
]


print()
print("=" * 60)
print("CUSTOMERS BY COHORT")
print("=" * 60)

print(
    cohort_summary.to_string(
        index=False
    )
)


# ============================================================
# STEP 14: CREATE EXCEL OUTPUT
# ============================================================

output_excel = (
    "Cohort_Analysis.xlsx"
)


with pd.ExcelWriter(
    output_excel,
    engine="openpyxl"
) as writer:

    customer_cohort_data = cohort_data[
        [
            "OrderID",
            "CustomerID",
            "OrderDate",
            "OrderMonth",
            "CohortMonth",
            "CohortIndex"
        ]
    ]

    customer_cohort_data.to_excel(
        writer,
        sheet_name="Customer Cohorts",
        index=False
    )

    cohort_summary.to_excel(
        writer,
        sheet_name="Cohort Summary",
        index=False
    )

    cohort_matrix.to_excel(
        writer,
        sheet_name="Cohort Customer Counts"
    )

    retention_matrix.to_excel(
        writer,
        sheet_name="Retention Matrix"
    )
    customer_cohort_data.to_excel(
        writer,
        sheet_name="Customer Cohorts",
        index=False
    )


    cohort_summary.to_excel(
        writer,
        sheet_name="Cohort Summary",
        index=False
    )


    cohort_matrix.to_excel(
        writer,
        sheet_name="Cohort Customer Counts"
    )


    retention_matrix.to_excel(
        writer,
        sheet_name="Retention Matrix"
    )


print()
print("=" * 60)
print("COHORT ANALYSIS COMPLETED")
print("=" * 60)

print(
    "Excel file:",
    output_excel
)

print(
    "Customer Cohorts sheet created."
)

print(
    "Cohort Summary sheet created."
)

print(
    "Cohort Customer Counts sheet created."
)

print(
    "Retention Matrix sheet created."
)

print("=" * 60)