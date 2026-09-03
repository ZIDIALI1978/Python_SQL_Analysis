import pyodbc
import pandas as pd
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
# 2. LOAD SUPPLIERS
# =======================================

suppliers_query = """
SELECT *
FROM Purchasing.Suppliers
"""

suppliers = pd.read_sql(
    suppliers_query,
    connection
)


print("\n======================================")
print("SUPPLIERS DATA")
print("======================================")

print(suppliers.head())


# =======================================
# 3. BASIC INFORMATION
# =======================================

print("\n======================================")
print("SUPPLIER SHAPE")
print("======================================")

print(suppliers.shape)


print("\n======================================")
print("SUPPLIER COLUMNS")
print("======================================")

print(suppliers.columns.tolist())


print("\n======================================")
print("SUPPLIER INFORMATION")
print("======================================")

suppliers.info()


# =======================================
# 4. MISSING VALUES
# =======================================

print("\n======================================")
print("MISSING VALUES")
print("======================================")

print(suppliers.isnull().sum())


# =======================================
# 5. TOTAL SUPPLIERS
# =======================================

total_suppliers = suppliers["SupplierID"].nunique()

print("\n======================================")
print("TOTAL SUPPLIERS")
print("======================================")

print(total_suppliers)


# =======================================
# 6. LOAD PRODUCTS
# =======================================

products_query = """
SELECT
    p.ProductID,
    p.SupplierID,
    p.ProductName,
    p.CostPrice,
    p.SellingPrice,
    p.IsActive,
    p.InStock,
    p.InOrder
FROM Inventory.Products AS p
"""

products = pd.read_sql(
    products_query,
    connection
)


print("\n======================================")
print("PRODUCTS LOADED")
print("======================================")

print(products.head())


# =======================================
# 7. CONVERT NUMERIC COLUMNS
# =======================================

products["CostPrice"] = pd.to_numeric(
    products["CostPrice"],
    errors="coerce"
)

products["SellingPrice"] = pd.to_numeric(
    products["SellingPrice"],
    errors="coerce"
)

products["InStock"] = pd.to_numeric(
    products["InStock"],
    errors="coerce"
)

products["InOrder"] = pd.to_numeric(
    products["InOrder"],
    errors="coerce"
)


# =======================================
# 8. PRODUCTS BY SUPPLIER
# =======================================

products_by_supplier = (
    products
    .groupby("SupplierID")
    .size()
    .sort_values(ascending=False)
)


print("\n======================================")
print("PRODUCTS BY SUPPLIER")
print("======================================")

print(products_by_supplier)


# =======================================
# 9. SUPPLIER NAMES WITH PRODUCT COUNT
# =======================================

supplier_product_count = (
    products
    .groupby("SupplierID")
    .size()
    .reset_index(name="ProductCount")
    .merge(
        suppliers[
            ["SupplierID", "SupplierName"]
        ],
        on="SupplierID",
        how="left"
    )
    .sort_values(
        "ProductCount",
        ascending=False
    )
)


print("\n======================================")
print("SUPPLIER PRODUCT COUNT")
print("======================================")

print(supplier_product_count)


# =======================================
# 10. TOP SUPPLIERS GRAPH
# =======================================

top_suppliers = supplier_product_count.head(10)


plt.figure(figsize=(10, 6))

plt.bar(
    top_suppliers["SupplierName"],
    top_suppliers["ProductCount"]
)

plt.xlabel("Supplier")
plt.ylabel("Number of Products")
plt.title("Top Suppliers by Number of Products")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# =======================================
# 11. AVERAGE SELLING PRICE BY SUPPLIER
# =======================================

avg_price_supplier = (
    products
    .groupby("SupplierID")["SellingPrice"]
    .mean()
    .reset_index(name="AverageSellingPrice")
    .merge(
        suppliers[
            ["SupplierID", "SupplierName"]
        ],
        on="SupplierID",
        how="left"
    )
    .sort_values(
        "AverageSellingPrice",
        ascending=False
    )
)


print("\n======================================")
print("AVERAGE SELLING PRICE BY SUPPLIER")
print("======================================")

print(avg_price_supplier)


