import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

# =======================================
# 1. Database Connection
# =======================================

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=ZUBAIR\\SQLEXPRESS;"
    "DATABASE=RetailECommerceDB;"
    "Trusted_Connection=yes;"
)

print("Database connected successfully!")


# =======================================
# 2. Products + Categories
# =======================================

query = """
SELECT
    p.ProductID,
    p.ProductName,
    p.CategoryID,
    c.CategoryName,
    p.CostPrice,
    p.SellingPrice,
    p.IsActive,
    p.InStock,
    p.InOrder
FROM Inventory.Products AS p
INNER JOIN Inventory.Categories AS c
    ON p.CategoryID = c.CategoryID
"""

products = pd.read_sql(query, connection)


# =======================================
# 3. Convert numeric columns
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


# =======================================
# 4. Products by Category
# =======================================

category_count = products["CategoryName"].value_counts()

print("\nProducts by Category:")
print(category_count)

print("\nMost Products Category:")
print(category_count.idxmax())

print("\nLeast Products Category:")
print(category_count.idxmin())


# =======================================
# 5. Graph 1
# =======================================

plt.figure(figsize=(10, 6))

plt.bar(
    category_count.index,
    category_count.values,
    color="pink"
)

plt.xlabel("Category")
plt.ylabel("Number of Products")
plt.title("Number of Products by Category")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# =======================================
# 6. Average Selling Price
# =======================================

average_price_category = products.groupby(
    "CategoryName"
)["SellingPrice"].mean()

print("\nAverage Selling Price by Category:")
print(average_price_category)


# =======================================
# 7. Graph 2
# =======================================

plt.figure(figsize=(10, 6))

plt.bar(
    average_price_category.index,
    average_price_category.values,
    color="grey"
)

plt.xlabel("Category")
plt.ylabel("Average Selling Price")
plt.title("Average Selling Price by Category")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# =======================================
# 8. Potential Sales
# =======================================

products["PotentialSales"] = (
    products["SellingPrice"] *
    products["InStock"]
)

category_sales = products.groupby(
    "CategoryName"
)["PotentialSales"].sum()

print("\nPotential Sales by Category:")
print(category_sales)


# =======================================
# 9. Graph 3
# =======================================

plt.figure(figsize=(10, 6))

plt.bar(
    category_sales.index,
    category_sales.values,
    color="black"
)

plt.xlabel("Category")
plt.ylabel("Potential Sales")
plt.title("Potential Sales Value by Category")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# =======================================
# 10. Close connection
# =======================================

connection.close()

print("\nDatabase connection closed!")