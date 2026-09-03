import pyodbc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# =======================================
# 1. DATABASE CONNECTION
# =======================================

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=ZUBAIR\\SQLEXPRESS;"
    "DATABASE=RetailECommerceDB;"
    "Trusted_Connection=yes;"
)

print("Database connected successfully!")


# =======================================
# 2. LOAD INVENTORY
# =======================================

inventory_query = """
SELECT
    ProductID,
    QuantityInStock,
    ReorderLevel
FROM Inventory.Inventory
"""

inventory = pd.read_sql(
    inventory_query,
    connection
)


# =======================================
# 3. LOAD PRODUCTS
# =======================================

products_query = """
SELECT
    p.ProductID,
    p.ProductName,
    p.CategoryID,
    p.SellingPrice,
    c.CategoryName,
    p.SupplierID
FROM Inventory.Products AS p
INNER JOIN Inventory.Categories AS c
    ON p.CategoryID = c.CategoryID
"""

products = pd.read_sql(
    products_query,
    connection
)


# =======================================
# 4. DISPLAY INVENTORY DATA
# =======================================

print("\n======================================")
print("INVENTORY DATA")
print("======================================")

print(inventory.head())


# =======================================
# 5. INVENTORY SHAPE
# =======================================

print("\n======================================")
print("INVENTORY SHAPE")
print("======================================")

print(inventory.shape)


# =======================================
# 6. INVENTORY COLUMNS
# =======================================

print("\n======================================")
print("INVENTORY COLUMNS")
print("======================================")

print(inventory.columns.tolist())


# =======================================
# 7. INVENTORY INFORMATION
# =======================================

print("\n======================================")
print("INVENTORY INFORMATION")
print("======================================")

inventory.info()


# =======================================
# 8. MISSING VALUES
# =======================================

print("\n======================================")
print("MISSING VALUES")
print("======================================")

print(inventory.isnull().sum())



# =======================================
# 8. TOTAL STOCK
# =======================================

print("\n======================================")
print("TOTAL STOCK")
print("======================================")

total_stock = inventory["QuantityInStock"].sum()

print("Total Quantity In Stock:")
print(total_stock)


# =======================================
# 9. AVERAGE STOCK
# =======================================

print("\n======================================")
print("AVERAGE STOCK")
print("======================================")

average_stock = inventory["QuantityInStock"].mean()

print("Average Stock per Product:")
print(round(average_stock, 2))


# =======================================
# 10. LOW STOCK PRODUCTS
# =======================================

print("\n======================================")
print("LOW STOCK PRODUCTS")
print("======================================")

low_stock = inventory[
    inventory["QuantityInStock"] <= inventory["ReorderLevel"]
]

print(low_stock)

print("\nNumber of Low Stock Products:")
print(len(low_stock))


# =======================================
# 11. OUT OF STOCK PRODUCTS
# =======================================

print("\n======================================")
print("OUT OF STOCK PRODUCTS")
print("======================================")

out_of_stock = inventory[
    inventory["QuantityInStock"] == 0
]

print(out_of_stock)

print("\nNumber of Out of Stock Products:")
print(len(out_of_stock))


# =======================================
# 12. HIGHEST STOCK
# =======================================

print("\n======================================")
print("HIGHEST STOCK")
print("======================================")

highest_stock = inventory.loc[
    inventory["QuantityInStock"].idxmax()
]

print(highest_stock)


# =======================================
# 13. LOWEST STOCK
# =======================================

print("\n======================================")
print("LOWEST STOCK")
print("======================================")

lowest_stock = inventory.loc[
    inventory["QuantityInStock"].idxmin()
]

print(lowest_stock)


# =======================================
# 14. REORDER REQUIRED
# =======================================

print("\n======================================")
print("REORDER REQUIRED")
print("======================================")

reorder_required = inventory[
    inventory["QuantityInStock"] <= inventory["ReorderLevel"]
]

print(reorder_required)

print("\nProducts Requiring Reorder:")
print(len(reorder_required))


