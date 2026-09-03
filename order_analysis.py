import pyodbc
import pandas as pd
import matplotlib.pyplot as plt


# =========================================================
# 1. DATABASE CONNECTION
# =========================================================

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=ZUBAIR\\SQLEXPRESS;"
    "DATABASE=RetailECommerceDB;"
    "Trusted_Connection=yes;"
)

print("Database connected successfully!")


# =========================================================
# 2. LOAD ORDERS
# =========================================================

orders_query = """
SELECT *
FROM Sales.Orders
"""

orders = pd.read_sql(
    orders_query,
    connection
)


# =========================================================
# 3. LOAD ORDER ITEMS
# =========================================================

items_query = """
SELECT *
FROM Sales.OrderItems
"""

items = pd.read_sql(
    items_query,
    connection
)


# =========================================================
# 4. LOAD CUSTOMERS
# =========================================================

customers_query = """
SELECT *
FROM Sales.Customers
"""

customers = pd.read_sql(
    customers_query,
    connection
)


# =========================================================
# 5. LOAD PRODUCTS + CATEGORIES
# =========================================================

products_query = """
SELECT
    p.ProductID,
    p.ProductName,
    c.CategoryName
FROM Inventory.Products AS p
INNER JOIN Inventory.Categories AS c
    ON p.CategoryID = c.CategoryID
"""

products = pd.read_sql(
    products_query,
    connection
)

print("\nProducts Loaded:")
print(products.head())

print("\nProduct Columns:")
print(products.columns.tolist())


# =========================================================
# 6. CONVERT NUMERIC COLUMNS
# =========================================================

items["Quantity"] = pd.to_numeric(
    items["Quantity"],
    errors="coerce"
)

items["UnitPrice"] = pd.to_numeric(
    items["UnitPrice"],
    errors="coerce"
)


# =========================================================
# 7. CALCULATE REVENUE FOR EACH ORDER ITEM
# =========================================================

items["Revenue"] = (
    items["Quantity"] *
    items["UnitPrice"]
)

print("\nFirst 5 Order Items with Revenue:")

print(
    items[
        [
            "OrderID",
            "ProductID",
            "Quantity",
            "UnitPrice",
            "Revenue"
        ]
    ].head()
)


# =========================================================
# 8. PRODUCT REVENUE ANALYSIS
# =========================================================

product_revenue = (
    items
    .merge(
        products,
        on="ProductID",
        how="left"
    )
)

print("\nOrder Items with Product Names:")

print(
    product_revenue[
        [
            "ProductID",
            "ProductName",
            "CategoryName",
            "Quantity",
            "UnitPrice",
            "Revenue"
        ]
    ].head()
)


# =========================================================
# 9. TOTAL REVENUE
# =========================================================

total_revenue = items["Revenue"].sum()

print("\n================================")
print("TOTAL REVENUE")
print("================================")
print(total_revenue)


# =========================================================
# 10. TOTAL ORDERS
# =========================================================

total_orders = orders["OrderID"].nunique()

print("\nTotal Orders:")
print(total_orders)


# =========================================================
# 11. TOTAL QUANTITY SOLD
# =========================================================

total_quantity = items["Quantity"].sum()

print("\nTotal Quantity Sold:")
print(total_quantity)


# =========================================================
# 12. AVERAGE ORDER VALUE
# =========================================================

if total_orders > 0:

    average_order_value = (
        total_revenue /
        total_orders
    )

else:

    average_order_value = 0


print("\nAverage Order Value:")
print(average_order_value)


# =========================================================
# 13. REVENUE BY CATEGORY
# =========================================================

category_revenue = (
    product_revenue
    .groupby("CategoryName")["Revenue"]
    .sum()
    .sort_values(
        ascending=False
    )
)

print("\nRevenue by Category:")
print(category_revenue)


# =========================================================
# 14. GRAPH - REVENUE BY CATEGORY
# =========================================================

plt.figure(figsize=(10, 6))

plt.bar(
    category_revenue.index,
    category_revenue.values,
    color="aqua"
)

plt.xlabel("Category")
plt.ylabel("Revenue")
plt.title("Revenue by Category")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# =========================================================
# 15. TOP 10 PRODUCTS BY REVENUE
# =========================================================

