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
# 2. LOAD SHIPMENTS
# ==========================================

query = """
SELECT *
FROM Sales.Shipments
"""

shipments = pd.read_sql(
    query,
    connection
)


# ==========================================
# 3. DISPLAY DATA
# ==========================================

print("\n======================================")
print("SHIPMENTS DATA")
print("======================================")

print(shipments.head())


# ==========================================
# 4. BASIC INFORMATION
# ==========================================

print("\nShipments Shape:")
print(shipments.shape)

print("\nShipments Columns:")
print(shipments.columns.tolist())


# ==========================================
# 5. DATA INFORMATION
# ==========================================

print("\n======================================")
print("SHIPMENT DATA INFORMATION")
print("======================================")

shipments.info()


# ==========================================
# 6. MISSING VALUES
# ==========================================

print("\n======================================")
print("MISSING VALUES")
print("======================================")

print(shipments.isnull().sum())


# ==========================================
# 7. CONVERT DATES
# ==========================================

shipments["ShippingDate"] = pd.to_datetime(
    shipments["ShippingDate"],
    errors="coerce"
)

shipments["DeliveryDate"] = pd.to_datetime(
    shipments["DeliveryDate"],
    errors="coerce"
)


# ==========================================
# 8. TOTAL SHIPMENTS
# ==========================================

total_shipments = shipments["ShipmentID"].nunique()

print("\n======================================")
print("TOTAL SHIPMENTS")
print("======================================")

print(total_shipments)


# ==========================================
# 9. DELIVERED SHIPMENTS
# ==========================================

delivered_shipments = shipments[
    shipments["DeliveryDate"].notna()
]

total_delivered = len(delivered_shipments)

print("\n======================================")
print("DELIVERED SHIPMENTS")
print("======================================")

print(total_delivered)


# ==========================================
# 10. PENDING SHIPMENTS
# ==========================================

pending_shipments = shipments[
    shipments["DeliveryDate"].isna()
]

total_pending = len(pending_shipments)

print("\n======================================")
print("PENDING SHIPMENTS")
print("======================================")

print(total_pending)


# ==========================================
# 11. SHIPMENTS BY COURIER
# ==========================================

courier_count = (
    shipments["Courier"]
    .value_counts()
)

print("\n======================================")
print("SHIPMENTS BY COURIER")
print("======================================")

print(courier_count)


# ==========================================
# 12. MOST USED COURIER
# ==========================================

most_used_courier = courier_count.idxmax()

most_used_courier_count = courier_count.max()

print("\n======================================")
print("MOST USED COURIER")
print("======================================")

print("Courier:", most_used_courier)
print("Shipments:", most_used_courier_count)


# ==========================================
# 13. DELIVERY TIME
# ==========================================

delivered_shipments = delivered_shipments.copy()

delivered_shipments["DeliveryDays"] = (
    delivered_shipments["DeliveryDate"]
    - delivered_shipments["ShippingDate"]
).dt.days


print("\n======================================")
print("DELIVERY TIME")
print("======================================")

print(
    delivered_shipments[
        [
            "ShipmentID",
            "Courier",
            "ShippingDate",
            "DeliveryDate",
            "DeliveryDays"
        ]
    ].head(10)
)


# ==========================================
# 14. AVERAGE DELIVERY TIME
# ==========================================

average_delivery_days = (
    delivered_shipments["DeliveryDays"]
    .mean()
)

print("\n======================================")
print("AVERAGE DELIVERY TIME")
print("======================================")

print(
    round(average_delivery_days, 2),
    "days"
)


# ==========================================
# 15. FASTEST DELIVERY
# ==========================================

fastest_delivery = (
    delivered_shipments["DeliveryDays"]
    .min()
)

print("\n======================================")
print("FASTEST DELIVERY")
print("======================================")

print(
    fastest_delivery,
    "days"
)


# ==========================================
# 16. SLOWEST DELIVERY
# ==========================================

slowest_delivery = (
    delivered_shipments["DeliveryDays"]
    .max()
)

print("\n======================================")
print("SLOWEST DELIVERY")
print("======================================")

print(
    slowest_delivery,
    "days"
)


# ==========================================
# 17. AVERAGE DELIVERY TIME BY COURIER
# ==========================================

courier_delivery_time = (
    delivered_shipments
    .groupby("Courier")["DeliveryDays"]
    .mean()
    .sort_values()
)

print("\n======================================")
print("AVERAGE DELIVERY TIME BY COURIER")
print("======================================")

print(
    courier_delivery_time.round(2)
)


# ==========================================
# 18. BEST COURIER BY DELIVERY TIME
# ==========================================

best_courier = courier_delivery_time.idxmin()

best_courier_days = courier_delivery_time.min()

print("\n======================================")
print("BEST COURIER")
print("======================================")

print("Courier:", best_courier)
print(
    "Average Delivery:",
    round(best_courier_days, 2),
    "days"
)


# ==========================================
# 19. COURIER GRAPH
# ==========================================

plt.figure(figsize=(10, 6))

courier_count.plot(
    kind="bar"
)

plt.title("Shipments by Courier")
plt.xlabel("Courier")
plt.ylabel("Number of Shipments")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# ==========================================
# 20. DELIVERY TIME BY COURIER GRAPH
# ==========================================

plt.figure(figsize=(10, 6))

courier_delivery_time.plot(
    kind="bar"
)

plt.title("Average Delivery Time by Courier")
plt.xlabel("Courier")
plt.ylabel("Average Delivery Days")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# ==========================================
# 21. DELIVERY STATUS GRAPH
# ==========================================

delivery_status = pd.Series(
    {
        "Delivered": total_delivered,
        "Pending": total_pending
    }
)

plt.figure(figsize=(8, 5))

delivery_status.plot(
    kind="bar"
)

plt.title("Shipment Delivery Status")
plt.xlabel("Status")
plt.ylabel("Number of Shipments")

plt.xticks(rotation=0)
plt.tight_layout()

plt.show()


# ==========================================
# 22. FINAL SHIPMENT INSIGHTS
# ==========================================

print("\n")
print("==============================================")
print("FINAL SHIPMENT INSIGHTS")
print("==============================================")


print("\nTotal Shipments:")
print(total_shipments)


print("\nDelivered Shipments:")
print(total_delivered)


print("\nPending Shipments:")
print(total_pending)


print("\nMost Used Courier:")
print(most_used_courier)


print("\nMost Used Courier Shipments:")
print(most_used_courier_count)


print("\nAverage Delivery Time:")
print(
    round(average_delivery_days, 2),
    "days"
)


print("\nFastest Delivery:")
print(
    fastest_delivery,
    "days"
)


print("\nSlowest Delivery:")
print(
    slowest_delivery,
    "days"
)


print("\nBest Courier:")
print(best_courier)


print("\nBest Courier Average Delivery:")
print(
    round(best_courier_days, 2),
    "days"
)


# ==========================================
# 23. CLOSE CONNECTION
# ==========================================

connection.close()

print("\nDatabase connection closed!")

print("\nSHIPMENT ANALYSIS COMPLETED SUCCESSFULLY!")