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
# 2. LOAD PRODUCTS
# ============================================================

products_query = """
SELECT
    ProductID,
    ProductName,
    CategoryID,
    CostPrice,
    SellingPrice
FROM Inventory.Products
"""

products = pd.read_sql(products_query, engine)

print(f"Products Loaded: {len(products)}")


# ============================================================
# 3. LOAD CATEGORIES
# ============================================================

categories_query = """
SELECT
    CategoryID,
    CategoryName
FROM Inventory.Categories
"""

categories = pd.read_sql(categories_query, engine)

print(f"Categories Loaded: {len(categories)}")


# ============================================================
# 4. LOAD ORDER ITEMS
# ============================================================

order_items_query = """
SELECT
    OrderID,
    ProductID,
    Quantity,
    UnitPrice
FROM Sales.OrderItems
"""

order_items = pd.read_sql(order_items_query, engine)

print(f"Order Items Loaded: {len(order_items)}")


# ============================================================
# 5. LOAD INVENTORY
# ============================================================

inventory_query = """
SELECT *
FROM Inventory.Inventory
"""

inventory = pd.read_sql(inventory_query, engine)

print(f"Inventory Rows Loaded: {len(inventory)}")

print("\nInventory Columns:")
print(inventory.columns.tolist())


# ============================================================
# 6. PRODUCT SALES CALCULATION
# ============================================================

order_items["Revenue"] = (
    order_items["Quantity"] *
    order_items["UnitPrice"]
)

product_sales = (
    order_items
    .groupby("ProductID")
    .agg(
        QuantitySold=("Quantity", "sum"),
        TotalRevenue=("Revenue", "sum"),
        TotalOrders=("OrderID", "nunique")
    )
    .reset_index()
)


# ============================================================
# 7. MERGE PRODUCTS + CATEGORIES + SALES
# ============================================================

product_analysis = products.merge(
    categories,
    on="CategoryID",
    how="left"
)

product_analysis = product_analysis.merge(
    product_sales,
    on="ProductID",
    how="left"
)


# Products with no sales
product_analysis["QuantitySold"] = (
    product_analysis["QuantitySold"]
    .fillna(0)
)

product_analysis["TotalRevenue"] = (
    product_analysis["TotalRevenue"]
    .fillna(0)
)

product_analysis["TotalOrders"] = (
    product_analysis["TotalOrders"]
    .fillna(0)
)


# ============================================================
# 8. PRODUCT COST & PROFIT
# ============================================================

product_analysis["TotalCost"] = (
    product_analysis["QuantitySold"] *
    product_analysis["CostPrice"]
)

product_analysis["TotalProfit"] = (
    product_analysis["TotalRevenue"] -
    product_analysis["TotalCost"]
)

product_analysis["ProfitMargin"] = np.where(
    product_analysis["TotalRevenue"] > 0,
    (
        product_analysis["TotalProfit"] /
        product_analysis["TotalRevenue"]
    ) * 100,
    0
)


# ============================================================
# 9. INVENTORY COLUMN DETECTION
# ============================================================

inventory_lower = {
    column.lower(): column
    for column in inventory.columns
}

product_id_column = None
stock_column = None

for column in inventory.columns:

    lower_column = column.lower()

    if lower_column == "productid":
        product_id_column = column

    if lower_column in [
        "quantity",
        "stock",
        "stockquantity",
        "quantityinstock",
        "currentstock"
    ]:
        stock_column = column


if product_id_column is None:
    raise ValueError(
        "ProductID column not found in Inventory table."
    )

if stock_column is None:
    raise ValueError(
        "Stock quantity column not found in Inventory table."
    )


print("\nInventory Product ID Column:", product_id_column)
print("Inventory Stock Column:", stock_column)


# ============================================================
# 10. MERGE INVENTORY
# ============================================================

inventory_clean = inventory[
    [product_id_column, stock_column]
].copy()

inventory_clean.columns = [
    "ProductID",
    "CurrentStock"
]

product_analysis = product_analysis.merge(
    inventory_clean,
    on="ProductID",
    how="left"
)

product_analysis["CurrentStock"] = (
    product_analysis["CurrentStock"]
    .fillna(0)
)


# ============================================================
# 11. INVENTORY VALUE
# ============================================================

product_analysis["InventoryValue"] = (
    product_analysis["CurrentStock"] *
    product_analysis["CostPrice"]
)


# ============================================================
# 12. SALES VELOCITY
# ============================================================

orders_query = """
SELECT
    OrderDate
FROM Sales.Orders
"""

orders = pd.read_sql(orders_query, engine)

orders["OrderDate"] = pd.to_datetime(
    orders["OrderDate"]
)

start_date = orders["OrderDate"].min()
end_date = orders["OrderDate"].max()

observation_days = (
    end_date - start_date
).days

if observation_days <= 0:
    observation_days = 1

