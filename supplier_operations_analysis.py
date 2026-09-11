import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from urllib.parse import quote_plus


# ============================================================
# 1. DATABASE CONNECTION
# ============================================================

server = r"ZUBAIR\SQLEXPRESS"
database = "RetailECommerceDB"

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

engine = create_engine(
    "mssql+pyodbc:///?odbc_connect="
    + quote_plus(connection_string)
)

print("Database connection created successfully.")


# ============================================================
# 2. LOAD SUPPLIERS
# ============================================================

suppliers_query = """
SELECT *
FROM Purchasing.Suppliers
"""

suppliers = pd.read_sql(suppliers_query, engine)

print(f"Suppliers Loaded: {len(suppliers)}")

print("\nSupplier Columns:")
print(suppliers.columns.tolist())


# ============================================================
# 3. LOAD PRODUCTS
# ============================================================

products_query = """
SELECT *
FROM Inventory.Products
"""

products = pd.read_sql(products_query, engine)

print(f"\nProducts Loaded: {len(products)}")

print("\nProduct Columns:")
print(products.columns.tolist())


# ============================================================
# 4. LOAD INVENTORY
# ============================================================

inventory_query = """
SELECT *
FROM Inventory.Inventory
"""

inventory = pd.read_sql(inventory_query, engine)

print(f"\nInventory Loaded: {len(inventory)}")

print("\nInventory Columns:")
print(inventory.columns.tolist())


# ============================================================
# 5. LOAD SHIPMENTS
# ============================================================

shipments_query = """
SELECT *
FROM Sales.Shipments
"""

shipments = pd.read_sql(shipments_query, engine)

print(f"\nShipments Loaded: {len(shipments)}")

print("\nShipment Columns:")
print(shipments.columns.tolist())


# ============================================================
# 6. LOAD ORDERS
# ============================================================

orders_query = """
SELECT *
FROM Sales.Orders
"""

orders = pd.read_sql(orders_query, engine)

print(f"\nOrders Loaded: {len(orders)}")

print("\nOrder Columns:")
print(orders.columns.tolist())


# ============================================================
# 7. SUPPLIER COLUMN DETECTION
# ============================================================

supplier_columns_lower = {
    column.lower(): column
    for column in suppliers.columns
}

product_columns_lower = {
    column.lower(): column
    for column in products.columns
}

inventory_columns_lower = {
    column.lower(): column
    for column in inventory.columns
}

shipment_columns_lower = {
    column.lower(): column
    for column in shipments.columns
}

order_columns_lower = {
    column.lower(): column
    for column in orders.columns
}


# ============================================================
# 8. FIND IMPORTANT COLUMNS
# ============================================================

def find_column(column_dictionary, possible_names):

    for name in possible_names:

        if name.lower() in column_dictionary:
            return column_dictionary[name.lower()]

    return None


supplier_id_col = find_column(
    supplier_columns_lower,
    ["SupplierID", "SupplierId"]
)

supplier_name_col = find_column(
    supplier_columns_lower,
    ["SupplierName", "Name"]
)

product_id_col = find_column(
    product_columns_lower,
    ["ProductID", "ProductId"]
)

product_supplier_col = find_column(
    product_columns_lower,
    ["SupplierID", "SupplierId"]
)

cost_price_col = find_column(
    product_columns_lower,
    ["CostPrice", "PurchasePrice", "UnitCost"]
)

inventory_product_col = find_column(
    inventory_columns_lower,
    ["ProductID", "ProductId"]
)

stock_col = find_column(
    inventory_columns_lower,
    [
        "QuantityInStock",
        "CurrentStock",
        "Stock",
        "Quantity"
    ]
)


# ============================================================
# 9. VALIDATE SUPPLIER / PRODUCT COLUMNS
# ============================================================

print("\nDetected Supplier ID:", supplier_id_col)
print("Detected Supplier Name:", supplier_name_col)
print("Detected Product ID:", product_id_col)
print("Detected Product Supplier ID:", product_supplier_col)
print("Detected Cost Price:", cost_price_col)
print("Detected Inventory Product ID:", inventory_product_col)
print("Detected Stock Column:", stock_col)


if supplier_id_col is None:
    raise ValueError(
        "SupplierID column was not found in Suppliers table."
    )

if product_supplier_col is None:
    raise ValueError(
        "SupplierID column was not found in Products table."
    )

if product_id_col is None:
    raise ValueError(
        "ProductID column was not found in Products table."
    )

if inventory_product_col is None:
    raise ValueError(
        "ProductID column was not found in Inventory table."
    )

if stock_col is None:
    raise ValueError(
        "Stock column was not found in Inventory table."
    )


# ============================================================
# 10. SUPPLIER PRODUCT ANALYSIS
# ============================================================

