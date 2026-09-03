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
products["InStock"] = pd.to_numeric(
    products["InStock"],
    errors="coerce"
)
##Convert numeric columns
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
    top_products["SellingPrice"]
    color="red"
)

plt.xlabel("Product")
plt.ylabel("Selling Price")
plt.title("Top 10 Most Expensive Products")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
# =======================================
# 14. Cost Price vs Selling Price
# =======================================

plt.figure(figsize=(8, 6))

plt.scatter(
    products["CostPrice"],
    products["SellingPrice"]
    color="green"
)

plt.xlabel("Cost Price")
plt.ylabel("Selling Price")
plt.title("Cost Price vs Selling Price")

plt.tight_layout()

plt.show()
# =======================================
# 15. Top 10 Products by Stock
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
    color="yellow"
)

plt.figure(figsize=(10, 6))

plt.bar(
    top_stock["ProductName"],
    top_stock["InStock"]
)

plt.xlabel("Product")
plt.ylabel("Stock Quantity")
plt.title("Top 10 Products by Stock")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
# =======================================
# 16. Top 10 Products by Profit
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
    color="pink"
)

plt.figure(figsize=(5, 2))

plt.bar(
    top_profit["ProductName"],
    top_profit["Profit"]
)

plt.xlabel("Product")
plt.ylabel("Profit")
plt.title("Top 10 Products by Profit")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
# =======================================
# 17. Active / Inactive Products
# =======================================

product_status = products["IsActive"].value_counts()

print("\nActive / Inactive Products:")
print(product_status)
plt.figure(figsize=(6, 5))

plt.bar(
    ["Active", "Inactive"],
    [
        product_status.get(True, 0),
        product_status.get(False, 0)
    ]
       color="orange"
)

plt.xlabel("Product Status")
plt.ylabel("Number of Products")
plt.title("Active vs Inactive Products")

plt.show()


# =======================================
# 13. Close Connection
# =======================================

connection.close()

print("\nDatabase connection closed!")
print("\nInStock Data Type:")
print(products["InStock"].dtype)

# =======================================
# NumPy Analysis
# =======================================

prices = products["SellingPrice"].dropna().to_numpy()

print("\nSelling Prices:")
print(prices)
average_price = np.mean(prices)

# =======================================
# NumPy Analysis
# =======================================

prices = products["SellingPrice"].dropna().to_numpy()

print("\n===== NumPy Selling Price Analysis =====")

print("Average Price:", np.mean(prices))
print("Minimum Price:", np.min(prices))
print("Maximum Price:", np.max(prices))
print("Median Price:", np.median(prices))
print("Standard Deviation:", np.std(prices))

print("25th Percentile:", np.percentile(prices, 25))
print("75th Percentile:", np.percentile(prices, 75))


# =======================================
# Cost vs Selling Price
# =======================================

cost_prices = products["CostPrice"].dropna().to_numpy()
selling_prices = products["SellingPrice"].dropna().to_numpy()

print("\n===== Cost vs Selling Price =====")

print("Average Cost Price:", np.mean(cost_prices))
print("Average Selling Price:", np.mean(selling_prices))


# =======================================
# Profit Analysis
# =======================================

profit = selling_prices - cost_prices

print("\n===== Profit Analysis =====")

print("Average Profit:", np.mean(profit))
print("Minimum Profit:", np.min(profit))
print("Maximum Profit:", np.max(profit))


# =======================================
# Potential Profit
# =======================================

stock = products["InStock"].fillna(0).to_numpy()

potential_profit = profit * stock

print("\nTotal Potential Profit:")
print(np.sum(potential_profit))


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
    category_revenue.values
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
    top_products_df["Revenue"]
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
    top_quantity_df["Quantity"]
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
    top_customers["Revenue"]
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
    status_count.values
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
    marker="o"
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

import pyodbc

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=ZUBAIR\\SQLEXPRESS;"
    "DATABASE=RetailECommerceDB;"
    "Trusted_Connection=yes;"
)

print("Database connected successfully!")