# =======================================
# 15. STOCK STATUS
# =======================================

inventory["StockStatus"] = np.where(
    inventory["QuantityInStock"] == 0,
    "Out of Stock",
    np.where(
        inventory["QuantityInStock"] <= inventory["ReorderLevel"],
        "Low Stock",
        "In Stock"
    )
)

print("\n======================================")
print("STOCK STATUS")
print("======================================")

print(
    inventory["StockStatus"].value_counts()
)


# =======================================
# 16. FINAL INVENTORY INSIGHTS
# =======================================

print("\n==============================================")
print("FINAL INVENTORY INSIGHTS")
print("==============================================")

print("\nTotal Inventory Stock:")
print(total_stock)

print("\nAverage Stock:")
print(round(average_stock, 2))

print("\nLow Stock Products:")
print(len(low_stock))

print("\nOut of Stock Products:")
print(len(out_of_stock))

print("\nProducts Requiring Reorder:")
print(len(reorder_required))

print("\nHighest Stock:")
print(highest_stock)

print("\nLowest Stock:")
print(lowest_stock)

print("\n==============================================")
print("INVENTORY ANALYSIS COMPLETED SUCCESSFULLY")
print("==============================================")


# =======================================
# 9. CONVERT NUMERIC COLUMNS
# =======================================

inventory["ProductID"] = pd.to_numeric(
    inventory["ProductID"],
    errors="coerce"
)

inventory["QuantityInStock"] = pd.to_numeric(
    inventory["QuantityInStock"],
    errors="coerce"
)

inventory["ReorderLevel"] = pd.to_numeric(
    inventory["ReorderLevel"],
    errors="coerce"
)

products["ProductID"] = pd.to_numeric(
    products["ProductID"],
    errors="coerce"
)

products["SellingPrice"] = pd.to_numeric(
    products["SellingPrice"],
    errors="coerce"
)


print("\nNumeric columns converted successfully!")


# =======================================
# 10. TOTAL INVENTORY RECORDS
# =======================================

print("\n======================================")
print("TOTAL INVENTORY RECORDS")
print("======================================")

total_inventory_records = len(inventory)

print(total_inventory_records)


# =======================================
# 11. INVENTORY STATISTICS
# =======================================

print("\n======================================")
print("INVENTORY STATISTICS")
print("======================================")

print(inventory.describe())


# =======================================
# 12. TOTAL STOCK
# =======================================

total_stock = inventory["QuantityInStock"].sum()

print("\n======================================")
print("TOTAL STOCK")
print("======================================")

print(total_stock)


# =======================================
# 13. AVERAGE STOCK
# =======================================

average_stock = inventory["QuantityInStock"].mean()

print("\n======================================")
print("AVERAGE STOCK PER PRODUCT")
print("======================================")

print(round(average_stock, 2))


# =======================================
# 14. HIGHEST STOCK PRODUCT
# =======================================

highest_stock_product = inventory.loc[
    inventory["QuantityInStock"].idxmax()
]

print("\n======================================")
print("HIGHEST STOCK PRODUCT")
print("======================================")

print(highest_stock_product)


# =======================================
# 15. LOWEST STOCK PRODUCT
# =======================================

lowest_stock_product = inventory.loc[
    inventory["QuantityInStock"].idxmin()
]

print("\n======================================")
print("LOWEST STOCK PRODUCT")
print("======================================")

print(lowest_stock_product)


# =======================================
# 16. MERGE INVENTORY WITH PRODUCTS
# =======================================

inventory_products = inventory.merge(
    products,
    on="ProductID",
    how="left"
)


print("\n======================================")
print("INVENTORY WITH PRODUCT DETAILS")
print("======================================")

print(
    inventory_products[
        [
            "ProductID",
            "ProductName",
            "CategoryName",
            "SellingPrice",
            "QuantityInStock",
            "ReorderLevel"
        ]
    ].head(10)
)


# =======================================
# 17. STOCK STATUS
# =======================================

