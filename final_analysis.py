import pyodbc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")


# ============================================================
# FINAL RETAIL E-COMMERCE BUSINESS ANALYSIS
# ============================================================

print("=" * 70)
print("          RETAIL E-COMMERCE BUSINESS ANALYSIS")
print("=" * 70)


# ============================================================
# 1. DATABASE CONNECTION
# ============================================================

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=ZUBAIR\\SQLEXPRESS;"
    "DATABASE=RetailECommerceDB;"
    "Trusted_Connection=yes;"
)

print("\nDatabase connected successfully!")


# ============================================================
# 2. LOAD CUSTOMERS
# ============================================================

customers = pd.read_sql("""
    SELECT
        CustomerID,
        FirstName,
        LastName,
        IsActive
    FROM Sales.Customers
""", connection)

print("Customers Loaded:", len(customers))


# ============================================================
# 3. LOAD ORDERS
# ============================================================

orders = pd.read_sql("""
    SELECT
        OrderID,
        CustomerID,
        OrderDate,
        Status
    FROM Sales.Orders
""", connection)

print("Orders Loaded:", len(orders))


# ============================================================
# 4. LOAD ORDER ITEMS
# ============================================================

items = pd.read_sql("""
    SELECT
        OrderItemID,
        OrderID,
        ProductID,
        Quantity,
        UnitPrice
    FROM Sales.OrderItems
""", connection)

print("Order Items Loaded:", len(items))


# ============================================================
# 5. LOAD PRODUCTS + CATEGORY
# ============================================================

products = pd.read_sql("""
    SELECT
        p.ProductID,
        p.ProductName,
        p.CategoryID,
        c.CategoryName,
        p.SupplierID,
        p.CostPrice,
        p.SellingPrice
    FROM Inventory.Products AS p
    INNER JOIN Inventory.Categories AS c
        ON p.CategoryID = c.CategoryID
""", connection)

print("Products Loaded:", len(products))


# ============================================================
# 6. LOAD PAYMENTS
# ============================================================

payments = pd.read_sql("""
    SELECT
        PaymentID,
        OrderID,
        Amount,
        PaymentMethod,
        PaymentDate
    FROM Sales.Payments
""", connection)

print("Payments Loaded:", len(payments))


# ============================================================
# 7. LOAD REVIEWS
# ============================================================

reviews = pd.read_sql("""
    SELECT
        ReviewID,
        CustomerID,
        ProductID,
        Rating,
        ReviewDate
    FROM Sales.Reviews
""", connection)

print("Reviews Loaded:", len(reviews))


# ============================================================
# 8. LOAD ADDRESSES
# ============================================================

addresses = pd.read_sql("""
    SELECT
        AddressID,
        CustomerID,
        AddressLine1,
        City,
        StateProvince,
        PostalCode,
        Country
    FROM Sales.Addresses
""", connection)

print("Addresses Loaded:", len(addresses))


# ============================================================
# 9. LOAD SHIPMENTS
# ============================================================

shipments = pd.read_sql("""
    SELECT
        ShipmentID,
        OrderID,
        Courier,
        TrackingNumber,
        ShippingDate,
        DeliveryDate
    FROM Sales.Shipments
""", connection)

print("Shipments Loaded:", len(shipments))


# ============================================================
# 10. LOAD SUPPLIERS
# ============================================================

supplier_table = None

for schema in ["Purchasing", "Inventory", "Sales", "dbo"]:

    check = pd.read_sql(f"""
        SELECT COUNT(*) AS TableCount
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = '{schema}'
        AND TABLE_NAME = 'Suppliers'
    """, connection)

    if int(check.iloc[0]["TableCount"]) > 0:
        supplier_table = f"[{schema}].[Suppliers]"
        break


if supplier_table is None:

    raise RuntimeError(
        "Suppliers table was not found."
    )


suppliers = pd.read_sql(f"""
    SELECT
        SupplierID,
        SupplierName,
        Email,
        Phone
    FROM {supplier_table}
""", connection)

print("Suppliers Loaded:", len(suppliers))
print("Supplier Table Used:", supplier_table)


# ============================================================
# 11. LOAD INVENTORY
# ============================================================

inventory = pd.read_sql("""
    SELECT
        ProductID,
        QuantityInStock,
        ReorderLevel
    FROM Inventory.Inventory
""", connection)

print("Inventory Loaded:", len(inventory))


# ============================================================
# 12. LOAD EMPLOYEES
# ============================================================

employees = pd.read_sql("""
    SELECT
        EmployeeID,
        FirstName,
        LastName,
        Email
    FROM HR.Employees
""", connection)

print("Employees Loaded:", len(employees))


# ============================================================
# 13. DATA CLEANING
# ============================================================

items["Quantity"] = pd.to_numeric(
    items["Quantity"],
    errors="coerce"
).fillna(0)

items["UnitPrice"] = pd.to_numeric(
    items["UnitPrice"],
    errors="coerce"
).fillna(0)

payments["Amount"] = pd.to_numeric(
    payments["Amount"],
    errors="coerce"
).fillna(0)

reviews["Rating"] = pd.to_numeric(
    reviews["Rating"],
    errors="coerce"
)

products["SellingPrice"] = pd.to_numeric(
    products["SellingPrice"],
    errors="coerce"
).fillna(0)

products["CostPrice"] = pd.to_numeric(
    products["CostPrice"],
    errors="coerce"
).fillna(0)

inventory["QuantityInStock"] = pd.to_numeric(
    inventory["QuantityInStock"],
    errors="coerce"
).fillna(0)

inventory["ReorderLevel"] = pd.to_numeric(
    inventory["ReorderLevel"],
    errors="coerce"
).fillna(0)


orders["OrderDate"] = pd.to_datetime(
    orders["OrderDate"],
    errors="coerce"
)

payments["PaymentDate"] = pd.to_datetime(
    payments["PaymentDate"],
    errors="coerce"
)

reviews["ReviewDate"] = pd.to_datetime(
    reviews["ReviewDate"],
    errors="coerce"
)

shipments["ShippingDate"] = pd.to_datetime(
    shipments["ShippingDate"],
    errors="coerce"
)

shipments["DeliveryDate"] = pd.to_datetime(
    shipments["DeliveryDate"],
    errors="coerce"
)


# ============================================================
# 14. CALCULATE REVENUE
# ============================================================

items["Revenue"] = (
    items["Quantity"] *
    items["UnitPrice"]
)


# ============================================================
# 15. CREATE MASTER SALES DATA
# ============================================================

sales_data = items.merge(
    products,
    on="ProductID",
    how="left"
)

sales_data = sales_data.merge(
    orders[
        [
            "OrderID",
            "CustomerID",
            "OrderDate",
            "Status"
        ]
    ],
    on="OrderID",
    how="left"
)

