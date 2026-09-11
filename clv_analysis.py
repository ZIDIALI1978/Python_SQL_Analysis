import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from urllib.parse import quote_plus


# ============================================================
# 1. DATABASE CONNECTION
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
# 2. LOAD ORDER DATA
# ============================================================

orders_query = """
SELECT
    OrderID,
    CustomerID,
    OrderDate
FROM Sales.Orders
"""

orders = pd.read_sql(orders_query, engine)

print(f"Orders Loaded: {len(orders)}")


# ============================================================
# 3. LOAD ORDER ITEMS + PRODUCT COST
# ============================================================

order_items_query = """
SELECT
    oi.OrderID,
    oi.ProductID,
    oi.Quantity,
    oi.UnitPrice,
    p.CostPrice
FROM Sales.OrderItems oi
INNER JOIN Inventory.Products p
    ON oi.ProductID = p.ProductID
"""

order_items = pd.read_sql(order_items_query, engine)

print(f"Order Items Loaded: {len(order_items)}")


# ============================================================
# 4. DATA PREPARATION
# ============================================================

orders["OrderDate"] = pd.to_datetime(orders["OrderDate"])

order_items["Revenue"] = (
    order_items["Quantity"] * order_items["UnitPrice"]
)

order_items["Cost"] = (
    order_items["Quantity"] * order_items["CostPrice"]
)

order_items["Profit"] = (
    order_items["Revenue"] - order_items["Cost"]
)


# ============================================================
# 5. MERGE ORDERS WITH ORDER ITEMS
# ============================================================

sales = orders.merge(
    order_items,
    on="OrderID",
    how="inner"
)

print(f"Analytical sales rows: {len(sales)}")


# ============================================================
# 6. CUSTOMER-LEVEL METRICS
# ============================================================

customer_clv = (
    sales.groupby("CustomerID")
    .agg(
        TotalOrders=("OrderID", "nunique"),
        TotalRevenue=("Revenue", "sum"),
        TotalCost=("Cost", "sum"),
        TotalProfit=("Profit", "sum"),
        FirstPurchase=("OrderDate", "min"),
        LastPurchase=("OrderDate", "max")
    )
    .reset_index()
)


# ============================================================
# 7. CUSTOMER AOV
# ============================================================

customer_clv["AOV"] = (
    customer_clv["TotalRevenue"]
    / customer_clv["TotalOrders"]
)


# ============================================================
# 8. OBSERVATION PERIOD
# ============================================================

observation_start = sales["OrderDate"].min()
observation_end = sales["OrderDate"].max()

observation_days = (
    observation_end - observation_start
).days

observation_years = observation_days / 365.25

print("\nOBSERVATION PERIOD")
print("Start:", observation_start.date())
print("End:", observation_end.date())
print("Years:", round(observation_years, 2))


# ============================================================
# 9. PURCHASE FREQUENCY
# ============================================================

customer_clv["AnnualPurchaseFrequency"] = (
    customer_clv["TotalOrders"]
    / observation_years
)


# ============================================================
# 10. CUSTOMER GROSS MARGIN
# ============================================================

customer_clv["GrossMargin"] = np.where(
    customer_clv["TotalRevenue"] > 0,
    customer_clv["TotalProfit"]
    / customer_clv["TotalRevenue"],
    0
)


# ============================================================
# 11. BASELINE CLV ASSUMPTION
# ============================================================

EXPECTED_LIFESPAN_YEARS = 2

customer_clv["ExpectedLifespanYears"] = (
    EXPECTED_LIFESPAN_YEARS
)


# ============================================================
# 12. CLV CALCULATION
# ============================================================

customer_clv["BaselineCLV"] = (
    customer_clv["AOV"]
    * customer_clv["AnnualPurchaseFrequency"]
    * customer_clv["ExpectedLifespanYears"]
    * customer_clv["GrossMargin"]
)


# ============================================================
# 13. ROUND VALUES
# ============================================================

numeric_columns = [
    "TotalRevenue",
    "TotalCost",
    "TotalProfit",
    "AOV",
    "AnnualPurchaseFrequency",
    "GrossMargin",
    "BaselineCLV"
]

for column in numeric_columns:
    customer_clv[column] = customer_clv[column].round(2)


# ============================================================
# 14. CLV SUMMARY
# ============================================================

# ============================================================
# 14. CLV SUMMARY
# ============================================================

overall_revenue = customer_clv["TotalRevenue"].sum()
overall_profit = customer_clv["TotalProfit"].sum()

overall_margin = 0

if overall_revenue > 0:
    overall_margin = overall_profit / overall_revenue

clv_summary = pd.DataFrame(
    {
        "Metric": [
            "Total Customers",
            "Total Revenue",
            "Total Profit",
            "Average Customer Revenue",
            "Average Customer Profit",
            "Average AOV",
            "Average Annual Purchase Frequency",
            "Overall Gross Margin",
            "Expected Customer Lifespan (Years)",
            "Average Baseline CLV",
            "Total Estimated CLV",
        ],
        "Value": [
            customer_clv["CustomerID"].nunique(),
            overall_revenue,
            overall_profit,
            customer_clv["TotalRevenue"].mean(),
            customer_clv["TotalProfit"].mean(),
            customer_clv["AOV"].mean(),
            customer_clv["AnnualPurchaseFrequency"].mean(),
            overall_margin,
            EXPECTED_LIFESPAN_YEARS,
            customer_clv["BaselineCLV"].mean(),
            customer_clv["BaselineCLV"].sum(),
        ],
    }
)

# ============================================================
# 15. DISPLAY RESULTS
# ============================================================

print("\nCUSTOMER CLV ANALYSIS")
print(customer_clv.head(10).to_string(index=False))

print("\nCLV SUMMARY")
print(clv_summary.to_string(index=False))


# ============================================================
# 16. TOP 10 CUSTOMERS BY CLV
# ============================================================

top_clv = (
    customer_clv
    .sort_values("BaselineCLV", ascending=False)
    .head(10)
)

print("\nTOP 10 CUSTOMERS BY BASELINE CLV")
print(top_clv[
    [
        "CustomerID",
        "TotalOrders",
        "TotalRevenue",
        "TotalProfit",
        "AOV",
        "BaselineCLV"
    ]
].to_string(index=False))


# ============================================================
# 17. EXPORT TO EXCEL
# ============================================================

output_file = "CLV_Analysis.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

    customer_clv.to_excel(
        writer,
        sheet_name="Customer CLV",
        index=False
    )

    clv_summary.to_excel(
        writer,
        sheet_name="CLV Summary",
        index=False
    )

    top_clv.to_excel(
        writer,
        sheet_name="Top CLV Customers",
        index=False
    )

print("\nCLV ANALYSIS COMPLETED")
print(f"Excel file: {output_file}")
print("Customer CLV sheet created.")
print("CLV Summary sheet created.")
print("Top CLV Customers sheet created.")