top_products = (
    product_revenue
    .groupby(
        [
            "ProductID",
            "ProductName"
        ]
    )["Revenue"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
)

print("\nTop 10 Products by Revenue:")
print(top_products)


# =========================================================
# 16. GRAPH - TOP PRODUCTS BY REVENUE
# =========================================================

top_products_df = (
    top_products
    .reset_index()
)

plt.figure(figsize=(10, 6))

plt.bar(
    top_products_df["ProductName"],
    top_products_df["Revenue"],
    color="grey"
)

plt.xlabel("Product")
plt.ylabel("Revenue")
plt.title("Top 10 Products by Revenue")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# =========================================================
# 17. TOP 10 PRODUCTS BY QUANTITY SOLD
# =========================================================

top_quantity = (
    product_revenue
    .groupby(
        [
            "ProductID",
            "ProductName"
        ]
    )["Quantity"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
)

print("\nTop 10 Products by Quantity Sold:")
print(top_quantity)


# =========================================================
# 18. GRAPH - TOP PRODUCTS BY QUANTITY
# =========================================================

top_quantity_df = (
    top_quantity
    .reset_index()
)

plt.figure(figsize=(10, 6))

plt.bar(
    top_quantity_df["ProductName"],
    top_quantity_df["Quantity"],
    color="red"
)

plt.xlabel("Product")
plt.ylabel("Quantity Sold")
plt.title("Top 10 Products by Quantity Sold")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# =========================================================
# 19. TOP CUSTOMERS BY REVENUE
# =========================================================

customer_revenue = (
    orders[
        [
            "OrderID",
            "CustomerID"
        ]
    ]
    .merge(
        items[
            [
                "OrderID",
                "Revenue"
            ]
        ],
        on="OrderID",
        how="inner"
    )
    .groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(
        ascending=False
    )
)

print("\nTop 10 Customers by Revenue:")
print(
    customer_revenue.head(10)
)


# =========================================================
# 20. ADD CUSTOMER NAMES
# =========================================================

customer_revenue_df = (
    customer_revenue
    .reset_index()
    .merge(
        customers[
            [
                "CustomerID",
                "FirstName",
                "LastName"
            ]
        ],
        on="CustomerID",
        how="left"
    )
)

customer_revenue_df["CustomerName"] = (
    customer_revenue_df["FirstName"]
    + " "
    + customer_revenue_df["LastName"]
)

print("\nTop 10 Customers:")

print(
    customer_revenue_df[
        [
            "CustomerID",
            "CustomerName",
            "Revenue"
        ]
    ].head(10)
)


# =========================================================
# 21. GRAPH - TOP CUSTOMERS
# =========================================================

top_customers = (
    customer_revenue_df
    .head(10)
)

plt.figure(figsize=(10, 6))

plt.bar(
    top_customers["CustomerName"],
    top_customers["Revenue"],
    color="brown"
)

plt.xlabel("Customer")
plt.ylabel("Revenue")
plt.title("Top 10 Customers by Revenue")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# =========================================================
# 22. ORDER STATUS ANALYSIS
# =========================================================

status_count = (
    orders["Status"]
    .value_counts()
)

print("\nOrders by Status:")
print(status_count)


# =========================================================
# 23. GRAPH - ORDER STATUS
# =========================================================

plt.figure(figsize=(8, 5))

plt.bar(
    status_count.index,
    status_count.values,
    color="pink"
)

plt.xlabel("Order Status")
plt.ylabel("Number of Orders")
plt.title("Orders by Status")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# =========================================================
# 24. ORDERS OVER TIME
# =========================================================

orders["OrderDate"] = pd.to_datetime(
    orders["OrderDate"]
)

monthly_orders = (
    orders
    .groupby(
        orders["OrderDate"].dt.to_period("M")
    )
    .size()
)

print("\nOrders by Month:")
print(monthly_orders)


# =========================================================
# 25. GRAPH - ORDERS OVER TIME
# =========================================================

plt.figure(figsize=(10, 6))

plt.plot(
    monthly_orders.index.astype(str),
    monthly_orders.values,
    marker="o",
    color="pink"
)

plt.xlabel("Month")
plt.ylabel("Number of Orders")
plt.title("Orders Over Time")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# =========================================================
# 26. FINAL BUSINESS INSIGHTS
# =========================================================

print("\n=======================================")
print("FINAL BUSINESS INSIGHTS")
print("=======================================")

print("\nTotal Revenue:")
print(total_revenue)

print("\nTotal Orders:")
print(total_orders)

print("\nTotal Quantity Sold:")
print(total_quantity)

print("\nAverage Order Value:")
print(average_order_value)


# Best Product

print("\nBest Product by Revenue:")

print(
    top_products_df.iloc[0]
)


# Best Category

print("\nBest Category by Revenue:")

print(
    category_revenue.idxmax()
)


print("\nBest Category Revenue:")

print(
    category_revenue.max()
)


# Best Customer

print("\nBest Customer by Revenue:")

print(
    customer_revenue_df.iloc[0][
        [
            "CustomerID",
            "CustomerName",
            "Revenue"
        ]
    ]
)


# =========================================================
# 27. CLOSE DATABASE CONNECTION
# =========================================================

connection.close()

print("\nDatabase connection closed!")