supplier_product = products.merge(
    inventory[
        [inventory_product_col, stock_col]
    ],
    left_on=product_id_col,
    right_on=inventory_product_col,
    how="left"
)

supplier_product["CurrentStock"] = (
    supplier_product[stock_col]
    .fillna(0)
)


# ============================================================
# 11. INVENTORY VALUE
# ============================================================

if cost_price_col is not None:

    supplier_product["InventoryValue"] = (
        supplier_product["CurrentStock"]
        * supplier_product[cost_price_col]
    )

else:

    supplier_product["InventoryValue"] = 0


# ============================================================
# 12. SUPPLIER SCORECARD
# ============================================================

supplier_scorecard = (
    supplier_product
    .groupby(product_supplier_col)
    .agg(
        ProductsSupplied=(
            product_id_col,
            "nunique"
        ),
        TotalStock=(
            "CurrentStock",
            "sum"
        ),
        InventoryValue=(
            "InventoryValue",
            "sum"
        )
    )
    .reset_index()
)


# ============================================================
# 13. ADD SUPPLIER NAME
# ============================================================

if supplier_name_col is not None:

    supplier_names = suppliers[
        [supplier_id_col, supplier_name_col]
    ].drop_duplicates()

    supplier_scorecard = supplier_scorecard.merge(
        supplier_names,
        left_on=product_supplier_col,
        right_on=supplier_id_col,
        how="left"
    )

    supplier_scorecard = supplier_scorecard.drop(
        columns=[supplier_id_col]
    )

    supplier_scorecard = supplier_scorecard.rename(
        columns={
            product_supplier_col: "SupplierID",
            supplier_name_col: "SupplierName"
        }
    )

else:

    supplier_scorecard = supplier_scorecard.rename(
        columns={
            product_supplier_col: "SupplierID"
        }
    )

    supplier_scorecard["SupplierName"] = (
        "Supplier " +
        supplier_scorecard["SupplierID"].astype(str)
    )


# ============================================================
# 14. SORT SUPPLIER SCORECARD
# ============================================================

supplier_scorecard = (
    supplier_scorecard
    .sort_values(
        "InventoryValue",
        ascending=False
    )
    .reset_index(drop=True)
)


# ============================================================
# 15. SHIPMENT COLUMN DETECTION
# ============================================================

shipment_order_col = find_column(
    shipment_columns_lower,
    ["OrderID", "OrderId"]
)

shipment_date_col = find_column(
    shipment_columns_lower,
    [
    "ShippingDate",
    "ShipmentDate",
    "ShippedDate",
    "ShipDate",
    "DispatchDate"
]
)

delivery_date_col = find_column(
    shipment_columns_lower,
    [
        "DeliveryDate",
        "DeliveredDate",
        "ReceivedDate"
    ]
)

expected_date_col = find_column(
    shipment_columns_lower,
    [
        "ExpectedDeliveryDate",
        "EstimatedDeliveryDate",
        "ExpectedDate"
    ]
)

courier_col = find_column(
    shipment_columns_lower,
    [
        "Courier",
        "CourierName",
        "Carrier",
        "ShippingCompany"
    ]
)


print("\nDetected Shipment Order ID:", shipment_order_col)
print("Detected Shipment Date:", shipment_date_col)
print("Detected Delivery Date:", delivery_date_col)
print("Detected Expected Delivery Date:", expected_date_col)
print("Detected Courier:", courier_col)


# ============================================================
# 16. DELIVERY ANALYSIS
# ============================================================

delivery_analysis = shipments.copy()


if shipment_date_col is not None:

    delivery_analysis[shipment_date_col] = pd.to_datetime(
        delivery_analysis[shipment_date_col],
        errors="coerce"
    )


if delivery_date_col is not None:

    delivery_analysis[delivery_date_col] = pd.to_datetime(
        delivery_analysis[delivery_date_col],
        errors="coerce"
    )


if expected_date_col is not None:

    delivery_analysis[expected_date_col] = pd.to_datetime(
        delivery_analysis[expected_date_col],
        errors="coerce"
    )


# ============================================================
# 17. DELIVERY TIME
# ============================================================

if (
    shipment_date_col is not None
    and delivery_date_col is not None
):

    delivery_analysis["DeliveryDays"] = (
        delivery_analysis[delivery_date_col]
        - delivery_analysis[shipment_date_col]
    ).dt.days

else:

    delivery_analysis["DeliveryDays"] = np.nan


# ============================================================
# 18. DELIVERY STATUS
# ============================================================

if (
    expected_date_col is not None
    and delivery_date_col is not None
):

    delivery_analysis["DeliveryPerformance"] = np.where(
        delivery_analysis[delivery_date_col].isna(),
        "Pending",
        np.where(
            delivery_analysis[delivery_date_col]
            <= delivery_analysis[expected_date_col],
            "On Time",
            "Delayed"
        )
    )