# =======================================
# 12. TOP SUPPLIERS BY AVERAGE PRICE
# =======================================

top_price_suppliers = avg_price_supplier.head(10)


plt.figure(figsize=(10, 6))

plt.bar(
    top_price_suppliers["SupplierName"],
    top_price_suppliers["AverageSellingPrice"]
)

plt.xlabel("Supplier")
plt.ylabel("Average Selling Price")

plt.title(
    "Suppliers by Average Selling Price"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# =======================================
# 13. SUPPLIER INVENTORY
# =======================================

supplier_inventory = (
    products
    .groupby("SupplierID")["InStock"]
    .sum()
    .reset_index(name="TotalStock")
    .merge(
        suppliers[
            ["SupplierID", "SupplierName"]
        ],
        on="SupplierID",
        how="left"
    )
    .sort_values(
        "TotalStock",
        ascending=False
    )
)


print("\n======================================")
print("INVENTORY BY SUPPLIER")
print("======================================")

print(supplier_inventory)


# =======================================
# 14. INVENTORY GRAPH
# =======================================

top_inventory_suppliers = (
    supplier_inventory.head(10)
)


plt.figure(figsize=(10, 6))

plt.bar(
    top_inventory_suppliers["SupplierName"],
    top_inventory_suppliers["TotalStock"]
)

plt.xlabel("Supplier")
plt.ylabel("Stock Quantity")

plt.title(
    "Top Suppliers by Inventory Stock"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# =======================================
# 15. SUPPLIER PROFIT POTENTIAL
# =======================================

products["PotentialProfit"] = (
    products["SellingPrice"]
    - products["CostPrice"]
) * products["InStock"]


supplier_profit = (
    products
    .groupby("SupplierID")["PotentialProfit"]
    .sum()
    .reset_index()
    .merge(
        suppliers[
            ["SupplierID", "SupplierName"]
        ],
        on="SupplierID",
        how="left"
    )
    .sort_values(
        "PotentialProfit",
        ascending=False
    )
)


print("\n======================================")
print("SUPPLIER POTENTIAL PROFIT")
print("======================================")

print(supplier_profit)


# =======================================
# 16. POTENTIAL PROFIT GRAPH
# =======================================

top_profit_suppliers = (
    supplier_profit.head(10)
)


plt.figure(figsize=(10, 6))

plt.bar(
    top_profit_suppliers["SupplierName"],
    top_profit_suppliers["PotentialProfit"]
)

plt.xlabel("Supplier")
plt.ylabel("Potential Profit")

plt.title(
    "Top Suppliers by Potential Profit"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# =======================================
# 17. FINAL SUPPLIER INSIGHTS
# =======================================

best_supplier_products = (
    supplier_product_count.iloc[0]
)

best_supplier_price = (
    avg_price_supplier.iloc[0]
)

best_supplier_inventory = (
    supplier_inventory.iloc[0]
)

best_supplier_profit = (
    supplier_profit.iloc[0]
)


print("\n")
print("==============================================")
print("FINAL SUPPLIER INSIGHTS")
print("==============================================")


print("\nTotal Suppliers:")
print(total_suppliers)


print("\nSupplier with Most Products:")
print(
    best_supplier_products["SupplierName"]
)


print("\nNumber of Products:")
print(
    best_supplier_products["ProductCount"]
)


print("\nHighest Average Selling Price Supplier:")
print(
    best_supplier_price["SupplierName"]
)


print("\nHighest Average Selling Price:")
print(
    best_supplier_price["AverageSellingPrice"]
)


print("\nSupplier with Highest Inventory:")
print(
    best_supplier_inventory["SupplierName"]
)


print("\nHighest Inventory:")
print(
    best_supplier_inventory["TotalStock"]
)


print("\nSupplier with Highest Potential Profit:")
print(
    best_supplier_profit["SupplierName"]
)


print("\nHighest Potential Profit:")
print(
    best_supplier_profit["PotentialProfit"]
)


# =======================================
# 18. CLOSE CONNECTION
# =======================================

connection.close()

print("\nDatabase connection closed!")

print("\nSUPPLIER ANALYSIS COMPLETED SUCCESSFULLY!")