cursor = connection.cursor()

cursor.execute("""
    SELECT TABLE_SCHEMA, TABLE_NAME
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_TYPE = 'BASE TABLE'
    ORDER BY TABLE_SCHEMA, TABLE_NAME
""")

print("\nTables in RetailECommerceDB:\n")

for row in cursor.fetchall():
    print(row)

connection.close()

import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
# ---------------------------------------
# 1. Connect to SQL Server
# ---------------------------------------

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=ZUBAIR\\SQLEXPRESS;"
    "DATABASE=RetailECommerceDB;"
    "Trusted_Connection=yes;"
)

print("Database connected successfully!")


# ---------------------------------------
# 2. SQL Query
# ---------------------------------------

query = """
SELECT *
FROM Sales.Customers
"""


# ---------------------------------------
# 3. Load data into DataFrame
# ---------------------------------------

df = pd.read_sql(query, connection)
# ---------------------------------------
# Active vs Inactive Customers
# ---------------------------------------

customer_status = df["IsActive"].value_counts()

print("\nCustomer Status:")
print(customer_status)

plt.bar(
    ["Active", "Inactive"],
    [
        customer_status.get(True, 0),
        customer_status.get(False, 0)
    ]
)

plt.xlabel("Customer Status")
plt.ylabel("Number of Customers")
plt.title("Active vs Inactive Customers")

plt.show()


# ---------------------------------------
# 4. First 5 rows
# ---------------------------------------

print("\nFirst 5 Customers:")
print(df.head())


# ---------------------------------------
# 5. Last 5 rows
# ---------------------------------------

print("\nLast 5 Customers:")
print(df.tail())


# ---------------------------------------
# 6. Number of rows and columns
# ---------------------------------------

print("\nShape:")
print(df.shape)


# ---------------------------------------
# 7. Column names
# ---------------------------------------

print("\nColumns:")
print(df.columns)


# ---------------------------------------
# 8. Data information
# ---------------------------------------

print("\nData Information:")
df.info()


# ---------------------------------------
# 9. Total customers
# ---------------------------------------

print("\nTotal Customers:")
print(len(df))


# ---------------------------------------
# 10. Active / Inactive customers
# ---------------------------------------

print("\nActive / Inactive Customers:")
print(df["IsActive"].value_counts())


# ---------------------------------------
# 11. Missing values
# ---------------------------------------

print("\nMissing Values:")
print(df.isnull().sum())


# ---------------------------------------
# 12. Convert DateJoined to datetime
# ---------------------------------------

df["DateJoined"] = pd.to_datetime(df["DateJoined"])
# ---------------------------------------
# Customers Joined by Date
# ---------------------------------------

customers_by_date = df.groupby(
    df["DateJoined"].dt.date
).size()

plt.plot(
    customers_by_date.index,
    customers_by_date.values,
    marker="o"
)

plt.xlabel("Date")
plt.ylabel("Number of Customers")
plt.title("Customers Joined Over Time")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()
# ---------------------------------------
# Customer Status Pie Chart
# ---------------------------------------

labels = ["Active", "Inactive"]

values = [
    customer_status.get(True, 0),
    customer_status.get(False, 0)
]

plt.pie(
    values,
    labels=labels,
    autopct="%1.1f%%"
)

plt.title("Customer Status Distribution")

plt.show()

print("\nDateJoined Data Type:")
print(df["DateJoined"].dtype)


# ---------------------------------------
# 13. Joining dates
# ---------------------------------------

print("\nFirst Joining Date:")
print(df["DateJoined"].min())

print("\nLatest Joining Date:")
print(df["DateJoined"].max())


# ---------------------------------------
# 14. Customer ID statistics
# ---------------------------------------

print("\nCustomer ID Statistics:")
print(df["CustomerID"].describe())


# ---------------------------------------
# 15. Close connection
# ---------------------------------------

connection.close()

print("\nDatabase connection closed!")

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
    category_count.values
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
    average_price_category.values
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
    category_sales.values
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