import pyodbc
import pandas as pd

# ======================================
# 1. DATABASE CONNECTION
# ======================================

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=ZUBAIR\\SQLEXPRESS;"
    "DATABASE=RetailECommerceDB;"
    "Trusted_Connection=yes;"
)

print("Database connected successfully!")


# ======================================
# 2. LOAD EMPLOYEES
# ======================================

query = """
SELECT *
FROM HR.Employees
"""

employees = pd.read_sql(
    query,
    connection
)


# ======================================
# 3. DISPLAY DATA
# ======================================

print("\n======================================")
print("EMPLOYEES DATA")
print("======================================")

print(employees.head())


# ======================================
# 4. SHAPE
# ======================================

print("\nEmployees Shape:")
print(employees.shape)


# ======================================
# 5. COLUMNS
# ======================================

print("\nEmployees Columns:")
print(employees.columns.tolist())


# ======================================
# 6. INFORMATION
# ======================================

print("\nEmployees Information:")
print(employees.info())


# ======================================
# 7. MISSING VALUES
# ======================================

print("\n======================================")
print("MISSING VALUES")
print("======================================")

print(employees.isnull().sum())


# ======================================
# 8. CLOSE CONNECTION
# ======================================

connection.close()

print("\nDatabase connection closed!")