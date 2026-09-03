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
# 2. LOAD SALES DATA
# =======================================

sales_query = """
SELECT
    o.OrderID,
    oi.ProductID,
    p.ProductName,
    c.CategoryName,
    oi.Quantity,
    oi.UnitPrice,
    (oi.Quantity * oi.UnitPrice) AS Revenue,
    o.OrderDate
FROM Sales.Orders o
JOIN Sales.OrderItems oi
    ON o.OrderID = oi.OrderID
JOIN Inventory.Products p
    ON oi.ProductID = p.ProductID
JOIN Inventory.Categories c
    ON p.CategoryID = c.CategoryID
"""

sales = pd.read_sql(sales_query, connection)

print("Sales Loaded:", len(sales))


# =======================================
# 3. LOAD PAYMENTS
# =======================================

payments_query = """
SELECT
    PaymentID,
    OrderID,
    Amount,
    PaymentMethod,
    PaymentDate
FROM Sales.Payments
"""

payments = pd.read_sql(payments_query, connection)

print("Payments Loaded:", len(payments))


# =======================================
# 4. LOAD REVIEWS
# =======================================

reviews_query = """
SELECT
    ReviewID,
    CustomerID,
    ProductID,
    Rating,
    ReviewDate
FROM Sales.Reviews
"""

reviews = pd.read_sql(reviews_query, connection)

print("Reviews Loaded:", len(reviews))


# =======================================
# 5. LOAD SHIPMENTS
# =======================================

shipments_query = """
SELECT
    ShipmentID,
    OrderID,
    Courier,
    ShippingDate,
    DeliveryDate
FROM Sales.Shipments
"""

shipments = pd.read_sql(shipments_query, connection)

print("Shipments Loaded:", len(shipments))


# =======================================
# 6. LOAD INVENTORY
# =======================================

inventory_query = """
SELECT
    ProductID,
    QuantityInStock,
    ReorderLevel
FROM Inventory.Inventory
"""

inventory = pd.read_sql(inventory_query, connection)

print("Inventory Loaded:", len(inventory))


# =======================================
# 7. LOAD ADDRESSES
# =======================================

address_query = """
SELECT
    AddressID,
    CustomerID,
    City,
    StateProvince,
    Country
FROM Sales.Addresses
"""

addresses = pd.read_sql(address_query, connection)

print("Addresses Loaded:", len(addresses))


# =======================================
# 8. GRAPH 1
# REVENUE BY CATEGORY
# =======================================

category_revenue = (
    sales.groupby("CategoryName")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))

category_revenue.plot(kind="bar")

plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# =======================================
# 9. GRAPH 2
# MONTHLY REVENUE
# =======================================

sales["OrderDate"] = pd.to_datetime(sales["OrderDate"])

monthly_revenue = (
    sales.groupby(
        sales["OrderDate"].dt.to_period("M")
    )["Revenue"]
    .sum()
)

plt.figure(figsize=(12, 6))

monthly_revenue.plot(kind="line", marker="o")

plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# =======================================
# 10. GRAPH 3
# TOP 10 PRODUCTS
# =======================================

top_products = (
    sales.groupby("ProductName")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))

top_products.sort_values().plot(kind="barh")

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")

plt.tight_layout()

plt.show()


# =======================================
# 11. GRAPH 4
# PAYMENT METHOD
# =======================================

payment_revenue = (
    payments.groupby("PaymentMethod")["Amount"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 6))

payment_revenue.plot(kind="bar")

plt.title("Revenue by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Payment Amount")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# =======================================
# 12. GRAPH 5
# RATING DISTRIBUTION
# =======================================

rating_counts = reviews["Rating"].value_counts().sort_index()

plt.figure(figsize=(8, 5))

rating_counts.plot(kind="bar")

plt.title("Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of Reviews")

plt.tight_layout()

plt.show()


# =======================================
# 13. GRAPH 6
# SHIPMENTS BY COURIER
# =======================================

courier_counts = (
    shipments["Courier"]
    .value_counts()
)

plt.figure(figsize=(8, 5))

courier_counts.plot(kind="bar")

plt.title("Shipments by Courier")
plt.xlabel("Courier")
plt.ylabel("Number of Shipments")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# =======================================
# 14. GRAPH 7
# INVENTORY STATUS
# =======================================

inventory["StockStatus"] = inventory.apply(
    lambda row:
        "Out of Stock"
        if row["QuantityInStock"] == 0
        else
        "Low Stock"
        if row["QuantityInStock"] <= row["ReorderLevel"]
        else
        "In Stock",
    axis=1
)

stock_status = inventory["StockStatus"].value_counts()

plt.figure(figsize=(8, 5))

stock_status.plot(kind="bar")

plt.title("Inventory Stock Status")
plt.xlabel("Stock Status")
plt.ylabel("Number of Products")

plt.tight_layout()

plt.show()


# =======================================
# 15. GRAPH 8
# ADDRESSES BY CITY
# =======================================

city_counts = (
    addresses["City"]
    .value_counts()
)

plt.figure(figsize=(10, 6))

city_counts.plot(kind="bar")

plt.title("Customers by City")
plt.xlabel("City")
plt.ylabel("Number of Customers")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# =======================================
# 16. CLOSE CONNECTION
# =======================================

connection.close()

print("\n======================================")
print("ALL DASHBOARD GRAPHS COMPLETED")
print("======================================")

print("Database connection closed!")