inventory_products["StockStatus"] = np.where(
    inventory_products["QuantityInStock"]
    <= inventory_products["ReorderLevel"],
    "Reorder Required",
    "Sufficient Stock"
)


print("\n======================================")
print("STOCK STATUS")
print("======================================")

print(
    inventory_products["StockStatus"].value_counts()
)


# =======================================
# 18. PRODUCTS REQUIRING REORDER
# =======================================

reorder_products = inventory_products[
    inventory_products["QuantityInStock"]
    <= inventory_products["ReorderLevel"]
]


print("\n======================================")
print("PRODUCTS REQUIRING REORDER")
print("======================================")

print(
    reorder_products[
        [
            "ProductID",
            "ProductName",
            "CategoryName",
            "QuantityInStock",
            "ReorderLevel"
        ]
    ]
)


# =======================================
# 19. TOTAL PRODUCTS REQUIRING REORDER
# =======================================

total_reorder_products = len(
    reorder_products
)

print("\n======================================")
print("TOTAL PRODUCTS REQUIRING REORDER")
print("======================================")

print(total_reorder_products)


# =======================================
# 20. TOP 10 PRODUCTS BY STOCK
# =======================================

top_stock_products = (
    inventory_products
    .sort_values(
        "QuantityInStock",
        ascending=False
    )
    .head(10)
)


print("\n======================================")
print("TOP 10 PRODUCTS BY STOCK")
print("======================================")

print(
    top_stock_products[
        [
            "ProductID",
            "ProductName",
            "CategoryName",
            "QuantityInStock"
        ]
    ]
)


# =======================================
# 21. LOWEST 10 PRODUCTS BY STOCK
# =======================================

lowest_stock_products = (
    inventory_products
    .sort_values(
        "QuantityInStock",
        ascending=True
    )
    .head(10)
)


print("\n======================================")
print("LOWEST 10 PRODUCTS BY STOCK")
print("======================================")

print(
    lowest_stock_products[
        [
            "ProductID",
            "ProductName",
            "CategoryName",
            "QuantityInStock"
        ]
    ]
)


# =======================================
# 22. INVENTORY VALUE
# =======================================

inventory_products["InventoryValue"] = (
    inventory_products["QuantityInStock"]
    * inventory_products["SellingPrice"]
)


total_inventory_value = (
    inventory_products["InventoryValue"].sum()
)


print("\n======================================")
print("TOTAL INVENTORY VALUE")
print("======================================")

print(round(total_inventory_value, 2))


# =======================================
# 23. TOP 10 PRODUCTS BY INVENTORY VALUE
# =======================================

top_inventory_value = (
    inventory_products
    .sort_values(
        "InventoryValue",
        ascending=False
    )
    .head(10)
)


print("\n======================================")
print("TOP 10 PRODUCTS BY INVENTORY VALUE")
print("======================================")

print(
    top_inventory_value[
        [
            "ProductID",
            "ProductName",
            "CategoryName",
            "QuantityInStock",
            "SellingPrice",
            "InventoryValue"
        ]
    ]
)


# =======================================
# 24. INVENTORY BY CATEGORY
# =======================================

category_inventory = (
    inventory_products
    .groupby("CategoryName")["QuantityInStock"]
    .sum()
    .sort_values(
        ascending=False
    )
)


print("\n======================================")
print("INVENTORY BY CATEGORY")
print("======================================")

print(category_inventory)


# =======================================
# 25. INVENTORY VALUE BY CATEGORY
# =======================================

category_inventory_value = (
    inventory_products
    .groupby("CategoryName")["InventoryValue"]
    .sum()
    .sort_values(
        ascending=False
    )
)


print("\n======================================")
print("INVENTORY VALUE BY CATEGORY")
print("======================================")

print(category_inventory_value)


# =======================================
# 26. REORDER PRODUCTS BY CATEGORY
# =======================================

reorder_by_category = (
    reorder_products
    .groupby("CategoryName")
    .size()
    .sort_values(
        ascending=False
    )
)


