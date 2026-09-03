import pyodbc
import pandas as pd
import matplotlib.pyplot as plt


# =====================================================
# 1. DATABASE CONNECTION
# =====================================================

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=ZUBAIR\\SQLEXPRESS;"
    "DATABASE=RetailECommerceDB;"
    "Trusted_Connection=yes;"
)

print("Database connected successfully!")


# =====================================================
# 2. LOAD PAYMENTS DATA
# =====================================================

payments_query = """
SELECT *
FROM Sales.Payments
"""

payments = pd.read_sql(
    payments_query,
    connection
)

print("\n======================================")
print("PAYMENTS DATA")
print("======================================")

print(payments.head())


# =====================================================
# 3. CHECK PAYMENTS DATA
# =====================================================

print("\nPayments Shape:")
print(payments.shape)

print("\nPayments Columns:")
print(payments.columns.tolist())

print("\nPayments Information:")
print(payments.info())


# =====================================================
# 4. CONVERT AMOUNT TO NUMERIC
# =====================================================

payments["Amount"] = pd.to_numeric(
    payments["Amount"],
    errors="coerce"
)


# =====================================================
# 5. TOTAL PAYMENT AMOUNT
# =====================================================

total_payment = payments["Amount"].sum()

print("\n======================================")
print("TOTAL PAYMENT AMOUNT")
print("======================================")

print(total_payment)


# =====================================================
# 6. NUMBER OF PAYMENTS
# =====================================================

total_payments = payments["PaymentID"].nunique()

print("\nTotal Payments:")
print(total_payments)


# =====================================================
# 7. AVERAGE PAYMENT
# =====================================================

average_payment = payments["Amount"].mean()

print("\nAverage Payment:")
print(average_payment)


# =====================================================
# 8. PAYMENT METHOD ANALYSIS
# =====================================================

payment_methods = (
    payments["PaymentMethod"]
    .value_counts()
)

print("\n======================================")
print("PAYMENTS BY METHOD")
print("======================================")

print(payment_methods)


# =====================================================
# 9. PAYMENT METHOD GRAPH
# =====================================================

plt.figure(figsize=(10, 6))

plt.bar(
    payment_methods.index,
    payment_methods.values,
     color="pink"
)

plt.xlabel("Payment Method")
plt.ylabel("Number of Payments")
plt.title("Payments by Payment Method")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# =====================================================
# 10. REVENUE BY PAYMENT METHOD
# =====================================================

revenue_by_method = (
    payments
    .groupby("PaymentMethod")["Amount"]
    .sum()
    .sort_values(
        ascending=False
    )
)

print("\n======================================")
print("REVENUE BY PAYMENT METHOD")
print("======================================")

print(revenue_by_method)


# =====================================================
# 11. REVENUE BY PAYMENT METHOD GRAPH
# =====================================================

plt.figure(figsize=(10, 6))

plt.bar(
    revenue_by_method.index,
    revenue_by_method.values,
     color="red"
)

plt.xlabel("Payment Method")
plt.ylabel("Total Amount")
plt.title("Revenue by Payment Method")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# =====================================================
# 12. PAYMENT DATE ANALYSIS
# =====================================================

payments["PaymentDate"] = pd.to_datetime(
    payments["PaymentDate"]
)

monthly_payments = (
    payments
    .groupby(
        payments["PaymentDate"].dt.to_period("M")
    )["Amount"]
    .sum()
)

print("\n======================================")
print("MONTHLY PAYMENT REVENUE")
print("======================================")

print(monthly_payments)


# =====================================================
# 13. MONTHLY PAYMENT GRAPH
# =====================================================

plt.figure(figsize=(10, 6))

plt.plot(
    monthly_payments.index.astype(str),
    monthly_payments.values,
    marker="o",
     color="brown"
)

plt.xlabel("Month")
plt.ylabel("Payment Amount")
plt.title("Monthly Payment Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# =====================================================
# 14. LARGEST PAYMENT
# =====================================================

largest_payment = payments.loc[
    payments["Amount"].idxmax()
]

print("\n======================================")
print("LARGEST PAYMENT")
print("======================================")

print(largest_payment)


# =====================================================
# 15. FINAL PAYMENT INSIGHTS
# =====================================================

print("\n======================================")
print("FINAL PAYMENT INSIGHTS")
print("======================================")

print("\nTotal Payment Amount:")
print(total_payment)

print("\nTotal Number of Payments:")
print(total_payments)

print("\nAverage Payment:")
print(average_payment)

print("\nMost Used Payment Method:")
print(payment_methods.idxmax())

print("\nHighest Revenue Payment Method:")
print(revenue_by_method.idxmax())

print("\nHighest Payment Amount:")
print(largest_payment["Amount"])


# =====================================================
# 16. CLOSE DATABASE
# =====================================================

connection.close()

print("\nDatabase connection closed!")