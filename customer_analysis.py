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
# 2. LOAD CUSTOMERS
# =======================================

customers_query = """
SELECT
    CustomerID,
    FirstName,
    LastName,
    Email,
    Phone,
    DateJoined,
    IsActive,
    CreatedDate
FROM Sales.Customers
"""

customers = pd.read_sql(
    customers_query,
    connection
)


# =======================================
# 3. DISPLAY CUSTOMER DATA
# =======================================

print("\n======================================")
print("CUSTOMERS DATA")
print("======================================")

print(customers.head())


# =======================================
# 4. CUSTOMER SHAPE
# =======================================

print("\n======================================")
print("CUSTOMER SHAPE")
print("======================================")

print(customers.shape)


# =======================================
# 5. CUSTOMER COLUMNS
# =======================================

print("\n======================================")
print("CUSTOMER COLUMNS")
print("======================================")

print(customers.columns.tolist())


# =======================================
# 6. CUSTOMER INFORMATION
# =======================================

print("\n======================================")
print("CUSTOMER INFORMATION")
print("======================================")

customers.info()


# =======================================
# 7. MISSING VALUES
# =======================================

print("\n======================================")
print("MISSING VALUES")
print("======================================")

print(customers.isnull().sum())


# =======================================
# 8. CONVERT DATE COLUMNS
# =======================================

customers["DateJoined"] = pd.to_datetime(
    customers["DateJoined"],
    errors="coerce"
)

customers["CreatedDate"] = pd.to_datetime(
    customers["CreatedDate"],
    errors="coerce"
)


# =======================================
# 9. CREATE CUSTOMER NAME
# =======================================

customers["CustomerName"] = (
    customers["FirstName"]
    + " "
    + customers["LastName"]
)


# =======================================
# 10. TOTAL CUSTOMERS
# =======================================

total_customers = customers["CustomerID"].nunique()

print("\n======================================")
print("TOTAL CUSTOMERS")
print("======================================")

print(total_customers)


# =======================================
# 11. ACTIVE / INACTIVE CUSTOMERS
# =======================================

customer_status = (
    customers["IsActive"]
    .value_counts()
)


print("\n======================================")
print("ACTIVE / INACTIVE CUSTOMERS")
print("======================================")

print(customer_status)


# =======================================
# 12. ACTIVE CUSTOMERS
# =======================================

active_customers = (
    customers["IsActive"] == True
).sum()


print("\n======================================")
print("ACTIVE CUSTOMERS")
print("======================================")

print(active_customers)


# =======================================
# 13. INACTIVE CUSTOMERS
# =======================================

inactive_customers = (
    customers["IsActive"] == False
).sum()


print("\n======================================")
print("INACTIVE CUSTOMERS")
print("======================================")

print(inactive_customers)


# =======================================
# 14. CUSTOMER PERCENTAGES
# =======================================

active_percentage = (
    active_customers / total_customers
) * 100

inactive_percentage = (
    inactive_customers / total_customers
) * 100


print("\n======================================")
print("CUSTOMER STATUS PERCENTAGE")
print("======================================")

print(
    "Active Customers:",
    round(active_percentage, 2),
    "%"
)

print(
    "Inactive Customers:",
    round(inactive_percentage, 2),
    "%"
)


# =======================================
# 15. FIRST JOINING DATE
# =======================================

first_joining_date = (
    customers["DateJoined"].min()
)


print("\n======================================")
print("FIRST JOINING DATE")
print("======================================")

print(first_joining_date)


# =======================================
# 16. LATEST JOINING DATE
# =======================================

latest_joining_date = (
    customers["DateJoined"].max()
)


print("\n======================================")
print("LATEST JOINING DATE")
print("======================================")

print(latest_joining_date)


# =======================================
# 17. CUSTOMERS BY JOINING MONTH
# =======================================

monthly_customers = (
    customers
    .groupby(
        customers["DateJoined"].dt.to_period("M")
    )
    .size()
)


print("\n======================================")
print("CUSTOMERS BY MONTH")
print("======================================")

print(monthly_customers)