print("\n======================================")
print("REORDER PRODUCTS BY CATEGORY")
print("======================================")

print(reorder_by_category)


# =======================================
# 27. STOCK STATUS GRAPH
# =======================================

stock_status_count = (
    inventory_products["StockStatus"]
    .value_counts()
)


plt.figure(figsize=(8, 5))

plt.bar(
    stock_status_count.index,
    stock_status_count.values
)

plt.xlabel("Stock Status")
plt.ylabel("Number of Products")
plt.title("Stock Status")

plt.xticks(rotation=20)
plt.tight_layout()
plt.show()


# =======================================
# 28. TOP 10 STOCK PRODUCTS GRAPH
# =======================================

plt.figure(figsize=(12, 6))

plt.bar(
    top_stock_products["ProductName"],
    top_stock_products["QuantityInStock"]
)

plt.xlabel("Product")
plt.ylabel("Quantity in Stock")
plt.title("Top 10 Products by Stock")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# =======================================
# 29. INVENTORY BY CATEGORY GRAPH
# =======================================

plt.figure(figsize=(10, 6))

plt.bar(
    category_inventory.index,
    category_inventory.values
)

plt.xlabel("Category")
plt.ylabel("Total Stock")
plt.title("Inventory by Category")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# =======================================
# 30. INVENTORY VALUE BY CATEGORY GRAPH
# =======================================

plt.figure(figsize=(10, 6))

plt.bar(
    category_inventory_value.index,
    category_inventory_value.values
)

plt.xlabel("Category")
plt.ylabel("Inventory Value")
plt.title("Inventory Value by Category")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# =======================================
# 31. REORDER PRODUCTS GRAPH
# =======================================

if len(reorder_by_category) > 0:

    plt.figure(figsize=(10, 6))

    plt.bar(
        reorder_by_category.index,
        reorder_by_category.values
    )

    plt.xlabel("Category")
    plt.ylabel("Products Requiring Reorder")
    plt.title("Reorder Required by Category")

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# =======================================
# 32. FINAL INVENTORY INSIGHTS
# =======================================

print("\n")
print("====================================================")
print("              FINAL INVENTORY INSIGHTS")
print("====================================================")


print("\nTotal Inventory Records:")
print(total_inventory_records)


print("\nTotal Products:")
print(len(inventory_products))


print("\nTotal Stock:")
print(total_stock)


print("\nAverage Stock per Product:")
print(round(average_stock, 2))


print("\nProducts Requiring Reorder:")
print(total_reorder_products)


print("\nTotal Inventory Value:")
print(round(total_inventory_value, 2))


print("\nHighest Stock Product:")
print(highest_stock_product["ProductID"])


highest_product_name = inventory_products.loc[
    inventory_products["QuantityInStock"].idxmax(),
    "ProductName"
]

print("Product Name:")
print(highest_product_name)


print("\nHighest Stock Quantity:")
print(highest_stock_product["QuantityInStock"])


print("\nLowest Stock Product:")

lowest_product_name = inventory_products.loc[
    inventory_products["QuantityInStock"].idxmin(),
    "ProductName"
]

print(lowest_product_name)


print("\nLowest Stock Quantity:")
print(lowest_stock_product["QuantityInStock"])


print("\nBest Category by Total Stock:")
print(category_inventory.idxmax())


print("\nBest Category Stock:")
print(category_inventory.max())


print("\nHighest Inventory Value Category:")
print(category_inventory_value.idxmax())


print("\nHighest Inventory Value:")
print(round(category_inventory_value.max(), 2))


if len(reorder_by_category) > 0:

    print("\nCategory Requiring Most Reorders:")
    print(reorder_by_category.idxmax())

    print("\nNumber of Reorders:")
    print(reorder_by_category.max())


print("\n====================================================")
print("       INVENTORY ANALYSIS COMPLETED SUCCESSFULLY")
print("====================================================")


# =======================================
# 33. CLOSE DATABASE CONNECTION
# =======================================

connection.close()

print("\nDatabase connection closed!")