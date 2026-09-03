import pyodbc
import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# 1. DATABASE CONNECTION
# ==========================================

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=ZUBAIR\\SQLEXPRESS;"
    "DATABASE=RetailECommerceDB;"
    "Trusted_Connection=yes;"
)

print("Database connected successfully!")


# ==========================================
# 2. LOAD ADDRESSES
# ==========================================

query = """
SELECT *
FROM Sales.Addresses
"""

addresses = pd.read_sql(
    query,
    connection
)


# ==========================================
# 3. BASIC INFORMATION
# ==========================================

print("\n======================================")
print("ADDRESSES DATA")
print("======================================")

print(addresses.head())


print("\nAddresses Shape:")
print(addresses.shape)


print("\nAddresses Columns:")
print(addresses.columns.tolist())


# ==========================================
# 4. DATA INFORMATION
# ==========================================

print("\n======================================")
print("ADDRESS DATA INFORMATION")
print("======================================")

addresses.info()


# ==========================================
# 5. MISSING VALUES
# ==========================================

print("\n======================================")
print("MISSING VALUES")
print("======================================")

print(addresses.isnull().sum())


# ==========================================
# 6. TOTAL ADDRESSES
# ==========================================

total_addresses = addresses["AddressID"].nunique()

print("\n======================================")
print("TOTAL ADDRESSES")
print("======================================")

print(total_addresses)


# ==========================================
# 7. UNIQUE CITIES
# ==========================================

unique_cities = addresses["City"].nunique()

print("\n======================================")
print("UNIQUE CITIES")
print("======================================")

print(unique_cities)


# ==========================================
# 8. ADDRESSES BY CITY
# ==========================================

city_count = (
    addresses["City"]
    .value_counts()
)

print("\n======================================")
print("ADDRESSES BY CITY")
print("======================================")

print(city_count)


# ==========================================
# 9. TOP CITIES
# ==========================================

print("\n======================================")
print("TOP 10 CITIES")
print("======================================")

print(city_count.head(10))


# ==========================================
# 10. ADDRESSES BY STATE
# ==========================================

state_count = (
    addresses["StateProvince"]
    .value_counts()
)

print("\n======================================")
print("ADDRESSES BY STATE")
print("======================================")

print(state_count)


# ==========================================
# 11. ADDRESSES BY COUNTRY
# ==========================================

country_count = (
    addresses["Country"]
    .value_counts()
)

print("\n======================================")
print("ADDRESSES BY COUNTRY")
print("======================================")

print(country_count)


# ==========================================
# 12. CITY GRAPH
# ==========================================

plt.figure(figsize=(10, 6))

city_count.plot(
    kind="bar"
)

plt.title("Customers / Addresses by City")
plt.xlabel("City")
plt.ylabel("Number of Addresses")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# ==========================================
# 13. STATE GRAPH
# ==========================================

plt.figure(figsize=(10, 6))

state_count.plot(
    kind="bar"
)

plt.title("Addresses by State")
plt.xlabel("State")
plt.ylabel("Number of Addresses")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# ==========================================
# 14. COUNTRY GRAPH
# ==========================================

plt.figure(figsize=(8, 5))

country_count.plot(
    kind="bar"
)

plt.title("Addresses by Country")
plt.xlabel("Country")
plt.ylabel("Number of Addresses")

plt.xticks(rotation=0)
plt.tight_layout()

plt.show()


# ==========================================
# 15. FINAL ADDRESS INSIGHTS
# ==========================================

print("\n")
print("==============================================")
print("FINAL ADDRESS INSIGHTS")
print("==============================================")


print("\nTotal Addresses:")
print(total_addresses)


print("\nUnique Cities:")
print(unique_cities)


print("\nMost Common City:")
print(city_count.idxmax())


print("\nAddresses in Most Common City:")
print(city_count.max())


print("\nMost Common State:")
print(state_count.idxmax())


print("\nAddresses in Most Common State:")
print(state_count.max())


print("\nMost Common Country:")
print(country_count.idxmax())


print("\nAddresses in Most Common Country:")
print(country_count.max())


# ==========================================
# 16. CLOSE CONNECTION
# ==========================================

connection.close()

print("\nDatabase connection closed!")
print("\nADDRESS ANALYSIS COMPLETED SUCCESSFULLY!")