else:

    delivery_analysis["DeliveryPerformance"] = np.where(
        delivery_analysis["DeliveryDays"].isna(),
        "Pending",
        "Delivered"
    )


# ============================================================
# 19. DELAY DAYS
# ============================================================

if (
    expected_date_col is not None
    and delivery_date_col is not None
):

    delivery_analysis["DelayDays"] = np.where(
        delivery_analysis[delivery_date_col].notna(),
        (
            delivery_analysis[delivery_date_col]
            - delivery_analysis[expected_date_col]
        ).dt.days,
        np.nan
    )

else:

    delivery_analysis["DelayDays"] = np.nan


# ============================================================
# 20. DELIVERY SUMMARY
# ============================================================

delivery_summary = pd.DataFrame(
    {
        "Metric": [
            "Total Shipments",
            "Delivered Shipments",
            "Pending Shipments",
            "On Time Shipments",
            "Delayed Shipments",
            "Average Delivery Days",
            "Average Delay Days"
        ],
        "Value": [
            len(delivery_analysis),
            delivery_analysis[
                "DeliveryDays"
            ].notna().sum(),
            (
                delivery_analysis[
                    "DeliveryPerformance"
                ] == "Pending"
            ).sum(),
            (
                delivery_analysis[
                    "DeliveryPerformance"
                ] == "On Time"
            ).sum(),
            (
                delivery_analysis[
                    "DeliveryPerformance"
                ] == "Delayed"
            ).sum(),
            delivery_analysis[
                "DeliveryDays"
            ].mean(),
            delivery_analysis[
                "DelayDays"
            ].mean()
        ]
    }
)


# ============================================================
# 21. COURIER PERFORMANCE
# ============================================================

if courier_col is not None:

    courier_performance = (
        delivery_analysis
        .groupby(courier_col)
        .agg(
            Shipments=(
                courier_col,
                "count"
            ),
            AverageDeliveryDays=(
                "DeliveryDays",
                "mean"
            ),
            AverageDelayDays=(
                "DelayDays",
                "mean"
            )
        )
        .reset_index()
    )

    courier_performance = courier_performance.rename(
        columns={
            courier_col: "Courier"
        }
    )

else:

    courier_performance = pd.DataFrame(
        columns=[
            "Courier",
            "Shipments",
            "AverageDeliveryDays",
            "AverageDelayDays"
        ]
    )


# ============================================================
# 22. COURIER DELIVERY STATUS
# ============================================================

if courier_col is not None:

    courier_status = pd.crosstab(
        delivery_analysis[courier_col],
        delivery_analysis[
            "DeliveryPerformance"
        ]
    ).reset_index()

    courier_status = courier_status.rename(
        columns={
            courier_col: "Courier"
        }
    )

else:

    courier_status = pd.DataFrame()


# ============================================================
# 23. ROUND NUMBERS
# ============================================================

for dataframe in [
    supplier_scorecard,
    delivery_summary,
    delivery_analysis,
    courier_performance
]:

    for column in [
        "InventoryValue",
        "AverageDeliveryDays",
        "AverageDelayDays",
        "DeliveryDays",
        "DelayDays"
    ]:

        if column in dataframe.columns:

            dataframe[column] = (
                dataframe[column]
                .round(2)
            )


# ============================================================
# 24. DISPLAY RESULTS
# ============================================================

print("\nSUPPLIER SCORECARD")

print(
    supplier_scorecard.to_string(
        index=False
    )
)


print("\nDELIVERY SUMMARY")

print(
    delivery_summary.to_string(
        index=False
    )
)


print("\nCOURIER PERFORMANCE")

print(
    courier_performance.to_string(
        index=False
    )
)


print("\nDELIVERY PERFORMANCE")

print(
    delivery_analysis[
        [
            "DeliveryPerformance"
        ]
    ]
    .value_counts()
    .to_string()
)


# ============================================================
# 25. EXPORT TO EXCEL
# ============================================================

output_file = "Supplier_Operations_Analysis.xlsx"


with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    supplier_scorecard.to_excel(
        writer,
        sheet_name="Supplier Scorecard",
        index=False
    )

    delivery_analysis.to_excel(
        writer,
        sheet_name="Delivery Analysis",
        index=False
    )

    delivery_summary.to_excel(
        writer,
        sheet_name="Delivery Summary",
        index=False
    )

    courier_performance.to_excel(
        writer,
        sheet_name="Courier Performance",
        index=False
    )

    courier_status.to_excel(
        writer,
        sheet_name="Courier Status",
        index=False
    )


print("\nSUPPLIER & OPERATIONS ANALYSIS COMPLETED")
print(f"Excel file: {output_file}")
print("Supplier Scorecard sheet created.")
print("Delivery Analysis sheet created.")
print("Delivery Summary sheet created.")
print("Courier Performance sheet created.")
print("Courier Status sheet created.")