# =======================================
# 18. CUSTOMERS BY JOINING YEAR
# =======================================

yearly_customers = (
    customers
    .groupby(
        customers["DateJoined"].dt.year
    )
    .size()
)


print("\n======================================")
print("CUSTOMERS BY YEAR")
print("======================================")

print(yearly_customers)


# =======================================
# 19. MOST ACTIVE JOINING YEAR
# =======================================

best_joining_year = yearly_customers.idxmax()

best_joining_year_customers = (
    yearly_customers.max()
)


print("\n======================================")
print("BEST CUSTOMER JOINING YEAR")
print("======================================")

print("Year:", best_joining_year)
print(
    "Customers Joined:",
    best_joining_year_customers
)


# =======================================
# 20. CUSTOMER ID STATISTICS
# =======================================

print("\n======================================")
print("CUSTOMER ID STATISTICS")
print("======================================")

print(
    customers["CustomerID"].describe()
)


# =======================================
# 21. TOP 10 CUSTOMER IDS
# =======================================

top_customer_ids = (
    customers[
        [
            "CustomerID",
            "CustomerName",
            "Email",
            "DateJoined"
        ]
    ]
    .sort_values(
        "CustomerID",
        ascending=False
    )
    .head(10)
)


print("\n======================================")
print("TOP 10 CUSTOMER IDs")
print("======================================")

print(top_customer_ids)


# =======================================
# 22. CUSTOMER JOINING GRAPH
# =======================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_customers.index.astype(str),
    monthly_customers.values,
    marker="o"
)

plt.xlabel("Month")
plt.ylabel("New Customers")
plt.title("Customer Registrations Over Time")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# =======================================
# 23. ACTIVE / INACTIVE GRAPH
# =======================================

status_labels = [
    "Active",
    "Inactive"
]

status_values = [
    active_customers,
    inactive_customers
]

plt.figure(figsize=(8, 5))

plt.bar(
    status_labels,
    status_values
)

plt.xlabel("Customer Status")
plt.ylabel("Number of Customers")
plt.title("Active vs Inactive Customers")

plt.tight_layout()
plt.show()


# =======================================
# 24. YEARLY CUSTOMER GRAPH
# =======================================

plt.figure(figsize=(10, 6))

plt.bar(
    yearly_customers.index.astype(str),
    yearly_customers.values
)

plt.xlabel("Year")
plt.ylabel("New Customers")
plt.title("Customers Joined by Year")

plt.tight_layout()
plt.show()


# =======================================
# 25. FINAL CUSTOMER INSIGHTS
# =======================================

print("\n")
print("====================================================")
print("              FINAL CUSTOMER INSIGHTS")
print("====================================================")


print("\nTotal Customers:")
print(total_customers)


print("\nActive Customers:")
print(active_customers)


print("\nInactive Customers:")
print(inactive_customers)


print("\nActive Customer Percentage:")
print(round(active_percentage, 2), "%")


print("\nInactive Customer Percentage:")
print(round(inactive_percentage, 2), "%")


print("\nFirst Joining Date:")
print(first_joining_date)


print("\nLatest Joining Date:")
print(latest_joining_date)


print("\nBest Customer Joining Year:")
print(best_joining_year)


print("\nCustomers Joined in Best Year:")
print(best_joining_year_customers)


print("\nMost Recent Customer:")

most_recent_customer = customers.loc[
    customers["DateJoined"].idxmax()
]

print(
    most_recent_customer[
        [
            "CustomerID",
            "CustomerName",
            "Email",
            "DateJoined"
        ]
    ]
)


print("\nOldest Customer Record:")

oldest_customer = customers.loc[
    customers["DateJoined"].idxmin()
]

print(
    oldest_customer[
        [
            "CustomerID",
            "CustomerName",
            "Email",
            "DateJoined"
        ]
    ]
)


print("\n====================================================")
print("       CUSTOMER ANALYSIS COMPLETED SUCCESSFULLY")
print("====================================================")


# =======================================
# 26. CLOSE CONNECTION
# =======================================

connection.close()

print("\nDatabase connection closed!")