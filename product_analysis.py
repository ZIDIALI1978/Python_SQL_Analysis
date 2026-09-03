import pyodbc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =======================================
# 1. Connect to SQL Server
# =======================================

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=ZUBAIR\\SQLEXPRESS;"
    "DATABASE=RetailECommerceDB;"
    "Trusted_Connection=yes;"
)

print("Database connected successfully!")


# =======================================
# 2. Load Products
# =======================================

query = """
SELECT *
FROM Inventory.Products
"""

products = pd.read_sql(query, connection)

# Convert numeric columns
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

print("\nData Types:")
print(
    products[
        ["CostPrice", "SellingPrice", "InStock", "InOrder"]
    ].dtypes
)

print("\nFirst 5 Products:")
print(products.head())

print("\nShape:")
print(products.shape)

print("\nColumns:")
print(products.columns)


# =======================================
# 3. Basic Information
# =======================================

print("\nProduct Information:")
products.info()


# =======================================
# 4. Check Missing Values
# =======================================

print("\nMissing Values:")
print(products.isnull().sum())


# =======================================
# 5. Price Statistics
# =======================================

print("\nCost Price Statistics:")
print(products["CostPrice"].describe())

print("\nSelling Price Statistics:")
print(products["SellingPrice"].describe())


# =======================================
# 6. Calculate Profit
# =======================================

products["Profit"] = (
    products["SellingPrice"] -
    products["CostPrice"]
)

print("\nProduct Profit:")
print(
    products[
        ["ProductName", "CostPrice",
         "SellingPrice", "Profit"]
    ].head()
)


# =======================================
# 7. Average Profit
# =======================================

print("\nAverage Profit:")
print(products["Profit"].mean())


# =======================================
# 8. Cheapest Product
# =======================================

cheapest = products.loc[
    products["SellingPrice"].idxmin()
]

print("\nCheapest Product:")
print(cheapest)


# =======================================
# 9. Most Expensive Product
# =======================================

expensive = products.loc[
    products["SellingPrice"].idxmax()
]

print("\nMost Expensive Product:")
print(expensive)


# =======================================
# 10. Potential Profit
# =======================================

products["PotentialProfit"] = (
    products["Profit"] *
    products["InStock"]
)

print("\nTotal Potential Profit:")
print(products["PotentialProfit"].sum())


# =======================================
# 11. Top 10 Expensive Products
# =======================================

top_products = products.nlargest(
    10,
    "SellingPrice"
)

print("\nTop 10 Most Expensive Products:")
print(
    top_products[
        ["ProductName", "SellingPrice"]
    ]
)


# =======================================
# 12. Graph - Top 10 Expensive Products
# =======================================

plt.figure(figsize=(9, 6))

plt.bar(
    top_products["ProductName"],
    top_products["SellingPrice"],
    color="red"
)

plt.xlabel("Product")
plt.ylabel("Selling Price")
plt.title("Top 10 Most Expensive Products")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# =======================================
# 13. Cost Price vs Selling Price
# =======================================

plt.figure(figsize=(8, 6))

plt.scatter(
    products["CostPrice"],
    products["SellingPrice"]
)

plt.xlabel("Cost Price")
plt.ylabel("Selling Price")
plt.title("Cost Price vs Selling Price")

plt.tight_layout()
plt.show()


# =======================================
# 14. Top 10 Products by Stock
# =======================================

top_stock = products.nlargest(
    10,
    "InStock"
)

print("\nTop 10 Products by Stock:")
print(
    top_stock[
        ["ProductName", "InStock"]
    ]
)

plt.figure(figsize=(10, 6))

plt.bar(
    top_stock["ProductName"],
    top_stock["InStock"],
    color="pink"
)

plt.xlabel("Product")
plt.ylabel("Stock Quantity")
plt.title("Top 10 Products by Stock")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# =======================================
# 15. Top 10 Products by Profit
# =======================================

top_profit = products.nlargest(
    10,
    "Profit"
)

print("\nTop 10 Products by Profit:")
print(
    top_profit[
        ["ProductName", "Profit"]
    ]
)

plt.figure(figsize=(10, 6))

plt.bar(
    top_profit["ProductName"],
    top_profit["Profit"],
    color="green"
)

plt.xlabel("Product")
plt.ylabel("Profit")
plt.title("Top 10 Products by Profit")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# =======================================
# 16. Active / Inactive Products
# =======================================
product_status = products["IsActive"].value_counts()

print("\nActive / Inactive Products:")
print(product_status)

plt.figure(figsize=(10, 6))

plt.bar(
    ["Active", "Inactive"],
    [
        product_status.get(True, 0),
        product_status.get(False, 0)
    ],
    color="pink"
)

plt.xlabel("Product Status")
plt.ylabel("Number of Products")
plt.title("Active vs Inactive Products")

plt.show()


# =======================================
# 17. Close Connection
# =======================================

connection.close()

print("\nDatabase connection closed!")


# =======================================
# 18. InStock Data Type
# =======================================

print("\nInStock Data Type:")
print(products["InStock"].dtype)


# =======================================
# 19. NumPy Selling Price Analysis
# =======================================

prices = products[
    "SellingPrice"
].dropna().to_numpy()

print("\n===== NumPy Selling Price Analysis =====")

print("Average Price:", np.mean(prices))
print("Minimum Price:", np.min(prices))
print("Maximum Price:", np.max(prices))
print("Median Price:", np.median(prices))
print("Standard Deviation:", np.std(prices))

print("25th Percentile:", np.percentile(prices, 25))
print("75th Percentile:", np.percentile(prices, 75))


# =======================================
# 20. Cost vs Selling Price
# =======================================

cost_prices = products[
    "CostPrice"
].dropna().to_numpy()

selling_prices = products[
    "SellingPrice"
].dropna().to_numpy()

print("\n===== Cost vs Selling Price =====")

print(
    "Average Cost Price:",
    np.mean(cost_prices)
)

print(
    "Average Selling Price:",
    np.mean(selling_prices)
)


# =======================================
# 21. Profit Analysis
# =======================================

profit = selling_prices - cost_prices

print("\n===== Profit Analysis =====")

print(
    "Average Profit:",
    np.mean(profit)
)

print(
    "Minimum Profit:",
    np.min(profit)
)

print(
    "Maximum Profit:",
    np.max(profit)
)


# =======================================
# 22. Potential Profit
# =======================================

stock = products[
    "InStock"
].fillna(0).to_numpy()

potential_profit = profit * stock

print("\nTotal Potential Profit:")
print(np.sum(potential_profit))