observation_months = observation_days / 30.44

product_analysis["MonthlySalesVelocity"] = np.where(
    observation_months > 0,
    product_analysis["QuantitySold"] /
    observation_months,
    0
)


# ============================================================
# 13. STOCK COVER
# ============================================================

product_analysis["MonthlySalesVelocity"] = (
    product_analysis["MonthlySalesVelocity"]
    .round(2)
)

product_analysis["StockCoverMonths"] = np.where(
    product_analysis["MonthlySalesVelocity"] > 0,
    product_analysis["CurrentStock"] /
    product_analysis["MonthlySalesVelocity"],
    np.nan
)


# ============================================================
# 14. INVENTORY RISK CLASSIFICATION
# ============================================================

def classify_inventory(row):

    stock = row["CurrentStock"]
    velocity = row["MonthlySalesVelocity"]

    if stock == 0:
        return "Out of Stock"

    if velocity == 0:
        return "Dead Stock"

    stock_cover = row["StockCoverMonths"]

    if stock_cover < 1:
        return "Low Stock"

    if stock_cover > 6:
        return "Overstock"

    return "Healthy"


product_analysis["InventoryRisk"] = (
    product_analysis.apply(
        classify_inventory,
        axis=1
    )
)


# ============================================================
# 15. ABC ANALYSIS
# ============================================================

product_analysis = product_analysis.sort_values(
    "TotalRevenue",
    ascending=False
).reset_index(drop=True)

total_revenue = product_analysis["TotalRevenue"].sum()

if total_revenue > 0:

    product_analysis["RevenueContribution"] = (
        product_analysis["TotalRevenue"] /
        total_revenue
    ) * 100

    product_analysis["CumulativeRevenue"] = (
        product_analysis["RevenueContribution"]
        .cumsum()
    )

else:

    product_analysis["RevenueContribution"] = 0
    product_analysis["CumulativeRevenue"] = 0


def abc_class(cumulative):

    if cumulative <= 80:
        return "A"

    elif cumulative <= 95:
        return "B"

    else:
        return "C"


product_analysis["ABCClass"] = (
    product_analysis["CumulativeRevenue"]
    .apply(abc_class)
)


# ============================================================
# 16. PRODUCT PERFORMANCE SCORE
# ============================================================

revenue_rank = (
    product_analysis["TotalRevenue"]
    .rank(pct=True)
)

profit_rank = (
    product_analysis["TotalProfit"]
    .rank(pct=True)
)

quantity_rank = (
    product_analysis["QuantitySold"]
    .rank(pct=True)
)

product_analysis["PerformanceScore"] = (
    (
        revenue_rank +
        profit_rank +
        quantity_rank
    ) / 3
) * 100

product_analysis["PerformanceScore"] = (
    product_analysis["PerformanceScore"]
    .round(2)
)


# ============================================================
# 17. PERFORMANCE CATEGORY
# ============================================================

def performance_category(score):

    if score >= 80:
        return "Excellent"

    elif score >= 60:
        return "Good"

    elif score >= 40:
        return "Average"

    else:
        return "Low"


product_analysis["PerformanceCategory"] = (
    product_analysis["PerformanceScore"]
    .apply(performance_category)
)


# ============================================================
# 18. ROUND NUMERIC VALUES
# ============================================================

round_columns = [
    "CostPrice",
    "SellingPrice",
    "TotalRevenue",
    "TotalCost",
    "TotalProfit",
    "ProfitMargin",
    "InventoryValue",
    "StockCoverMonths",
    "RevenueContribution",
    "CumulativeRevenue"
]

for column in round_columns:

    if column in product_analysis.columns:

        product_analysis[column] = (
            product_analysis[column]
            .round(2)
        )


# ============================================================
# 19. PRODUCT SCORECARD
# ============================================================

product_scorecard = product_analysis[
    [
        "ProductID",
        "ProductName",
        "CategoryName",
        "QuantitySold",
        "TotalOrders",
        "TotalRevenue",
        "TotalCost",
        "TotalProfit",
        "ProfitMargin",
        "CurrentStock",
        "InventoryValue",
        "MonthlySalesVelocity",
        "StockCoverMonths",
        "InventoryRisk",
        "ABCClass",
        "PerformanceScore",
        "PerformanceCategory"
    ]
].copy()


# ============================================================
# 20. ABC SUMMARY
# ============================================================

abc_summary = (
    product_analysis
    .groupby("ABCClass")
    .agg(
        Products=("ProductID", "count"),
        Revenue=("TotalRevenue", "sum"),
        Profit=("TotalProfit", "sum"),
        QuantitySold=("QuantitySold", "sum")
    )
    .reset_index()
)

abc_summary["RevenuePercentage"] = (
    abc_summary["Revenue"] /
    total_revenue
) * 100

abc_summary = abc_summary.round(2)


# ============================================================
# 21. INVENTORY RISK SUMMARY
# ============================================================

