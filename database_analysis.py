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