sales_data = sales_data.merge(
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


# Customer Name
sales_data["CustomerName"] = (
    sales_data["FirstName"].fillna("").astype(str)
    + " "
    + sales_data["LastName"].fillna("").astype(str)
).str.strip()


print("\nSales master data created successfully.")


# ============================================================
# 16. CUSTOMER KPIs
# ============================================================

total_customers = customers["CustomerID"].nunique()

active_customers = (
    customers["IsActive"]
    .eq(True)
    .sum()
)

inactive_customers = (
    customers["IsActive"]
    .eq(False)
    .sum()
)


# ============================================================
# 17. ADDRESS KPIs
# ============================================================

total_addresses = len(addresses)

unique_cities = addresses["City"].nunique()

city_counts = addresses["City"].value_counts()

state_counts = addresses["StateProvince"].value_counts()

country_counts = addresses["Country"].value_counts()


most_common_city = (
    city_counts.idxmax()
    if len(city_counts) > 0
    else "N/A"
)

most_common_state = (
    state_counts.idxmax()
    if len(state_counts) > 0
    else "N/A"
)

most_common_country = (
    country_counts.idxmax()
    if len(country_counts) > 0
    else "N/A"
)


# ============================================================
# 18. PRODUCT KPIs
# ============================================================

total_products = products["ProductID"].nunique()


# ============================================================
# 19. INVENTORY KPIs
# ============================================================

total_stock = inventory["QuantityInStock"].sum()

average_stock = inventory["QuantityInStock"].mean()

low_stock = inventory[
    (inventory["QuantityInStock"] > 0)
    &
    (
        inventory["QuantityInStock"]
        <= inventory["ReorderLevel"]
    )
]

out_of_stock = inventory[
    inventory["QuantityInStock"] == 0
]

reorder_required = inventory[
    inventory["QuantityInStock"]
    <= inventory["ReorderLevel"]
]


# ============================================================
# 20. SALES KPIs
# ============================================================

total_orders = orders["OrderID"].nunique()

total_quantity = items["Quantity"].sum()

total_revenue = items["Revenue"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)


# ============================================================
# 21. PAYMENT KPIs
# ============================================================

total_payments = payments["PaymentID"].nunique()

total_payment_amount = payments["Amount"].sum()

average_payment = payments["Amount"].mean()


# ============================================================
# 22. REVIEW KPIs
# ============================================================

total_reviews = reviews["ReviewID"].nunique()

average_rating = reviews["Rating"].mean()

rating_counts = (
    reviews["Rating"]
    .dropna()
    .value_counts()
    .sort_index()
)

most_common_rating = (
    rating_counts.idxmax()
    if len(rating_counts) > 0
    else "N/A"
)


# ============================================================
# 23. SHIPMENT KPIs
# ============================================================

total_shipments = len(shipments)

delivered_shipments = (
    shipments["DeliveryDate"]
    .notna()
    .sum()
)

pending_shipments = (
    shipments["DeliveryDate"]
    .isna()
    .sum()
)

courier_counts = shipments["Courier"].value_counts()

most_used_courier = (
    courier_counts.idxmax()
    if len(courier_counts) > 0
    else "N/A"
)


# Delivery Time

delivered_data = shipments[
    shipments["DeliveryDate"].notna()
    &
    shipments["ShippingDate"].notna()
].copy()


delivered_data["DeliveryDays"] = (
    delivered_data["DeliveryDate"]
    -
    delivered_data["ShippingDate"]
).dt.days


if len(delivered_data) > 0:

    average_delivery_time = (
        delivered_data["DeliveryDays"].mean()
    )

    average_delivery_by_courier = (
        delivered_data
        .groupby("Courier")["DeliveryDays"]
        .mean()
        .sort_values()
    )

else:

    average_delivery_time = 0

    average_delivery_by_courier = pd.Series(
        dtype=float
    )


if len(average_delivery_by_courier) > 0:

    best_courier = (
        average_delivery_by_courier.idxmin()
    )

    best_courier_average = (
        average_delivery_by_courier.min()
    )

else:

    best_courier = "N/A"

    best_courier_average = 0


# ============================================================
# 24. SUPPLIER KPIs
# ============================================================

total_suppliers = len(suppliers)


products_supplier = products[
    [
        "ProductID",
        "SupplierID",
        "ProductName",
        "SellingPrice"
    ]
].copy()


supplier_price_data = products_supplier.merge(
    suppliers[
        [
            "SupplierID",
            "SupplierName"
        ]
    ],
    on="SupplierID",
    how="left"
)


average_supplier_price = (
    supplier_price_data
    .groupby("SupplierName")["SellingPrice"]
    .mean()
    .sort_values(ascending=False)
)


supplier_inventory_data = products_supplier.merge(
    inventory[
        [
            "ProductID",
            "QuantityInStock"
        ]
    ],
    on="ProductID",
    how="left"
)


supplier_inventory_data = (
    supplier_inventory_data
    .merge(
        suppliers[
            [
                "SupplierID",
                "SupplierName"
            ]
        ],
        on="SupplierID",
        how="left"
    )
)


supplier_stock = (
    supplier_inventory_data
    .groupby("SupplierName")["QuantityInStock"]
    .sum()
    .sort_values(ascending=False)
)


if len(average_supplier_price) > 0:

    highest_price_supplier = (
        average_supplier_price.idxmax()
    )

    highest_average_price = (
        average_supplier_price.max()
    )

else:

    highest_price_supplier = "N/A"
    highest_average_price = 0


if len(supplier_stock) > 0:

    highest_inventory_supplier = (
        supplier_stock.idxmax()
    )

    highest_supplier_inventory = (
        supplier_stock.max()
    )

else:

    highest_inventory_supplier = "N/A"
    highest_supplier_inventory = 0


# ============================================================
# 25. EMPLOYEE KPI
# ============================================================

total_employees = len(employees)


# ============================================================
# 26. TOP PRODUCTS
# ============================================================

top_products = (
    sales_data
    .groupby(
        [
            "ProductID",
            "ProductName"
        ]
    )["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

top_products_df = (
    top_products
    .head(10)
    .reset_index()
)


# ============================================================
# 27. CATEGORY REVENUE
# ============================================================

category_revenue = (
    sales_data
    .groupby("CategoryName")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)


# ============================================================
# 28. TOP CUSTOMERS
# ============================================================

top_customers = (
    sales_data
    .groupby(
        [
            "CustomerID",
            "CustomerName"
        ]
    )["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)


# ============================================================
# 29. MONTHLY REVENUE
# ============================================================

monthly_sales = sales_data.dropna(
    subset=["OrderDate"]
).copy()


monthly_sales["Month"] = (
    monthly_sales["OrderDate"]
    .dt.to_period("M")
)


monthly_revenue = (
    monthly_sales
    .groupby("Month")["Revenue"]
    .sum()
)


# ============================================================
# 30. PAYMENT METHOD
# ============================================================

payment_method_revenue = (
    payments
    .groupby("PaymentMethod")["Amount"]
    .sum()
    .sort_values(ascending=False)
)


# ============================================================
# 31. TOP RATED PRODUCTS
# ============================================================

product_ratings = (
    reviews
    .merge(
        products[
            [
                "ProductID",
                "ProductName"
            ]
        ],
        on="ProductID",
        how="left"
    )
    .groupby(
        [
            "ProductID",
            "ProductName"
        ]
    )["Rating"]
    .mean()
    .sort_values(ascending=False)
)


# ============================================================
# 32. STOCK STATUS
# ============================================================

inventory["StockStatus"] = np.where(
    inventory["QuantityInStock"] == 0,
    "Out of Stock",
    np.where(
        inventory["QuantityInStock"]
        <= inventory["ReorderLevel"],
        "Low Stock",
        "In Stock"
    )
)


stock_status = (
    inventory["StockStatus"]
    .value_counts()
)


# ============================================================
# 33. PROFIT & MARGIN ANALYSIS
# ============================================================

print("\n")
print("=" * 70)
print("                 PROFIT & MARGIN ANALYSIS")
print("=" * 70)


# Profit per unit

sales_data["ProfitPerUnit"] = (
    sales_data["SellingPrice"]
    -
    sales_data["CostPrice"]
)


# Total profit

sales_data["TotalProfit"] = (
    sales_data["ProfitPerUnit"]
    *
    sales_data["Quantity"]
)


# Profit margin

sales_data["ProfitMargin"] = np.where(
    sales_data["SellingPrice"] != 0,
    (
        sales_data["ProfitPerUnit"]
        /
        sales_data["SellingPrice"]
    ) * 100,
    0
)


# Total business profit

total_profit = (
    sales_data["TotalProfit"].sum()
)


# Average profit per unit

average_profit_per_unit = (
    sales_data["ProfitPerUnit"].mean()
    if len(sales_data) > 0
    else 0
)


# Average profit margin

average_profit_margin = (
    sales_data["ProfitMargin"].mean()
    if len(sales_data) > 0
    else 0
)


# ============================================================
# PROFIT BY PRODUCT
# ============================================================

profit_by_product = (
    sales_data
    .groupby(
        [
            "ProductID",
            "ProductName"
        ]
    )["TotalProfit"]
    .sum()
    .sort_values(ascending=False)
)


# ============================================================
# PROFIT BY CATEGORY
# ============================================================

profit_by_category = (
    sales_data
    .groupby("CategoryName")["TotalProfit"]
    .sum()
    .sort_values(ascending=False)
)


# ============================================================
# PROFIT MARGIN BY PRODUCT
# ============================================================

product_profit_margin = (
    sales_data
    .groupby(
        [
            "ProductID",
            "ProductName"
        ]
    )["ProfitMargin"]
    .mean()
    .sort_values(ascending=False)
)


# ============================================================
# TOP 10 PROFITABLE PRODUCTS
# ============================================================

top_profit_products = (
    profit_by_product
    .head(10)
    .reset_index()
)


# ============================================================
# TOP 10 PRODUCTS BY PROFIT MARGIN
# ============================================================

top_margin_products = (
    product_profit_margin
    .head(10)
    .reset_index()
)


# ============================================================
# BEST PROFITABLE PRODUCT
# ============================================================

if len(profit_by_product) > 0:

    best_profit_product = (
        profit_by_product.idxmax()
    )

    best_profit_value = (
        profit_by_product.max()
    )

else:

    best_profit_product = ("N/A", "N/A")
    best_profit_value = 0


# ============================================================
# BEST PROFITABLE CATEGORY
# ============================================================

if len(profit_by_category) > 0:

    best_profit_category = (
        profit_by_category.idxmax()
    )

    best_category_profit = (
        profit_by_category.max()
    )

else:

    best_profit_category = "N/A"
    best_category_profit = 0


# ============================================================
# BEST PROFIT MARGIN PRODUCT
# ============================================================

if len(product_profit_margin) > 0:

    best_margin_product = (
        product_profit_margin.idxmax()
    )

    best_margin_value = (
        product_profit_margin.max()
    )

else:

    best_margin_product = ("N/A", "N/A")
    best_margin_value = 0


# ============================================================
# 34. FINAL BEST PERFORMERS
# ============================================================

best_product_name = (
    top_products_df.iloc[0]["ProductName"]
    if len(top_products_df) > 0
    else "N/A"
)

best_product_revenue = (
    top_products_df.iloc[0]["Revenue"]
    if len(top_products_df) > 0
    else 0
)


best_category = (
    category_revenue.idxmax()
    if len(category_revenue) > 0
    else "N/A"
)

best_category_revenue = (
    category_revenue.max()
    if len(category_revenue) > 0
    else 0
)


best_customer_name = (
    top_customers.iloc[0]["CustomerName"]
    if len(top_customers) > 0
    else "N/A"
)

best_customer_revenue = (
    top_customers.iloc[0]["Revenue"]
    if len(top_customers) > 0
    else 0
)


best_payment_method = (
    payment_method_revenue.idxmax()
    if len(payment_method_revenue) > 0
    else "N/A"
)

best_payment_revenue = (
    payment_method_revenue.max()
    if len(payment_method_revenue) > 0
    else 0
)


best_month = (
    monthly_revenue.idxmax()
    if len(monthly_revenue) > 0
    else "N/A"
)

best_month_revenue = (
    monthly_revenue.max()
    if len(monthly_revenue) > 0
    else 0
)


# ============================================================
# 35. FINAL BUSINESS DASHBOARD
# ============================================================

print("\n")
print("=" * 70)
print("                 FINAL BUSINESS DASHBOARD")
print("=" * 70)


print("\nCUSTOMER KPIs")
print("-" * 70)

print("Total Customers:", total_customers)
print("Active Customers:", active_customers)
print("Inactive Customers:", inactive_customers)


print("\nADDRESS KPIs")
print("-" * 70)

print("Total Addresses:", total_addresses)
print("Unique Cities:", unique_cities)
print("Most Common City:", most_common_city)
print("Most Common State:", most_common_state)
print("Most Common Country:", most_common_country)


print("\nPRODUCT KPIs")
print("-" * 70)

print("Total Products:", total_products)


print("\nINVENTORY KPIs")
print("-" * 70)

print("Total Stock:", int(total_stock))
print("Average Stock:", round(average_stock, 2))
print("Low Stock Products:", len(low_stock))
print("Out of Stock Products:", len(out_of_stock))
print("Products Requiring Reorder:", len(reorder_required))


print("\nSALES KPIs")
print("-" * 70)

print("Total Orders:", total_orders)
print("Total Quantity Sold:", int(total_quantity))
print("Total Revenue:", round(total_revenue, 2))
print("Average Order Value:", round(average_order_value, 2))


print("\nPAYMENT KPIs")
print("-" * 70)

print("Total Payments:", total_payments)
print("Total Payment Amount:", round(total_payment_amount, 2))
print("Average Payment:", round(average_payment, 2))


print("\nREVIEW KPIs")
print("-" * 70)

print("Total Reviews:", total_reviews)
print("Average Rating:", round(average_rating, 2))
print("Most Common Rating:", most_common_rating)


print("\nSHIPMENT KPIs")
print("-" * 70)

print("Total Shipments:", total_shipments)
print("Delivered Shipments:", delivered_shipments)
print("Pending Shipments:", pending_shipments)
print("Most Used Courier:", most_used_courier)

print(
    "Average Delivery Time:",
    round(average_delivery_time, 2),
    "days"
)

print("Best Courier:", best_courier)

print(
    "Best Courier Average:",
    round(best_courier_average, 2),
    "days"
)


print("\nSUPPLIER KPIs")
print("-" * 70)

print("Total Suppliers:", total_suppliers)

print(
    "Highest Average Price Supplier:",
    highest_price_supplier
)

print(
    "Highest Average Selling Price:",
    round(highest_average_price, 2)
)

print(
    "Highest Inventory Supplier:",
    highest_inventory_supplier
)

print(
    "Highest Supplier Inventory:",
    int(highest_supplier_inventory)
)


print("\nEMPLOYEE KPIs")
print("-" * 70)

print("Total Employees:", total_employees)


# ============================================================
# BEST PERFORMERS
# ============================================================

print("\nBEST PERFORMERS")
print("-" * 70)


# Revenue performers

print("Best Product:", best_product_name)

print(
    "Best Product Revenue:",
    round(best_product_revenue, 2)
)


print("Best Category:", best_category)

print(
    "Best Category Revenue:",
    round(best_category_revenue, 2)
)


print("Top Customer:", best_customer_name)

print(
    "Top Customer Revenue:",
    round(best_customer_revenue, 2)
)


print(
    "Best Payment Method:",
    best_payment_method
)

print(
    "Best Payment Method Revenue:",
    round(best_payment_revenue, 2)
)


print("Best Revenue Month:", best_month)

print(
    "Best Month Revenue:",
    round(best_month_revenue, 2)
)


# ============================================================
# NEW PROFIT PERFORMERS
# ============================================================

print("\nPROFIT PERFORMERS")
print("-" * 70)


print(
    "Best Profit Product:",
    best_profit_product[1]
)


print(
    "Best Profit:",
    round(
        best_profit_value,
        2
    )
)


print(
    "Best Profit Category:",
    best_profit_category
)


print(
    "Best Category Profit:",
    round(
        best_category_profit,
        2
    )
)


print(
    "Best Profit Margin Product:",
    best_margin_product[1]
)


print(
    "Best Profit Margin:",
    round(
        best_margin_value,
        2
    ),
    "%"
)


# ============================================================
# PROFIT KPIs
# ============================================================

print("\nPROFIT KPIs")
print("-" * 70)

print(
    "Total Business Profit:",
    round(total_profit, 2)
)

print(
    "Average Profit per Unit:",
    round(
        average_profit_per_unit,
        2
    )
)

print(
    "Average Profit Margin:",
    round(
        average_profit_margin,
        2
    ),
    "%"
)


# ============================================================
# TOP PROFITABLE PRODUCTS
# ============================================================

print("\n")
print("=" * 70)
print("TOP 10 MOST PROFITABLE PRODUCTS")
print("=" * 70)

print(top_profit_products)


# ============================================================
# PROFIT BY CATEGORY
# ============================================================

print("\n")
print("=" * 70)
print("PROFIT BY CATEGORY")
print("=" * 70)

print(profit_by_category)


# ============================================================
# TOP PROFIT MARGIN PRODUCTS
# ============================================================

print("\n")
print("=" * 70)
print("TOP 10 PRODUCTS BY PROFIT MARGIN")
print("=" * 70)

print(top_margin_products)


# ============================================================
# GRAPH ANALYSIS
# ============================================================

print("\n")
print("=" * 70)
print("                    GRAPH ANALYSIS")
print("=" * 70)


# ============================================================
# GRAPH 1
# ACTIVE VS INACTIVE CUSTOMERS
# ============================================================

plt.figure(figsize=(7, 6))

customer_status = (
    customers["IsActive"]
    .map({
        True: "Active",
        False: "Inactive"
    })
    .value_counts()
)

customer_status.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90,
    colors=["pink", "skyblue"]
)

plt.title("Active vs Inactive Customers")
plt.ylabel("")
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 2
# ADDRESSES BY CITY
# ============================================================

plt.figure(figsize=(10, 6))

city_counts.plot(
    kind="bar",
    color="deeppink"
)

plt.title("Addresses by City")
plt.xlabel("City")
plt.ylabel("Number of Addresses")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 3
# ADDRESSES BY STATE
# ============================================================

plt.figure(figsize=(10, 6))

state_counts.plot(
    kind="bar",
    color="skyblue"
)

plt.title("Addresses by State")
plt.xlabel("State")
plt.ylabel("Number of Addresses")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 4
# PRODUCTS BY CATEGORY
# ============================================================

products_by_category = (
    products["CategoryName"]
    .value_counts()
)

plt.figure(figsize=(10, 6))

products_by_category.plot(
    kind="bar",
    color="gold"
)

plt.title("Products by Category")
plt.xlabel("Category")
plt.ylabel("Number of Products")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 5
# PRODUCT PRICE DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

products["SellingPrice"].plot(
    kind="hist",
    bins=20,
    color="orchid"
)

plt.title("Product Selling Price Distribution")
plt.xlabel("Selling Price")
plt.ylabel("Number of Products")
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 6
# TOP 10 PRODUCTS BY REVENUE
# ============================================================

plt.figure(figsize=(10, 6))

top_products_df.set_index(
    "ProductName"
)["Revenue"].plot(
    kind="bar",
    color="royalblue"
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 7
# REVENUE BY CATEGORY
# ============================================================

plt.figure(figsize=(10, 6))

category_revenue.plot(
    kind="bar",
    color="tomato"
)

plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 8
# TOP 10 CUSTOMERS
# ============================================================

plt.figure(figsize=(10, 6))

top_customers.set_index(
    "CustomerName"
)["Revenue"].plot(
    kind="bar",
    color="brown"
)

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Customer")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 9
# ORDER STATUS
# ============================================================

order_status = orders["Status"].value_counts()

plt.figure(figsize=(9, 6))

order_status.plot(
    kind="bar",
    color="gray"
)

plt.title("Orders by Status")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 10
# MONTHLY REVENUE
# ============================================================

plt.figure(figsize=(12, 6))

monthly_revenue_plot = monthly_revenue.copy()

monthly_revenue_plot.index = (
    monthly_revenue_plot.index.astype(str)
)

monthly_revenue_plot.plot(
    kind="line",
    marker="o",
    color="green"
)

plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 11
# PAYMENT METHOD REVENUE
# ============================================================

plt.figure(figsize=(10, 6))

payment_method_revenue.plot(
    kind="bar",
    color="teal"
)

plt.title("Revenue by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Payment Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 12
# PAYMENT METHOD PIE
# ============================================================

plt.figure(figsize=(8, 8))

payment_method_revenue.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90,
    colors=[
        "pink",
        "skyblue",
        "orange",
        "violet",
        "lightgreen",
        "gold"
    ]
)

plt.title("Payment Method Distribution")
plt.ylabel("")
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 13
# RATING DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

rating_counts.plot(
    kind="bar",
    color="crimson"
)

plt.title("Customer Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 14
# INVENTORY STOCK DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

inventory["QuantityInStock"].plot(
    kind="hist",
    bins=15,
    color="magenta"
)

plt.title("Inventory Stock Distribution")
plt.xlabel("Quantity in Stock")
plt.ylabel("Number of Products")
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 15
# TOP 10 PRODUCTS BY INVENTORY
# ============================================================

inventory_products = inventory.merge(
    products[
        [
            "ProductID",
            "ProductName"
        ]
    ],
    on="ProductID",
    how="left"
)

top_inventory = (
    inventory_products
    .sort_values(
        "QuantityInStock",
        ascending=False
    )
    .head(10)
)

plt.figure(figsize=(10, 6))

top_inventory.set_index(
    "ProductName"
)["QuantityInStock"].plot(
    kind="bar",
    color="darkorange"
)

plt.title("Top 10 Products by Inventory")
plt.xlabel("Product")
plt.ylabel("Quantity in Stock")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 16
# STOCK STATUS
# ============================================================

plt.figure(figsize=(8, 7))

stock_status.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90,
    colors=[
        "limegreen",
        "gold",
        "red"
    ]
)

plt.title("Inventory Stock Status")
plt.ylabel("")
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 17
# SHIPMENTS BY COURIER
# ============================================================

plt.figure(figsize=(10, 6))

courier_counts.plot(
    kind="bar",
    color="slateblue"
)

plt.title("Shipments by Courier")
plt.xlabel("Courier")
plt.ylabel("Number of Shipments")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 18
# DELIVERY TIME BY COURIER
# ============================================================

if len(average_delivery_by_courier) > 0:

    plt.figure(figsize=(10, 6))

    average_delivery_by_courier.plot(
        kind="bar",
        color="salmon"
    )

    plt.title(
        "Average Delivery Time by Courier"
    )

    plt.xlabel("Courier")
    plt.ylabel("Average Delivery Days")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# ============================================================
# GRAPH 19
# SUPPLIER INVENTORY
# ============================================================

plt.figure(figsize=(12, 6))

supplier_stock.plot(
    kind="bar",
    color="indigo"
)

plt.title("Inventory by Supplier")
plt.xlabel("Supplier")
plt.ylabel("Total Inventory")
plt.xticks(rotation=75)
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 20
# SUPPLIER AVERAGE SELLING PRICE
# ============================================================

plt.figure(figsize=(12, 6))

average_supplier_price.plot(
    kind="bar",
    color="olive"
)

plt.title(
    "Average Selling Price by Supplier"
)

plt.xlabel("Supplier")
plt.ylabel("Average Selling Price")
plt.xticks(rotation=75)
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 21
# EMPLOYEES
# ============================================================

employee_names = (
    employees["FirstName"].fillna("").astype(str)
    + " "
    + employees["LastName"].fillna("").astype(str)
).str.strip()

employee_counts = employee_names.value_counts()

plt.figure(figsize=(10, 6))

employee_counts.plot(
    kind="bar",
    color="skyblue"
)

plt.title("Employees")
plt.xlabel("Employee")
plt.ylabel("Number of Employees")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 22
# PAYMENT AMOUNT DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

payments["Amount"].plot(
    kind="hist",
    bins=20,
    color="navy"
)

plt.title("Payment Amount Distribution")
plt.xlabel("Payment Amount")
plt.ylabel("Number of Payments")
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 23
# SELLING PRICE VS INVENTORY
# ============================================================

price_inventory = products[
    [
        "ProductID",
        "SellingPrice"
    ]
].merge(
    inventory[
        [
            "ProductID",
            "QuantityInStock"
        ]
    ],
    on="ProductID",
    how="inner"
)

plt.figure(figsize=(9, 6))

plt.scatter(
    price_inventory["SellingPrice"],
    price_inventory["QuantityInStock"],
    color="mediumvioletred"
)

plt.title(
    "Selling Price vs Inventory"
)

plt.xlabel("Selling Price")
plt.ylabel("Quantity in Stock")
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 24
# QUANTITY SOLD VS REVENUE
# ============================================================

product_sales = (
    sales_data
    .groupby("ProductName")
    .agg(
        Quantity=("Quantity", "sum"),
        Revenue=("Revenue", "sum")
    )
)

plt.figure(figsize=(9, 6))

plt.scatter(
    product_sales["Quantity"],
    product_sales["Revenue"],
    color="darkcyan"
)

plt.title(
    "Quantity Sold vs Revenue"
)

plt.xlabel("Quantity Sold")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 25
# TOP PRODUCTS BY QUANTITY SOLD
# ============================================================

top_quantity = (
    sales_data
    .groupby("ProductName")["Quantity"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
)

plt.figure(figsize=(10, 6))

top_quantity.plot(
    kind="bar",
    color="hotpink"
)

plt.title(
    "Top 10 Products by Quantity Sold"
)

plt.xlabel("Product")
plt.ylabel("Quantity Sold")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 26
# CATEGORY REVENUE PIE
# ============================================================

plt.figure(figsize=(9, 9))

category_revenue.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90,
    colors=[
        "pink",
        "skyblue",
        "gold",
        "violet",
        "orange",
        "lightgreen",
        "cyan",
        "salmon"
    ]
)

plt.title(
    "Revenue Share by Category"
)

plt.ylabel("")
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 27
# TOP PRODUCTS BY REVIEWS
# ============================================================

reviews_by_product = (
    reviews
    .merge(
        products[
            [
                "ProductID",
                "ProductName"
            ]
        ],
        on="ProductID",
        how="left"
    )
    .groupby("ProductName")
    .size()
    .sort_values(
        ascending=False
    )
    .head(10)
)

plt.figure(figsize=(10, 6))

reviews_by_product.plot(
    kind="bar",
    color="darkviolet"
)

plt.title(
    "Top 10 Products by Number of Reviews"
)

plt.xlabel("Product")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# GRAPH 28
# REVIEW RATING PIE
# ============================================================

plt.figure(figsize=(8, 8))

rating_counts.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90,
    colors=[
        "red",
        "orange",
        "yellow",
        "lightgreen",
        "deepskyblue"
    ]
)

plt.title(
    "Review Rating Distribution"
)

plt.ylabel("")
plt.tight_layout()
plt.show()



# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n")
print("=" * 70)
print("             ALL 29 GRAPHS GENERATED SUCCESSFULLY")
print("=" * 70)


# ============================================================
# 40. ADVANCED CUSTOMER ANALYSIS
# ============================================================

print("\n")
print("=" * 70)
print("                 ADVANCED CUSTOMER ANALYSIS")
print("=" * 70)


# ============================================================
# 1. CUSTOMER ORDER ANALYSIS
# ============================================================

customer_analysis = (
    sales_data
    .groupby(
        ["CustomerID", "CustomerName"]
    )
    .agg(
        TotalOrders=("OrderID", "nunique"),
        TotalQuantity=("Quantity", "sum"),
        TotalSpending=("Revenue", "sum")
    )
    .reset_index()
)


# ============================================================
# 2. AVERAGE ORDER VALUE
# ============================================================

customer_analysis["AverageOrderValue"] = np.where(
    customer_analysis["TotalOrders"] > 0,
    customer_analysis["TotalSpending"]
    / customer_analysis["TotalOrders"],
    0
)


# ============================================================
# 3. TOTAL CUSTOMERS WITH ORDERS
# ============================================================

customers_with_orders = (
    customer_analysis["CustomerID"]
    .nunique()
)


# ============================================================
# 4. CUSTOMERS WITHOUT ORDERS
# ============================================================

customers_without_orders = (
    total_customers
    - customers_with_orders
)


# ============================================================
# 5. REPEAT CUSTOMERS
# ============================================================

repeat_customers = (
    customer_analysis[
        customer_analysis["TotalOrders"] > 1
    ]
)


# ============================================================
# 6. TOP CUSTOMERS BY SPENDING
# ============================================================

top_spending_customers = (
    customer_analysis
    .sort_values(
        "TotalSpending",
        ascending=False
    )
    .head(10)
)


# ============================================================
# 7. TOP CUSTOMERS BY ORDERS
# ============================================================

top_order_customers = (
    customer_analysis
    .sort_values(
        "TotalOrders",
        ascending=False
    )
    .head(10)
)


# ============================================================
# 8. TOP CUSTOMERS BY QUANTITY
# ============================================================

top_quantity_customers = (
    customer_analysis
    .sort_values(
        "TotalQuantity",
        ascending=False
    )
    .head(10)
)


# ============================================================
# 9. CUSTOMER SEGMENTATION
# ============================================================

def customer_segment(spending):

    if spending >= 10000:
        return "VIP"

    elif spending >= 5000:
        return "High Value"

    elif spending >= 2000:
        return "Regular"

    else:
        return "Low Value"


customer_analysis["CustomerSegment"] = (
    customer_analysis["TotalSpending"]
    .apply(customer_segment)
)


# ============================================================
# 10. CUSTOMER SEGMENT COUNTS
# ============================================================

customer_segments = (
    customer_analysis["CustomerSegment"]
    .value_counts()
)


# ============================================================
# 11. CUSTOMER ANALYSIS OUTPUT
# ============================================================

print("\nCUSTOMER ANALYSIS KPIs")
print("-" * 70)

print(
    "Total Customers:",
    total_customers
)

print(
    "Customers With Orders:",
    customers_with_orders
)

print(
    "Customers Without Orders:",
    customers_without_orders
)

print(
    "Repeat Customers:",
    len(repeat_customers)
)


# ============================================================
# 12. TOP 10 SPENDING CUSTOMERS
# ============================================================

print("\n")
print("=" * 70)
print("TOP 10 CUSTOMERS BY SPENDING")
print("=" * 70)

print(
    top_spending_customers[
        [
            "CustomerName",
            "TotalOrders",
            "TotalQuantity",
            "TotalSpending",
            "AverageOrderValue"
        ]
    ]
)


# ============================================================
# 13. TOP 10 ORDER CUSTOMERS
# ============================================================

print("\n")
print("=" * 70)
print("TOP 10 CUSTOMERS BY NUMBER OF ORDERS")
print("=" * 70)

print(
    top_order_customers[
        [
            "CustomerName",
            "TotalOrders",
            "TotalSpending"
        ]
    ]
)


# ============================================================
# 14. TOP 10 QUANTITY CUSTOMERS
# ============================================================

print("\n")
print("=" * 70)
print("TOP 10 CUSTOMERS BY QUANTITY PURCHASED")
print("=" * 70)

print(
    top_quantity_customers[
        [
            "CustomerName",
            "TotalQuantity",
            "TotalSpending"
        ]
    ]
)


# ============================================================
# 15. CUSTOMER SEGMENTS
# ============================================================

print("\n")
print("=" * 70)
print("CUSTOMER SEGMENTATION")
print("=" * 70)

print(customer_segments)


# ============================================================
# 16. BEST CUSTOMER
# ============================================================

if len(customer_analysis) > 0:

    best_customer = customer_analysis.iloc[
        customer_analysis["TotalSpending"].idxmax()
    ]

    print("\nBEST CUSTOMER")
    print("-" * 70)

    print(
        "Customer:",
        best_customer["CustomerName"]
    )

    print(
        "Orders:",
        int(best_customer["TotalOrders"])
    )

    print(
        "Quantity Purchased:",
        int(best_customer["TotalQuantity"])
    )

    print(
        "Total Spending:",
        round(
            best_customer["TotalSpending"],
            2
        )
    )

    print(
        "Average Order Value:",
        round(
            best_customer["AverageOrderValue"],
            2
        )
    )

    print(
        "Customer Segment:",
        best_customer["CustomerSegment"]
    )


# ============================================================
# 17. CUSTOMER INSIGHTS
# ============================================================

print("\n")
print("=" * 70)
print("CUSTOMER BUSINESS INSIGHTS")
print("=" * 70)


if len(repeat_customers) > 0:

    print(
        "\nRepeat customers are present."
    )

    print(
        "These customers should be targeted"
        " with loyalty campaigns."
    )

else:

    print(
        "\nNo repeat customers were identified."
    )


if customers_without_orders > 0:

    print(
        "\nSome customers have never placed an order."
    )

    print(
        "Consider promotional campaigns"
        " to convert them."
    )

else:

    print(
        "\nAll customers have placed at least one order."
    )


if "VIP" in customer_segments.index:

    print(
        "\nVIP customers detected:",
        int(customer_segments["VIP"])
    )

    print(
        "VIP customers should receive"
        " personalized offers."
    )


print("\n")
print("=" * 70)
print("          ADVANCED CUSTOMER ANALYSIS COMPLETED")
print("=" * 70)


# ============================================================
# GRAPH 29
# CUSTOMER SEGMENTATION
# ============================================================

plt.figure(figsize=(9, 6))

customer_segments.plot(
    kind="bar"
)

plt.title("Customer Segmentation")

plt.xlabel("Customer Segment")

plt.ylabel("Number of Customers")

plt.xticks(rotation=0)

plt.tight_layout()

plt.show()


# ============================================================
# 35. AUTOMATED BUSINESS INSIGHTS
# ============================================================

print("\n")
print("=" * 70)
print("                 AUTOMATED BUSINESS INSIGHTS")
print("=" * 70)


# ------------------------------------------------------------
# 1. BEST REVENUE PRODUCT
# ------------------------------------------------------------

print("\n1. BEST REVENUE PRODUCT")
print("-" * 70)

print(
    "Product:",
    best_product_name
)

print(
    "Revenue:",
    round(best_product_revenue, 2)
)


# ------------------------------------------------------------
# 2. BEST PROFIT PRODUCT
# ------------------------------------------------------------

print("\n2. BEST PROFIT PRODUCT")
print("-" * 70)

print(
    "Product:",
    best_profit_product[1]
)

print(
    "Profit:",
    round(best_profit_value, 2)
)


# ------------------------------------------------------------
# 3. BEST PROFIT MARGIN PRODUCT
# ------------------------------------------------------------

print("\n3. BEST PROFIT MARGIN PRODUCT")
print("-" * 70)

print(
    "Product:",
    best_margin_product[1]
)

print(
    "Profit Margin:",
    round(best_margin_value, 2),
    "%"
)


# ------------------------------------------------------------
# 4. BEST REVENUE CATEGORY
# ------------------------------------------------------------

print("\n4. BEST REVENUE CATEGORY")
print("-" * 70)

print(
    "Category:",
    best_category
)

print(
    "Revenue:",
    round(best_category_revenue, 2)
)


# ------------------------------------------------------------
# 5. BEST PROFIT CATEGORY
# ------------------------------------------------------------

print("\n5. BEST PROFIT CATEGORY")
print("-" * 70)

print(
    "Category:",
    best_profit_category
)

print(
    "Profit:",
    round(best_category_profit, 2)
)


# ------------------------------------------------------------
# 6. TOP CUSTOMER
# ------------------------------------------------------------

print("\n6. TOP CUSTOMER")
print("-" * 70)

print(
    "Customer:",
    best_customer_name
)

print(
    "Revenue:",
    round(best_customer_revenue, 2)
)


# ------------------------------------------------------------
# 7. BEST PAYMENT METHOD
# ------------------------------------------------------------

print("\n7. BEST PAYMENT METHOD")
print("-" * 70)

print(
    "Payment Method:",
    best_payment_method
)

print(
    "Payment Revenue:",
    round(best_payment_revenue, 2)
)


# ------------------------------------------------------------
# 8. BEST REVENUE MONTH
# ------------------------------------------------------------

print("\n8. BEST REVENUE MONTH")
print("-" * 70)

print(
    "Month:",
    best_month
)

print(
    "Revenue:",
    round(best_month_revenue, 2)
)


# ------------------------------------------------------------
# 9. INVENTORY ALERT
# ------------------------------------------------------------

print("\n9. INVENTORY ALERT")
print("-" * 70)

print(
    "Low Stock Products:",
    len(low_stock)
)

print(
    "Out of Stock Products:",
    len(out_of_stock)
)

print(
    "Products Requiring Reorder:",
    len(reorder_required)
)


# ------------------------------------------------------------
# 10. DELIVERY PERFORMANCE
# ------------------------------------------------------------

print("\n10. DELIVERY PERFORMANCE")
print("-" * 70)

print(
    "Best Courier:",
    best_courier
)

print(
    "Average Delivery Time:",
    round(
        best_courier_average,
        2
    ),
    "days"
)


# ------------------------------------------------------------
# 11. CUSTOMER SATISFACTION
# ------------------------------------------------------------

print("\n11. CUSTOMER SATISFACTION")
print("-" * 70)

print(
    "Average Rating:",
    round(
        average_rating,
        2
    )
)

print(
    "Most Common Rating:",
    most_common_rating
)


# ------------------------------------------------------------
# 12. OVERALL BUSINESS PERFORMANCE
# ------------------------------------------------------------

print("\n12. OVERALL BUSINESS PERFORMANCE")
print("-" * 70)

print(
    "Total Revenue:",
    round(
        total_revenue,
        2
    )
)

print(
    "Total Profit:",
    round(
        total_profit,
        2
    )
)

print(
    "Average Profit Margin:",
    round(
        average_profit_margin,
        2
    ),
    "%"
)

print(
    "Total Orders:",
    total_orders
)

print(
    "Average Order Value:",
    round(
        average_order_value,
        2
    )
)


print("\n")
print("=" * 70)
print("          AUTOMATED INSIGHTS COMPLETED")
print("=" * 70)

# ============================================================
# 36. EXPORT ANALYSIS TO EXCEL
# ============================================================

print("\n")
print("=" * 70)
print("              EXPORTING ANALYSIS TO EXCEL")
print("=" * 70)

excel_file = "Retail_ECommerce_Final_Analysis.xlsx"

with pd.ExcelWriter(
    excel_file,
    engine="openpyxl"
) as writer:

    # --------------------------------------------------------
    # RAW DATA TABLES
    # --------------------------------------------------------

    customers.to_excel(
        writer,
        sheet_name="Customers",
        index=False
    )

    orders.to_excel(
        writer,
        sheet_name="Orders",
        index=False
    )

    items.to_excel(
        writer,
        sheet_name="Order Items",
        index=False
    )

    products.to_excel(
        writer,
        sheet_name="Products",
        index=False
    )

    payments.to_excel(
        writer,
        sheet_name="Payments",
        index=False
    )

    reviews.to_excel(
        writer,
        sheet_name="Reviews",
        index=False
    )

    addresses.to_excel(
        writer,
        sheet_name="Addresses",
        index=False
    )

    shipments.to_excel(
        writer,
        sheet_name="Shipments",
        index=False
    )

    suppliers.to_excel(
        writer,
        sheet_name="Suppliers",
        index=False
    )

    inventory.to_excel(
        writer,
        sheet_name="Inventory",
        index=False
    )

    employees.to_excel(
        writer,
        sheet_name="Employees",
        index=False
    )

    # --------------------------------------------------------
    # BUSINESS ANALYSIS
    # --------------------------------------------------------

    top_products_df.to_excel(
        writer,
        sheet_name="Top Products",
        index=False
    )

    category_revenue.to_frame(
        "Revenue"
    ).to_excel(
        writer,
        sheet_name="Category Revenue"
    )

    top_customers.to_excel(
        writer,
        sheet_name="Top Customers",
        index=False
    )

    monthly_revenue.to_frame(
        "Revenue"
    ).to_excel(
        writer,
        sheet_name="Monthly Revenue"
    )

    payment_method_revenue.to_frame(
        "Payment Amount"
    ).to_excel(
        writer,
        sheet_name="Payment Methods"
    )

    product_ratings.to_frame(
        "Average Rating"
    ).to_excel(
        writer,
        sheet_name="Product Ratings"
    )

    stock_status.to_frame(
        "Products"
    ).to_excel(
        writer,
        sheet_name="Stock Status"
    )

    profit_by_category.to_frame(
        "Total Profit"
    ).to_excel(
        writer,
        sheet_name="Profit Category"
    )

    top_profit_products.to_excel(
        writer,
        sheet_name="Top Profit Products",
        index=False
    )

    top_margin_products.to_excel(
        writer,
        sheet_name="Top Profit Margin",
        index=False
    )

    supplier_stock.to_frame(
        "Inventory"
    ).to_excel(
        writer,
        sheet_name="Supplier Inventory"
    )

    average_supplier_price.to_frame(
        "Average Price"
    ).to_excel(
        writer,
        sheet_name="Supplier Prices"
    )


print("\nExcel file created successfully!")

print(
    "File:",
    excel_file
)



connection.close()

print("\nDatabase connection closed.")

print(
    "FINAL ANALYSIS COMPLETED SUCCESSFULLY!"
)

# ============================================================
# 39. AUTOMATED BUSINESS INSIGHTS
# ============================================================

print("\n")
print("=" * 70)
print("                 AUTOMATED BUSINESS INSIGHTS")
print("=" * 70)


# ------------------------------------------------------------
# 1. BEST REVENUE PRODUCT
# ------------------------------------------------------------

print("\n1. BEST REVENUE PRODUCT")
print("-" * 70)

print(
    "Product:",
    best_product_name
)

print(
    "Revenue:",
    round(best_product_revenue, 2)
)


# ------------------------------------------------------------
# 2. BEST PROFIT PRODUCT
# ------------------------------------------------------------

print("\n2. BEST PROFIT PRODUCT")
print("-" * 70)

print(
    "Product:",
    best_profit_product[1]
)

print(
    "Profit:",
    round(best_profit_value, 2)
)


# ------------------------------------------------------------
# 3. BEST PROFIT CATEGORY
# ------------------------------------------------------------

print("\n3. BEST PROFIT CATEGORY")
print("-" * 70)

print(
    "Category:",
    best_profit_category
)

print(
    "Profit:",
    round(best_category_profit, 2)
)


# ------------------------------------------------------------
# 4. BEST PROFIT MARGIN PRODUCT
# ------------------------------------------------------------

print("\n4. BEST PROFIT MARGIN PRODUCT")
print("-" * 70)

print(
    "Product:",
    best_margin_product[1]
)

print(
    "Profit Margin:",
    round(best_margin_value, 2),
    "%"
)


# ------------------------------------------------------------
# 5. BEST CUSTOMER
# ------------------------------------------------------------

print("\n5. TOP CUSTOMER")
print("-" * 70)

print(
    "Customer:",
    best_customer_name
)

print(
    "Revenue:",
    round(best_customer_revenue, 2)
)


# ------------------------------------------------------------
# 6. BEST PAYMENT METHOD
# ------------------------------------------------------------

print("\n6. BEST PAYMENT METHOD")
print("-" * 70)

print(
    "Payment Method:",
    best_payment_method
)

print(
    "Payment Revenue:",
    round(best_payment_revenue, 2)
)


# ------------------------------------------------------------
# 7. BEST REVENUE MONTH
# ------------------------------------------------------------

print("\n7. BEST REVENUE MONTH")
print("-" * 70)

print(
    "Month:",
    best_month
)

print(
    "Revenue:",
    round(best_month_revenue, 2)
)


# ------------------------------------------------------------
# 8. INVENTORY WARNING
# ------------------------------------------------------------

print("\n8. INVENTORY ANALYSIS")
print("-" * 70)

print(
    "Low Stock Products:",
    len(low_stock)
)

print(
    "Out of Stock Products:",
    len(out_of_stock)
)

print(
    "Products Requiring Reorder:",
    len(reorder_required)
)


if len(out_of_stock) > 0:

    print(
        "WARNING: Some products are out of stock."
    )

else:

    print(
        "No products are currently out of stock."
    )


# ------------------------------------------------------------
# 9. SHIPPING ANALYSIS
# ------------------------------------------------------------

print("\n9. SHIPPING ANALYSIS")
print("-" * 70)

print(
    "Total Shipments:",
    total_shipments
)

print(
    "Delivered Shipments:",
    delivered_shipments
)

print(
    "Pending Shipments:",
    pending_shipments
)

print(
    "Best Courier:",
    best_courier
)

print(
    "Average Delivery Time:",
    round(
        average_delivery_time,
        2
    ),
    "days"
)


# ------------------------------------------------------------
# 10. CUSTOMER ACTIVITY
# ------------------------------------------------------------

print("\n10. CUSTOMER ACTIVITY")
print("-" * 70)

print(
    "Total Customers:",
    total_customers
)

print(
    "Active Customers:",
    active_customers
)

print(
    "Inactive Customers:",
    inactive_customers
)


# ------------------------------------------------------------
# 11. PRODUCT PERFORMANCE
# ------------------------------------------------------------

print("\n11. PRODUCT PERFORMANCE")
print("-" * 70)

print(
    "Total Products:",
    total_products
)

print(
    "Best Revenue Product:",
    best_product_name
)

print(
    "Best Profit Product:",
    best_profit_product[1]
)

print(
    "Best Margin Product:",
    best_margin_product[1]
)


# ------------------------------------------------------------
# 12. BUSINESS RECOMMENDATIONS
# ------------------------------------------------------------

print("\n")
print("=" * 70)
print("                 BUSINESS RECOMMENDATIONS")
print("=" * 70)


print("\nRecommendation 1:")
print(
    "Focus marketing on the highest revenue products."
)


print("\nRecommendation 2:")
print(
    "Increase stock for products requiring reorder."
)


print("\nRecommendation 3:")
print(
    "Promote products with high profit margins."
)


print("\nRecommendation 4:")
print(
    "Study the behavior of top customers and create"
    " loyalty offers for them."
)


print("\nRecommendation 5:")
print(
    "Monitor pending shipments and improve delivery"
    " performance where necessary."
)


print("\nRecommendation 6:")
print(
    "Focus on categories generating the highest profit."
)


print("\nRecommendation 7:")
print(
    "Compare revenue and profit before deciding which"
    " products should receive additional marketing."
)


print("\n")
print("=" * 70)
print("             BUSINESS INSIGHTS COMPLETED")
print("=" * 70)