inventory_risk_summary = (
    product_analysis
    .groupby("InventoryRisk")
    .agg(
        Products=("ProductID", "count"),
        InventoryValue=("InventoryValue", "sum"),
        QuantityInStock=("CurrentStock", "sum")
    )
    .reset_index()
)

inventory_risk_summary = (
    inventory_risk_summary
    .sort_values(
        "InventoryValue",
        ascending=False
    )
)


# ============================================================
# 22. TOP PRODUCTS
# ============================================================

top_revenue_products = (
    product_analysis
    .sort_values(
        "TotalRevenue",
        ascending=False
    )
    .head(10)
)

top_profit_products = (
    product_analysis
    .sort_values(
        "TotalProfit",
        ascending=False
    )
    .head(10)
)

top_velocity_products = (
    product_analysis
    .sort_values(
        "MonthlySalesVelocity",
        ascending=False
    )
    .head(10)
)


# ============================================================
# 23. LOW STOCK PRODUCTS
# ============================================================

low_stock_products = product_analysis[
    product_analysis["InventoryRisk"] == "Low Stock"
].copy()


# ============================================================
# 24. DEAD STOCK PRODUCTS
# ============================================================

dead_stock_products = product_analysis[
    product_analysis["InventoryRisk"] == "Dead Stock"
].copy()


# ============================================================
# 25. OVERSTOCK PRODUCTS
# ============================================================

overstock_products = product_analysis[
    product_analysis["InventoryRisk"] == "Overstock"
].copy()


# ============================================================
# 26. DISPLAY RESULTS
# ============================================================

print("\nPRODUCT PERFORMANCE SUMMARY")

print(
    product_scorecard[
        [
            "ProductID",
            "ProductName",
            "CategoryName",
            "QuantitySold",
            "TotalRevenue",
            "TotalProfit",
            "ProfitMargin",
            "CurrentStock",
            "InventoryRisk",
            "ABCClass",
            "PerformanceScore"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


print("\nABC SUMMARY")
print(
    abc_summary.to_string(index=False)
)


print("\nINVENTORY RISK SUMMARY")
print(
    inventory_risk_summary.to_string(index=False)
)


print("\nTOP 10 REVENUE PRODUCTS")

print(
    top_revenue_products[
        [
            "ProductID",
            "ProductName",
            "TotalRevenue",
            "TotalProfit",
            "ProfitMargin"
        ]
    ]
    .to_string(index=False)
)


print("\nTOP 10 PROFIT PRODUCTS")

print(
    top_profit_products[
        [
            "ProductID",
            "ProductName",
            "TotalRevenue",
            "TotalProfit",
            "ProfitMargin"
        ]
    ]
    .to_string(index=False)
)


print("\nLOW STOCK PRODUCTS")
print(
    low_stock_products[
        [
            "ProductID",
            "ProductName",
            "CurrentStock",
            "MonthlySalesVelocity",
            "StockCoverMonths"
        ]
    ]
    .head(20)
    .to_string(index=False)
)


print("\nDEAD STOCK PRODUCTS")
print(
    dead_stock_products[
        [
            "ProductID",
            "ProductName",
            "CurrentStock",
            "InventoryValue"
        ]
    ]
    .head(20)
    .to_string(index=False)
)


# ============================================================
# 27. EXPORT TO EXCEL
# ============================================================

output_file = "Product_Inventory_Analysis.xlsx"

with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    product_scorecard.to_excel(
        writer,
        sheet_name="Product Scorecard",
        index=False
    )

    abc_summary.to_excel(
        writer,
        sheet_name="ABC Analysis",
        index=False
    )

    inventory_risk_summary.to_excel(
        writer,
        sheet_name="Inventory Risk",
        index=False
    )

    top_revenue_products.to_excel(
        writer,
        sheet_name="Top Revenue Products",
        index=False
    )

    top_profit_products.to_excel(
        writer,
        sheet_name="Top Profit Products",
        index=False
    )

    top_velocity_products.to_excel(
        writer,
        sheet_name="Top Sales Velocity",
        index=False
    )

    low_stock_products.to_excel(
        writer,
        sheet_name="Low Stock",
        index=False
    )

    dead_stock_products.to_excel(
        writer,
        sheet_name="Dead Stock",
        index=False
    )

    overstock_products.to_excel(
        writer,
        sheet_name="Overstock",
        index=False
    )


print("\nPRODUCT & INVENTORY ANALYSIS COMPLETED")
print(f"Excel file: {output_file}")
print("Product Scorecard sheet created.")
print("ABC Analysis sheet created.")
print("Inventory Risk sheet created.")
print("Top Revenue Products sheet created.")
print("Top Profit Products sheet created.")
print("Top Sales Velocity sheet created.")
print("Low Stock sheet created.")
print("Dead Stock sheet created.")
print("Overstock sheet created.")