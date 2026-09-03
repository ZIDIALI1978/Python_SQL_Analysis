# ============================================================
# RETAIL E-COMMERCE PROFESSIONAL EXCEL DASHBOARD
# STEP 8 - FINAL VERSION
# ============================================================
# ============================================================
# RETAIL E-COMMERCE PROFESSIONAL EXCEL DASHBOARD
# STEP 8 - FINAL VERSION
# ============================================================

from openpyxl import Workbook
from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment,
    Border,
    Side
)
from openpyxl.utils import get_column_letter

from openpyxl.chart import (
    BarChart,
    LineChart,
    PieChart,
    DoughnutChart,
    Reference
)

from openpyxl.formatting.rule import (
    CellIsRule,
    FormulaRule
)

from openpyxl.worksheet.table import (
    Table,
    TableStyleInfo
)

import pyodbc
import pandas as pd
import numpy as np

from datetime import datetime
from pathlib import Path


# ============================================================
# 1. DATABASE CONNECTION
# ============================================================

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=ZUBAIR\\SQLEXPRESS;"
    "DATABASE=RetailECommerceDB;"
    "Trusted_Connection=yes;"
)

print("=" * 80)
print("       RETAIL E-COMMERCE PROFESSIONAL EXCEL DASHBOARD")
print("=" * 80)

print("\nDatabase connected successfully!")


# ============================================================
# 2. OUTPUT FILE
# ============================================================

output_folder = Path.cwd()

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

output_file = (
    output_folder
    / f"Retail_ECommerce_Final_Analysis_{timestamp}.xlsx"
)

print("\nOutput File:")
print(output_file)


# ============================================================
# 3. CREATE WORKBOOK
# ============================================================

wb = Workbook()

default_sheet = wb.active

wb.remove(default_sheet)


# ============================================================
# 4. EXCEL COLORS / STYLES
# ============================================================

dark_blue = "1F4E78"

light_blue = "D9EAF7"

green = "70AD47"

light_green = "E2F0D9"

orange = "ED7D31"

light_orange = "FCE4D6"

red = "C00000"

light_red = "F4CCCC"

yellow = "FFC000"

light_yellow = "FFF2CC"

purple = "7030A0"

light_purple = "E4DFEC"

white = "FFFFFF"

black = "000000"

gray = "D9E1F2"


# ============================================================
# 5. FONTS
# ============================================================

title_font = Font(
    bold=True,
    size=20,
    color=white
)

section_font = Font(
    bold=True,
    size=14,
    color=white
)

header_font = Font(
    bold=True,
    size=11,
    color=white
)

kpi_label_font = Font(
    bold=True,
    size=11,
    color=white
)

kpi_value_font = Font(
    bold=True,
    size=16,
    color=black
)


# ============================================================
# 6. FILLS
# ============================================================

header_fill = PatternFill(
    fill_type="solid",
    fgColor=dark_blue
)

title_fill = PatternFill(
    fill_type="solid",
    fgColor=dark_blue
)

green_fill = PatternFill(
    fill_type="solid",
    fgColor=green
)

orange_fill = PatternFill(
    fill_type="solid",
    fgColor=orange
)

red_fill = PatternFill(
    fill_type="solid",
    fgColor=red
)

yellow_fill = PatternFill(
    fill_type="solid",
    fgColor=yellow
)

purple_fill = PatternFill(
    fill_type="solid",
    fgColor=purple
)


# ============================================================
# 7. BORDER
# ============================================================

thin_side = Side(
    style="thin",
    color="B7B7B7"
)

thin_border = Border(
    left=thin_side,
    right=thin_side,
    top=thin_side,
    bottom=thin_side
)


# ============================================================
# 8. FUNCTION - WRITE DATAFRAME
# ============================================================

def write_dataframe_to_excel(df, sheet_name):

    sheet_name = sheet_name[:31]

    ws = wb.create_sheet(sheet_name)

    # --------------------------------------------------------
    # Headers
    # --------------------------------------------------------

    for col_num, column_name in enumerate(
        df.columns,
        1
    ):

        cell = ws.cell(
            row=1,
            column=col_num,
            value=column_name
        )

        cell.fill = header_fill

        cell.font = header_font

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

        cell.border = thin_border

    # --------------------------------------------------------
    # Data
    # --------------------------------------------------------

    for row_num, row_data in enumerate(
        df.itertuples(index=False),
        2
    ):

        for col_num, value in enumerate(
            row_data,
            1
        ):

            if pd.isna(value):
                value = None

            cell = ws.cell(
                row=row_num,
                column=col_num,
                value=value
            )

            cell.border = thin_border

    # --------------------------------------------------------
    # Freeze Header
    # --------------------------------------------------------

    ws.freeze_panes = "A2"

    # --------------------------------------------------------
    # Auto Filter
    # --------------------------------------------------------

    if ws.max_row >= 2:
        ws.auto_filter.ref = ws.dimensions

    # --------------------------------------------------------
    # Column Width
    # --------------------------------------------------------

    for column_cells in ws.columns:

        max_length = 0

        column_letter = get_column_letter(
            column_cells[0].column
        )

        for cell in column_cells:

            try:

                length = len(
                    str(cell.value)
                )

                max_length = max(
                    max_length,
                    length
                )

            except:
                pass

        ws.column_dimensions[
            column_letter
        ].width = min(
            max_length + 2,
            40
        )

    # --------------------------------------------------------
    # Add Excel Table
    # --------------------------------------------------------

    if ws.max_row >= 2 and ws.max_column >= 1:

        table_ref = (
            f"A1:"
            f"{get_column_letter(ws.max_column)}"
            f"{ws.max_row}"
        )

        table = Table(
            displayName=(
                "Table_" +
                sheet_name.replace(" ", "")
            ),
            ref=table_ref
        )

        style = TableStyleInfo(
            name="TableStyleMedium2",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=False
        )

        table.tableStyleInfo = style

        ws.add_table(table)

    return ws


# ============================================================
# 9. LOAD CUSTOMERS
# ============================================================

customers = pd.read_sql(
    """
    SELECT
        CustomerID,
        FirstName,
        LastName,
        IsActive
    FROM Sales.Customers
    """,
    connection
)

print(
    "Customers Loaded:",
    len(customers)
)


# ============================================================
# 10. LOAD ORDERS
# ============================================================

orders = pd.read_sql(
    """
    SELECT
        OrderID,
        CustomerID,
        OrderDate,
        Status
    FROM Sales.Orders
    """,
    connection
)

print(
    "Orders Loaded:",
    len(orders)
)


# ============================================================
# 11. LOAD ORDER ITEMS
# ============================================================

order_items = pd.read_sql(
    """
    SELECT
        OrderItemID,
        OrderID,
        ProductID,
        Quantity,
        UnitPrice
    FROM Sales.OrderItems
    """,
    connection
)

print(
    "Order Items Loaded:",
    len(order_items)
)


# ============================================================
# 12. LOAD PRODUCTS
# ============================================================

products = pd.read_sql(
    """
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
    """,
    connection
)

print(
    "Products Loaded:",
    len(products)
)


# ============================================================
# 13. LOAD PAYMENTS
# ============================================================

payments = pd.read_sql(
    """
    SELECT
        PaymentID,
        OrderID,
        Amount,
        PaymentMethod,
        PaymentDate
    FROM Sales.Payments
    """,
    connection
)

print(
    "Payments Loaded:",
    len(payments)
)


# ============================================================
# 14. LOAD REVIEWS
# ============================================================

reviews = pd.read_sql(
    """
    SELECT
        ReviewID,
        CustomerID,
        ProductID,
        Rating,
        ReviewDate
    FROM Sales.Reviews
    """,
    connection
)

print(
    "Reviews Loaded:",
    len(reviews)
)


# ============================================================
# 15. LOAD ADDRESSES
# ============================================================

addresses = pd.read_sql(
    """
    SELECT
        AddressID,
        CustomerID,
        AddressLine1,
        City,
        StateProvince,
        PostalCode,
        Country
    FROM Sales.Addresses
    """,
    connection
)

print(
    "Addresses Loaded:",
    len(addresses)
)


# ============================================================
# 16. LOAD SHIPMENTS
# ============================================================

shipments = pd.read_sql(
    """
    SELECT
        ShipmentID,
        OrderID,
        Courier,
        TrackingNumber,
        ShippingDate,
        DeliveryDate
    FROM Sales.Shipments
    """,
    connection
)

print(
    "Shipments Loaded:",
    len(shipments)
)


# ============================================================
# 17. FIND SUPPLIER TABLE
# ============================================================

supplier_table = None

for schema in [
    "Purchasing",
    "Inventory",
    "Sales",
    "dbo"
]:

    check = pd.read_sql(
        f"""
        SELECT COUNT(*) AS TableCount
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = '{schema}'
        AND TABLE_NAME = 'Suppliers'
        """,
        connection
    )

    if int(
        check.iloc[0]["TableCount"]
    ) > 0:

        supplier_table = (
            f"[{schema}].[Suppliers]"
        )

        break


if supplier_table is None:

    raise RuntimeError(
        "Suppliers table was not found."
    )


# ============================================================
# 18. LOAD SUPPLIERS
# ============================================================

suppliers = pd.read_sql(
    f"""
    SELECT
        SupplierID,
        SupplierName,
        Email,
        Phone
    FROM {supplier_table}
    """,
    connection
)

print(
    "Suppliers Loaded:",
    len(suppliers)
)


# ============================================================
# 19. LOAD INVENTORY
# ============================================================

inventory = pd.read_sql(
    """
    SELECT
        ProductID,
        QuantityInStock,
        ReorderLevel
    FROM Inventory.Inventory
    """,
    connection
)

print(
    "Inventory Loaded:",
    len(inventory)
)


# ============================================================
# 20. LOAD EMPLOYEES
# ============================================================

employees = pd.read_sql(
    """
    SELECT
        EmployeeID,
        FirstName,
        LastName,
        Email
    FROM HR.Employees
    """,
    connection
)

print(
    "Employees Loaded:",
    len(employees)
)


# ============================================================
# 21. DATA CLEANING
# ============================================================

order_items["Quantity"] = pd.to_numeric(
    order_items["Quantity"],
    errors="coerce"
).fillna(0)

order_items["UnitPrice"] = pd.to_numeric(
    order_items["UnitPrice"],
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
# 22. CALCULATE REVENUE
# ============================================================

order_items["Revenue"] = (
    order_items["Quantity"]
    *
    order_items["UnitPrice"]
)


# ============================================================
# 23. CREATE MASTER SALES DATA
# ============================================================

sales_data = order_items.merge(
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


sales_data["CustomerName"] = (
    sales_data["FirstName"]
    .fillna("")
    .astype(str)
    + " "
    +
    sales_data["LastName"]
    .fillna("")
    .astype(str)
).str.strip()


# ============================================================
# 24. PROFIT ANALYSIS
# ============================================================

sales_data["ProfitPerUnit"] = (
    sales_data["SellingPrice"]
    -
    sales_data["CostPrice"]
)

sales_data["TotalProfit"] = (
    sales_data["ProfitPerUnit"]
    *
    sales_data["Quantity"]
)

sales_data["ProfitMargin"] = np.where(
    sales_data["SellingPrice"] != 0,

    (
        sales_data["ProfitPerUnit"]
        /
        sales_data["SellingPrice"]
    )
    *
    100,

    0
)


# ============================================================
# 25. CUSTOMER KPIs
# ============================================================

total_customers = (
    customers["CustomerID"]
    .nunique()
)

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
# 26. ADDRESS KPIs
# ============================================================

total_addresses = len(addresses)

unique_cities = (
    addresses["City"]
    .nunique()
)

city_counts = (
    addresses["City"]
    .value_counts()
)

state_counts = (
    addresses["StateProvince"]
    .value_counts()
)

country_counts = (
    addresses["Country"]
    .value_counts()
)

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
# 27. PRODUCT KPIs
# ============================================================

total_products = (
    products["ProductID"]
    .nunique()
)


# ============================================================
# 28. INVENTORY KPIs
# ============================================================

total_stock = (
    inventory["QuantityInStock"]
    .sum()
)

average_stock = (
    inventory["QuantityInStock"]
    .mean()
)

low_stock = inventory[
    (
        inventory["QuantityInStock"] > 0
    )
    &
    (
        inventory["QuantityInStock"]
        <=
        inventory["ReorderLevel"]
    )
]

out_of_stock = inventory[
    inventory["QuantityInStock"] == 0
]

reorder_required = inventory[
    inventory["QuantityInStock"]
    <=
    inventory["ReorderLevel"]
]


inventory["StockStatus"] = np.where(
    inventory["QuantityInStock"] == 0,
    "Out of Stock",

    np.where(
        inventory["QuantityInStock"]
        <=
        inventory["ReorderLevel"],

        "Low Stock",

        "In Stock"
    )
)

stock_status = (
    inventory["StockStatus"]
    .value_counts()
)


# ============================================================
# 29. SALES KPIs
# ============================================================

total_orders = (
    orders["OrderID"]
    .nunique()
)

total_quantity = (
    order_items["Quantity"]
    .sum()
)

total_revenue = (
    order_items["Revenue"]
    .sum()
)

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)


# ============================================================
# 30. PAYMENT KPIs
# ============================================================

total_payments = (
    payments["PaymentID"]
    .nunique()
)

total_payment_amount = (
    payments["Amount"]
    .sum()
)

average_payment = (
    payments["Amount"]
    .mean()
)


# ============================================================
# 31. REVIEW KPIs
# ============================================================

total_reviews = (
    reviews["ReviewID"]
    .nunique()
)

average_rating = (
    reviews["Rating"]
    .mean()
)

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
# 32. SHIPMENT KPIs
# ============================================================

total_shipments = len(
    shipments
)

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

courier_counts = (
    shipments["Courier"]
    .value_counts()
)

most_used_courier = (
    courier_counts.idxmax()
    if len(courier_counts) > 0
    else "N/A"
)


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
        delivered_data["DeliveryDays"]
        .mean()
    )

    average_delivery_by_courier = (
        delivered_data
        .groupby("Courier")["DeliveryDays"]
        .mean()
        .sort_values()
    )

else:

    average_delivery_time = 0

    average_delivery_by_courier = (
        pd.Series(dtype=float)
    )


if len(
    average_delivery_by_courier
) > 0:

    best_courier = (
        average_delivery_by_courier
        .idxmin()
    )

    best_courier_average = (
        average_delivery_by_courier
        .min()
    )

else:

    best_courier = "N/A"

    best_courier_average = 0


# ============================================================
# 33. SUPPLIER ANALYSIS
# ============================================================

total_suppliers = len(
    suppliers
)


supplier_products = products[
    [
        "ProductID",
        "SupplierID",
        "ProductName",
        "SellingPrice"
    ]
].copy()


supplier_price_data = (
    supplier_products
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


average_supplier_price = (
    supplier_price_data
    .groupby("SupplierName")
    ["SellingPrice"]
    .mean()
    .sort_values(
        ascending=False
    )
)


supplier_inventory_data = (
    supplier_products
    .merge(
        inventory[
            [
                "ProductID",
                "QuantityInStock"
            ]
        ],
        on="ProductID",
        how="left"
    )
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
    .groupby("SupplierName")
    ["QuantityInStock"]
    .sum()
    .sort_values(
        ascending=False
    )
)


if len(
    average_supplier_price
) > 0:

    highest_price_supplier = (
        average_supplier_price
        .idxmax()
    )

    highest_average_price = (
        average_supplier_price
        .max()
    )

else:

    highest_price_supplier = "N/A"

    highest_average_price = 0


if len(
    supplier_stock
) > 0:

    highest_inventory_supplier = (
        supplier_stock
        .idxmax()
    )

    highest_supplier_inventory = (
        supplier_stock
        .max()
    )

else:

    highest_inventory_supplier = "N/A"

    highest_supplier_inventory = 0


# ============================================================
# 34. EMPLOYEE KPI
# ============================================================

total_employees = len(
    employees
)


# ============================================================
# 35. TOP PRODUCTS BY REVENUE
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
    .sort_values(
        ascending=False
    )
)

top_products_df = (
    top_products
    .head(10)
    .reset_index()
)


# ============================================================
# 36. CATEGORY REVENUE
# ============================================================

category_revenue = (
    sales_data
    .groupby(
        "CategoryName"
    )["Revenue"]
    .sum()
    .sort_values(
        ascending=False
    )
)


# ============================================================
# 37. TOP CUSTOMERS
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
    .sort_values(
        ascending=False
    )
    .head(10)
    .reset_index()
)


# ============================================================
# 38. MONTHLY REVENUE
# ============================================================

monthly_sales = (
    sales_data
    .dropna(
        subset=["OrderDate"]
    )
    .copy()
)


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
# 39. PAYMENT METHOD
# ============================================================

payment_method_revenue = (
    payments
    .groupby(
        "PaymentMethod"
    )["Amount"]
    .sum()
    .sort_values(
        ascending=False
    )
)


# ============================================================
# 40. TOP RATED PRODUCTS
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
    .sort_values(
        ascending=False
    )
)


top_rated_products = (
    product_ratings
    .head(10)
    .reset_index()
)


# ============================================================
# 41. PROFIT KPIs
# ============================================================

total_profit = (
    sales_data["TotalProfit"]
    .sum()
)

average_profit_per_unit = (
    sales_data["ProfitPerUnit"]
    .mean()
)

average_profit_margin = (
    sales_data["ProfitMargin"]
    .mean()
)


# ============================================================
# 42. PROFIT BY PRODUCT
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
    .sort_values(
        ascending=False
    )
)


top_profit_products = (
    profit_by_product
    .head(10)
    .reset_index()
)


# ============================================================
# 43. PROFIT BY CATEGORY
# ============================================================

profit_by_category = (
    sales_data
    .groupby(
        "CategoryName"
    )["TotalProfit"]
    .sum()
    .sort_values(
        ascending=False
    )
)


# ============================================================
# 44. PROFIT MARGIN BY PRODUCT
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
    .sort_values(
        ascending=False
    )
)


top_margin_products = (
    product_profit_margin
    .head(10)
    .reset_index()
)


# ============================================================
# 45. BEST PERFORMERS
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


best_profit_product = (
    profit_by_product.idxmax()
    if len(profit_by_product) > 0
    else ("", "N/A")
)

best_profit_value = (
    profit_by_product.max()
    if len(profit_by_product) > 0
    else 0
)


best_profit_category = (
    profit_by_category.idxmax()
    if len(profit_by_category) > 0
    else "N/A"
)

best_category_profit = (
    profit_by_category.max()
    if len(profit_by_category) > 0
    else 0
)


best_margin_product = (
    product_profit_margin.idxmax()
    if len(product_profit_margin) > 0
    else ("", "N/A")
)

best_margin_value = (
    product_profit_margin.max()
    if len(product_profit_margin) > 0
    else 0
)


# ============================================================
# 46. EXPORT RAW DATA SHEETS
# ============================================================

write_dataframe_to_excel(
    customers,
    "Customers"
)

write_dataframe_to_excel(
    orders,
    "Orders"
)

write_dataframe_to_excel(
    order_items,
    "Order Items"
)

write_dataframe_to_excel(
    products,
    "Products"
)

write_dataframe_to_excel(
    payments,
    "Payments"
)

write_dataframe_to_excel(
    reviews,
    "Reviews"
)

write_dataframe_to_excel(
    addresses,
    "Addresses"
)

write_dataframe_to_excel(
    shipments,
    "Shipments"
)

write_dataframe_to_excel(
    suppliers,
    "Suppliers"
)

write_dataframe_to_excel(
    inventory,
    "Inventory"
)

write_dataframe_to_excel(
    employees,
    "Employees"
)

write_dataframe_to_excel(
    sales_data,
    "Sales Master"
)


# ============================================================
# 47. ANALYSIS SHEET FUNCTION
# ============================================================

def create_analysis_sheet(
    sheet_name,
    title,
    dataframe
):

    ws = wb.create_sheet(
        sheet_name
    )

    ws["A1"] = title

    ws["A1"].font = Font(
        bold=True,
        size=18,
        color=white
    )

    ws["A1"].fill = title_fill

    ws.merge_cells(
        start_row=1,
        start_column=1,
        end_row=1,
        end_column=max(
            2,
            len(dataframe.columns)
        )
    )

    ws["A1"].alignment = Alignment(
        horizontal="center"
    )

    # headers

    for col_num, column_name in enumerate(
        dataframe.columns,
        1
    ):

        cell = ws.cell(
            row=3,
            column=col_num,
            value=column_name
        )

        cell.fill = header_fill

        cell.font = header_font

        cell.alignment = Alignment(
            horizontal="center"
        )

        cell.border = thin_border

    # data

    for row_num, row_data in enumerate(
        dataframe.itertuples(index=False),
        4
    ):

        for col_num, value in enumerate(
            row_data,
            1
        ):

            if pd.isna(value):
                value = None

            cell = ws.cell(
                row=row_num,
                column=col_num,
                value=value
            )

            cell.border = thin_border

    ws.freeze_panes = "A4"

    # widths

    for column_cells in ws.columns:

        max_length = 0

        column_letter = get_column_letter(
            column_cells[0].column
        )

        for cell in column_cells:

            try:

                max_length = max(
                    max_length,
                    len(str(cell.value))
                )

            except:
                pass

        ws.column_dimensions[
            column_letter
        ].width = min(
            max_length + 3,
            40
        )

    return ws


# ============================================================
# 48. CREATE ANALYSIS DATAFRAMES
# ============================================================

customer_status_df = pd.DataFrame({
    "Customer Status": [
        "Active",
        "Inactive"
    ],
    "Customers": [
        active_customers,
        inactive_customers
    ]
})


city_df = (
    city_counts
    .reset_index()

)

city_df.columns = [
    "City",
    "Addresses"
]


state_df = (
    state_counts
    .reset_index()
)

state_df.columns = [
    "State",
    "Addresses"
]


category_df = (
    category_revenue
    .reset_index()
)

category_df.columns = [
    "Category",
    "Revenue"
]


order_status_df = (
    orders["Status"]
    .value_counts()
    .reset_index()
)

order_status_df.columns = [
    "Order Status",
    "Orders"
]


payment_df = (
    payment_method_revenue
    .reset_index()
)

payment_df.columns = [
    "Payment Method",
    "Payment Amount"
]


monthly_df = (
    monthly_revenue
    .reset_index()
)

monthly_df.columns = [
    "Month",
    "Revenue"
]

monthly_df["Month"] = (
    monthly_df["Month"]
    .astype(str)
)


profit_category_df = (
    profit_by_category
    .reset_index()
)

profit_category_df.columns = [
    "Category",
    "Profit"
]


stock_df = (
    stock_status
    .reset_index()
)

stock_df.columns = [
    "Stock Status",
    "Products"
]


courier_df = (
    courier_counts
    .reset_index()
)

courier_df.columns = [
    "Courier",
    "Shipments"
]


delivery_df = (
    average_delivery_by_courier
    .reset_index()
)

delivery_df.columns = [
    "Courier",
    "Average Delivery Days"
]


supplier_stock_df = (
    supplier_stock
    .reset_index()
)

supplier_stock_df.columns = [
    "Supplier",
    "Inventory"
]


supplier_price_df = (
    average_supplier_price
    .reset_index()
)

supplier_price_df.columns = [
    "Supplier",
    "Average Selling Price"
]


quantity_df = (
    sales_data
    .groupby("ProductName")["Quantity"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
    .reset_index()
)

quantity_df.columns = [
    "Product",
    "Quantity Sold"
]


review_product_df = (
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
    .reset_index()
)

review_product_df.columns = [
    "Product",
    "Reviews"
]


inventory_products = (
    inventory
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
)

top_inventory_df = (
    inventory_products
    .sort_values(
        "QuantityInStock",
        ascending=False
    )
    .head(10)
    [
        [
            "ProductName",
            "QuantityInStock"
        ]
    ]
)

top_inventory_df.columns = [
    "Product",
    "Inventory"
]


# ============================================================
# 49. CREATE ANALYSIS SHEETS
# ============================================================

create_analysis_sheet(
    "Customer Analysis",
    "CUSTOMER ANALYSIS",
    customer_status_df
)

create_analysis_sheet(
    "City Analysis",
    "ADDRESS ANALYSIS BY CITY",
    city_df
)

create_analysis_sheet(
    "State Analysis",
    "ADDRESS ANALYSIS BY STATE",
    state_df
)

create_analysis_sheet(
    "Category Analysis",
    "CATEGORY REVENUE ANALYSIS",
    category_df
)

create_analysis_sheet(
    "Order Status",
    "ORDER STATUS ANALYSIS",
    order_status_df
)

create_analysis_sheet(
    "Payment Analysis",
    "PAYMENT METHOD ANALYSIS",
    payment_df
)

create_analysis_sheet(
    "Monthly Revenue",
    "MONTHLY REVENUE ANALYSIS",
    monthly_df
)

create_analysis_sheet(
    "Profit Analysis",
    "PROFIT BY CATEGORY",
    profit_category_df
)

create_analysis_sheet(
    "Stock Analysis",
    "INVENTORY STOCK STATUS",
    stock_df
)

create_analysis_sheet(
    "Courier Analysis",
    "SHIPMENTS BY COURIER",
    courier_df
)

create_analysis_sheet(
    "Delivery Analysis",
    "AVERAGE DELIVERY TIME BY COURIER",
    delivery_df
)

create_analysis_sheet(
    "Supplier Stock",
    "INVENTORY BY SUPPLIER",
    supplier_stock_df
)

create_analysis_sheet(
    "Supplier Price",
    "AVERAGE SELLING PRICE BY SUPPLIER",
    supplier_price_df
)

create_analysis_sheet(
    "Quantity Analysis",
    "TOP PRODUCTS BY QUANTITY SOLD",
    quantity_df
)

create_analysis_sheet(
    "Product Reviews",
    "TOP PRODUCTS BY REVIEWS",
    review_product_df
)

create_analysis_sheet(
    "Top Inventory",
    "TOP PRODUCTS BY INVENTORY",
    top_inventory_df
)


# ============================================================
# 50. FINAL DASHBOARD
# ============================================================

dashboard = wb.create_sheet(
    "Dashboard",
    0
)


# ============================================================
# 51. DASHBOARD TITLE
# ============================================================

dashboard["A1"] = (
    "RETAIL E-COMMERCE BUSINESS DASHBOARD"
)

dashboard["A1"].font = title_font

dashboard["A1"].fill = title_fill

dashboard["A1"].alignment = Alignment(
    horizontal="center",
    vertical="center"
)

dashboard.merge_cells(
    "A1:N2"
)


dashboard["A3"] = (
    "Business Performance | Sales | Profit | Customers | Inventory | Payments"
)

dashboard["A3"].font = Font(
    italic=True,
    size=11
)

dashboard["A3"].alignment = Alignment(
    horizontal="center"
)

dashboard.merge_cells(
    "A3:N3"
)


# ============================================================
# 52. KPI FUNCTION
# ============================================================

def create_kpi(
    cell,
    label,
    value,
    fill
):

    row = dashboard[cell].row
    col = dashboard[cell].column

    label_cell = dashboard.cell(
        row=row,
        column=col,
        value=label
    )

    label_cell.fill = fill

    label_cell.font = kpi_label_font

    label_cell.alignment = Alignment(
        horizontal="center",
        vertical="center"
    )

    label_cell.border = thin_border

    value_cell = dashboard.cell(
        row=row + 1,
        column=col,
        value=value
    )

    value_cell.font = kpi_value_font

    value_cell.alignment = Alignment(
        horizontal="center",
        vertical="center"
    )

    value_cell.border = thin_border

    dashboard.merge_cells(
        start_row=row,
        start_column=col,
        end_row=row,
        end_column=col + 1
    )

    dashboard.merge_cells(
        start_row=row + 1,
        start_column=col,
        end_row=row + 1,
        end_column=col + 1
    )


# ============================================================
# 53. KPI CARDS
# ============================================================

create_kpi(
    "A5",
    "TOTAL CUSTOMERS",
    total_customers,
    header_fill
)

create_kpi(
    "C5",
    "TOTAL ORDERS",
    total_orders,
    green_fill
)

create_kpi(
    "E5",
    "TOTAL PRODUCTS",
    total_products,
    orange_fill
)

create_kpi(
    "G5",
    "TOTAL REVENUE",
    round(total_revenue, 2),
    purple_fill
)

create_kpi(
    "I5",
    "TOTAL PROFIT",
    round(total_profit, 2),
    green_fill
)

create_kpi(
    "K5",
    "TOTAL PAYMENTS",
    total_payments,
    orange_fill
)

create_kpi(
    "M5",
    "TOTAL REVIEWS",
    total_reviews,
    header_fill
)


create_kpi(
    "A9",
    "TOTAL STOCK",
    int(total_stock),
    orange_fill
)

create_kpi(
    "C9",
    "AVG ORDER VALUE",
    round(average_order_value, 2),
    purple_fill
)

create_kpi(
    "E9",
    "AVG RATING",
    round(average_rating, 2),
    green_fill
)

create_kpi(
    "G9",
    "TOTAL SHIPMENTS",
    total_shipments,
    header_fill
)

create_kpi(
    "I9",
    "LOW STOCK",
    len(low_stock),
    yellow_fill
)

create_kpi(
    "K9",
    "OUT OF STOCK",
    len(out_of_stock),
    red_fill
)

create_kpi(
    "M9",
    "AVG PROFIT MARGIN",
    round(
        average_profit_margin,
        2
    ),
    purple_fill
)


# ============================================================
# 54. BEST PERFORMERS SECTION
# ============================================================

dashboard["A13"] = (
    "BEST BUSINESS PERFORMERS"
)

dashboard["A13"].fill = title_fill

dashboard["A13"].font = section_font

dashboard.merge_cells(
    "A13:N13"
)

dashboard["A13"].alignment = Alignment(
    horizontal="center"
)


performers = [
    (
        "A15",
        "Best Product",
        best_product_name
    ),
    (
        "D15",
        "Best Category",
        best_category
    ),
    (
        "G15",
        "Top Customer",
        best_customer_name
    ),
    (
        "J15",
        "Best Payment",
        best_payment_method
    ),
    (
        "M15",
        "Best Month",
        str(best_month)
    ),
]


for position, label, value in performers:

    row = dashboard[position].row
    col = dashboard[position].column

    dashboard.cell(
        row=row,
        column=col,
        value=label
    )

    dashboard.cell(
        row=row,
        column=col
    ).fill = header_fill

    dashboard.cell(
        row=row,
        column=col
    ).font = header_font

    dashboard.cell(
        row=row,
        column=col
    ).alignment = Alignment(
        horizontal="center"
    )

    dashboard.cell(
        row=row,
        column=col
    ).border = thin_border

    dashboard.cell(
        row=row + 1,
        column=col,
        value=value
    )

    dashboard.cell(
        row=row + 1,
        column=col
    ).alignment = Alignment(
        horizontal="center",
        wrap_text=True
    )

    dashboard.cell(
        row=row + 1,
        column=col
    ).border = thin_border


# ============================================================
# 55. BEST PERFORMER VALUES
# ============================================================

dashboard["A18"] = "Best Product Revenue"

dashboard["B18"] = round(
    best_product_revenue,
    2
)

dashboard["D18"] = "Best Category Revenue"

dashboard["E18"] = round(
    best_category_revenue,
    2
)

dashboard["G18"] = "Top Customer Revenue"

dashboard["H18"] = round(
    best_customer_revenue,
    2
)

dashboard["J18"] = "Payment Amount"

dashboard["K18"] = round(
    best_payment_revenue,
    2
)

dashboard["M18"] = "Month Revenue"

dashboard["N18"] = round(
    best_month_revenue,
    2
)


for cell in [
    "A18",
    "B18",
    "D18",
    "E18",
    "G18",
    "H18",
    "J18",
    "K18",
    "M18",
    "N18"
]:

    dashboard[cell].border = thin_border

    dashboard[cell].alignment = Alignment(
        horizontal="center"
    )


# ============================================================
# 56. PROFIT SECTION
# ============================================================

dashboard["A21"] = (
    "PROFIT ANALYSIS"
)

dashboard["A21"].fill = purple_fill

dashboard["A21"].font = section_font

dashboard.merge_cells(
    "A21:N21"
)

dashboard["A21"].alignment = Alignment(
    horizontal="center"
)


profit_information = [
    (
        "A23",
        "Total Business Profit",
        round(total_profit, 2)
    ),

    (
        "D23",
        "Average Profit / Unit",
        round(
            average_profit_per_unit,
            2
        )
    ),

    (
        "G23",
        "Best Profit Product",
        (
            best_profit_product[1]
            if isinstance(
                best_profit_product,
                tuple
            )
            else best_profit_product
        )
    ),

    (
        "J23",
        "Best Profit Category",
        best_profit_category
    ),

    (
        "M23",
        "Best Margin Product",
        (
            best_margin_product[1]
            if isinstance(
                best_margin_product,
                tuple
            )
            else best_margin_product
        )
    )
]


for position, label, value in profit_information:

    row = dashboard[position].row
    col = dashboard[position].column

    dashboard.cell(
        row=row,
        column=col,
        value=label
    )

    dashboard.cell(
        row=row,
        column=col
    ).fill = purple_fill

    dashboard.cell(
        row=row,
        column=col
    ).font = header_font

    dashboard.cell(
        row=row,
        column=col
    ).alignment = Alignment(
        horizontal="center"
    )

    dashboard.cell(
        row=row,
        column=col
    ).border = thin_border

    dashboard.cell(
        row=row + 1,
        column=col,
        value=value
    )

    dashboard.cell(
        row=row + 1,
        column=col
    ).alignment = Alignment(
        horizontal="center",
        wrap_text=True
    )

    dashboard.cell(
        row=row + 1,
        column=col
    ).border = thin_border


# ============================================================
# 57. DASHBOARD COLUMN WIDTH
# ============================================================

for col in range(
    1,
    15
):

    dashboard.column_dimensions[
        get_column_letter(col)
    ].width = 16


# ============================================================
# 58. CONDITIONAL FORMATTING
# ============================================================

inventory_ws = wb["Inventory"]


# ------------------------------------------------------------
# CONDITIONAL FORMATTING COLORS
# ------------------------------------------------------------

cf_red_fill = PatternFill(
    fill_type="solid",
    fgColor="FFC7CE"
)

cf_yellow_fill = PatternFill(
    fill_type="solid",
    fgColor="FFEB9C"
)


# ------------------------------------------------------------
# OUT OF STOCK
# QuantityInStock = 0
# Column B
# ------------------------------------------------------------

inventory_ws.conditional_formatting.add(
    "B2:B1000",
    CellIsRule(
        operator="equal",
        formula=["0"],
        fill=cf_red_fill
    )
)


# ------------------------------------------------------------
# LOW STOCK
# QuantityInStock > 0
# AND
# QuantityInStock <= ReorderLevel
#
# B = QuantityInStock
# C = ReorderLevel
# ------------------------------------------------------------

inventory_ws.conditional_formatting.add(
    "B2:B1000",
    FormulaRule(
        formula=[
            'AND(B2>0,B2<=C2)'
        ],
        fill=cf_yellow_fill
    )
)


print(
    "Conditional formatting added successfully!"
)

# ============================================================
# 59. CREATE ALL 29 DASHBOARD CHARTS
# ============================================================

print("\nCreating 29 dashboard charts...")


# ============================================================
# HELPER FUNCTION
# ============================================================

def add_bar_chart(
    source_sheet,
    title,
    position,
    data_col=2,
    category_col=1,
    height=8,
    width=12,
    horizontal=False
):

    ws = wb[source_sheet]

    chart = BarChart()

    data = Reference(
        ws,
        min_col=data_col,
        min_row=3,
        max_row=ws.max_row
    )

    categories = Reference(
        ws,
        min_col=category_col,
        min_row=4,
        max_row=ws.max_row
    )

    chart.add_data(
        data,
        titles_from_data=True
    )

    chart.set_categories(
        categories
    )

    chart.title = title

    chart.height = height
    chart.width = width

    if horizontal:
        chart.type = "bar"

    dashboard.add_chart(
        chart,
        position
    )

    return chart


# ============================================================
# CHART 1
# CUSTOMER STATUS
# ============================================================

ws = wb["Customer Analysis"]

chart1 = DoughnutChart()

data = Reference(
    ws,
    min_col=2,
    min_row=3,
    max_row=5
)

labels = Reference(
    ws,
    min_col=1,
    min_row=4,
    max_row=5
)

chart1.add_data(
    data,
    titles_from_data=True
)

chart1.set_categories(
    labels
)

chart1.title = "Active vs Inactive Customers"

chart1.height = 8
chart1.width = 12

dashboard.add_chart(
    chart1,
    "A27"
)


# ============================================================
# CHART 2
# CATEGORY REVENUE
# ============================================================

add_bar_chart(
    "Category Analysis",
    "Revenue by Category",
    "G27",
    width=12
)


# ============================================================
# CHART 3
# MONTHLY REVENUE
# ============================================================

ws = wb["Monthly Revenue"]

chart3 = LineChart()

data = Reference(
    ws,
    min_col=2,
    min_row=3,
    max_row=ws.max_row
)

categories = Reference(
    ws,
    min_col=1,
    min_row=4,
    max_row=ws.max_row
)

chart3.add_data(
    data,
    titles_from_data=True
)

chart3.set_categories(
    categories
)

chart3.title = "Monthly Revenue Trend"

chart3.y_axis.title = "Revenue"
chart3.x_axis.title = "Month"

chart3.height = 8
chart3.width = 14

dashboard.add_chart(
    chart3,
    "A44"
)


# ============================================================
# CHART 4
# ORDER STATUS
# ============================================================

add_bar_chart(
    "Order Status",
    "Orders by Status",
    "H44",
    width=12
)


# ============================================================
# CHART 5
# PAYMENT METHOD
# ============================================================

ws = wb["Payment Analysis"]

chart5 = PieChart()

data = Reference(
    ws,
    min_col=2,
    min_row=3,
    max_row=ws.max_row
)

categories = Reference(
    ws,
    min_col=1,
    min_row=4,
    max_row=ws.max_row
)

chart5.add_data(
    data,
    titles_from_data=True
)

chart5.set_categories(
    categories
)

chart5.title = "Payment Method Distribution"

chart5.height = 8
chart5.width = 12

dashboard.add_chart(
    chart5,
    "A61"
)


# ============================================================
# CHART 6
# PROFIT BY CATEGORY
# ============================================================

add_bar_chart(
    "Profit Analysis",
    "Profit by Category",
    "G61",
    width=12
)


# ============================================================
# CHART 7
# INVENTORY STATUS
# ============================================================

ws = wb["Stock Analysis"]

chart7 = PieChart()

data = Reference(
    ws,
    min_col=2,
    min_row=3,
    max_row=ws.max_row
)

categories = Reference(
    ws,
    min_col=1,
    min_row=4,
    max_row=ws.max_row
)

chart7.add_data(
    data,
    titles_from_data=True
)

chart7.set_categories(
    categories
)

chart7.title = "Inventory Stock Status"

chart7.height = 8
chart7.width = 12

dashboard.add_chart(
    chart7,
    "M61"
)


# ============================================================
# CHART 8
# TOP PRODUCTS BY QUANTITY
# ============================================================

add_bar_chart(
    "Quantity Analysis",
    "Top Products by Quantity Sold",
    "A78",
    width=14,
    horizontal=True
)


# ============================================================
# CHART 9
# SHIPMENTS BY COURIER
# ============================================================

add_bar_chart(
    "Courier Analysis",
    "Shipments by Courier",
    "H78",
    width=12
)


# ============================================================
# CHART 10
# DELIVERY TIME BY COURIER
# ============================================================

if wb["Delivery Analysis"].max_row >= 4:

    add_bar_chart(
        "Delivery Analysis",
        "Average Delivery Time by Courier",
        "A95",
        width=12
    )


# ============================================================
# CHART 11
# SUPPLIER INVENTORY
# ============================================================

add_bar_chart(
    "Supplier Stock",
    "Inventory by Supplier",
    "H95",
    width=14,
    horizontal=True
)


# ============================================================
# CHART 12
# TOP PRODUCTS BY REVENUE
# ============================================================

top_product_chart_df = (
    sales_data
    .groupby("ProductName", as_index=False)["Revenue"]
    .sum()
    .sort_values(
        "Revenue",
        ascending=False
    )
    .head(10)
)

top_product_chart_df.columns = [
    "Product",
    "Revenue"
]


ws12 = create_analysis_sheet(
    "Top Revenue Products",
    "TOP PRODUCTS BY REVENUE",
    top_product_chart_df
)

add_bar_chart(
    "Top Revenue Products",
    "Top Products by Revenue",
    "A112",
    width=14,
    horizontal=True
)


# ============================================================
# CHART 13
# TOP CUSTOMERS BY REVENUE
# ============================================================

top_customer_chart_df = top_customers.copy()

top_customer_chart_df.columns = [
    "Customer ID",
    "Customer",
    "Revenue"
]

ws13 = create_analysis_sheet(
    "Top Customers",
    "TOP CUSTOMERS BY REVENUE",
    top_customer_chart_df
)


# Customer name = column B
# Revenue = column C

chart13 = BarChart()

data = Reference(
    ws13,
    min_col=3,
    min_row=3,
    max_row=ws13.max_row
)

categories = Reference(
    ws13,
    min_col=2,
    min_row=4,
    max_row=ws13.max_row
)

chart13.add_data(
    data,
    titles_from_data=True
)

chart13.set_categories(
    categories
)

chart13.title = "Top Customers by Revenue"

chart13.height = 8
chart13.width = 14

chart13.type = "bar"

dashboard.add_chart(
    chart13,
    "H112"
)


# ============================================================
# CHART 14
# TOP RATED PRODUCTS
# ============================================================

rated_chart_df = top_rated_products.copy()

rated_chart_df.columns = [
    "Product ID",
    "Product",
    "Rating"
]

ws14 = create_analysis_sheet(
    "Top Rated Products",
    "TOP RATED PRODUCTS",
    rated_chart_df
)

chart14 = BarChart()

data = Reference(
    ws14,
    min_col=3,
    min_row=3,
    max_row=ws14.max_row
)

categories = Reference(
    ws14,
    min_col=2,
    min_row=4,
    max_row=ws14.max_row
)

chart14.add_data(
    data,
    titles_from_data=True
)

chart14.set_categories(
    categories
)

chart14.title = "Top Rated Products"

chart14.height = 8
chart14.width = 14

chart14.type = "bar"

dashboard.add_chart(
    chart14,
    "A129"
)


# ============================================================
# CHART 15
# PROFIT BY PRODUCT
# ============================================================

profit_product_chart_df = top_profit_products.copy()

profit_product_chart_df.columns = [
    "Product ID",
    "Product",
    "Profit"
]

ws15 = create_analysis_sheet(
    "Top Profit Products",
    "TOP PRODUCTS BY PROFIT",
    profit_product_chart_df
)

chart15 = BarChart()

data = Reference(
    ws15,
    min_col=3,
    min_row=3,
    max_row=ws15.max_row
)

categories = Reference(
    ws15,
    min_col=2,
    min_row=4,
    max_row=ws15.max_row
)

chart15.add_data(
    data,
    titles_from_data=True
)

chart15.set_categories(
    categories
)

chart15.title = "Top Products by Profit"

chart15.height = 8
chart15.width = 14

chart15.type = "bar"

dashboard.add_chart(
    chart15,
    "H129"
)


# ============================================================
# CHART 16
# PROFIT MARGIN BY PRODUCT
# ============================================================

margin_chart_df = top_margin_products.copy()

margin_chart_df.columns = [
    "Product ID",
    "Product",
    "Profit Margin"
]

ws16 = create_analysis_sheet(
    "Top Profit Margins",
    "TOP PRODUCTS BY PROFIT MARGIN",
    margin_chart_df
)

chart16 = BarChart()

data = Reference(
    ws16,
    min_col=3,
    min_row=3,
    max_row=ws16.max_row
)

categories = Reference(
    ws16,
    min_col=2,
    min_row=4,
    max_row=ws16.max_row
)

chart16.add_data(
    data,
    titles_from_data=True
)

chart16.set_categories(
    categories
)

chart16.title = "Top Products by Profit Margin"

chart16.y_axis.title = "Profit Margin %"

chart16.height = 8
chart16.width = 14

chart16.type = "bar"

dashboard.add_chart(
    chart16,
    "A146"
)


# ============================================================
# CHART 17
# CITY-WISE ADDRESSES
# ============================================================

add_bar_chart(
    "City Analysis",
    "Addresses by City",
    "H146",
    width=14,
    horizontal=True
)


# ============================================================
# CHART 18
# STATE-WISE ADDRESSES
# ============================================================

add_bar_chart(
    "State Analysis",
    "Addresses by State",
    "A163",
    width=14,
    horizontal=True
)


# ============================================================
# CHART 19
# REVIEWS BY PRODUCT
# ============================================================

add_bar_chart(
    "Product Reviews",
    "Top Products by Number of Reviews",
    "H163",
    width=14,
    horizontal=True
)


# ============================================================
# CHART 20
# TOP INVENTORY PRODUCTS
# ============================================================

add_bar_chart(
    "Top Inventory",
    "Top Products by Inventory",
    "A180",
    width=14,
    horizontal=True
)


# ============================================================
# CHART 21
# SUPPLIER AVERAGE PRICE
# ============================================================

add_bar_chart(
    "Supplier Price",
    "Average Selling Price by Supplier",
    "H180",
    width=14,
    horizontal=True
)


# ============================================================
# CHART 22
# COURIER DELIVERY TIME
# ============================================================

if wb["Delivery Analysis"].max_row >= 4:

    add_bar_chart(
        "Delivery Analysis",
        "Courier Delivery Performance",
        "A197",
        width=14
    )


# ============================================================
# CHART 23
# CUSTOMER CITY DISTRIBUTION
# ============================================================

add_bar_chart(
    "City Analysis",
    "Customer Addresses by City",
    "H197",
    width=14,
    horizontal=True
)


# ============================================================
# CHART 24
# CUSTOMER STATE DISTRIBUTION
# ============================================================

add_bar_chart(
    "State Analysis",
    "Customer Addresses by State",
    "A214",
    width=14,
    horizontal=True
)


# ============================================================
# CHART 25
# SUPPLIER STOCK COMPARISON
# ============================================================

add_bar_chart(
    "Supplier Stock",
    "Supplier Inventory Comparison",
    "H214",
    width=14,
    horizontal=True
)


# ============================================================
# CHART 26
# SUPPLIER PRICE COMPARISON
# ============================================================

add_bar_chart(
    "Supplier Price",
    "Supplier Average Price Comparison",
    "A231",
    width=14,
    horizontal=True
)


# ============================================================
# CHART 27
# ORDER STATUS DISTRIBUTION
# ============================================================

ws27 = wb["Order Status"]

chart27 = PieChart()

data = Reference(
    ws27,
    min_col=2,
    min_row=3,
    max_row=ws27.max_row
)

categories = Reference(
    ws27,
    min_col=1,
    min_row=4,
    max_row=ws27.max_row
)

chart27.add_data(
    data,
    titles_from_data=True
)

chart27.set_categories(
    categories
)

chart27.title = "Order Status Distribution"

chart27.height = 8
chart27.width = 12

dashboard.add_chart(
    chart27,
    "H231"
)


# ============================================================
# CHART 28
# PAYMENT AMOUNT DISTRIBUTION
# ============================================================

ws28 = wb["Payment Analysis"]

chart28 = DoughnutChart()

data = Reference(
    ws28,
    min_col=2,
    min_row=3,
    max_row=ws28.max_row
)

categories = Reference(
    ws28,
    min_col=1,
    min_row=4,
    max_row=ws28.max_row
)

chart28.add_data(
    data,
    titles_from_data=True
)

chart28.set_categories(
    categories
)

chart28.title = "Payment Amount Distribution"

chart28.height = 8
chart28.width = 12

dashboard.add_chart(
    chart28,
    "A248"
)


# ============================================================
# CHART 29
# STOCK STATUS DISTRIBUTION
# ============================================================

ws29 = wb["Stock Analysis"]

chart29 = DoughnutChart()

data = Reference(
    ws29,
    min_col=2,
    min_row=3,
    max_row=ws29.max_row
)

categories = Reference(
    ws29,
    min_col=1,
    min_row=4,
    max_row=ws29.max_row
)

chart29.add_data(
    data,
    titles_from_data=True
)

chart29.set_categories(
    categories
)

chart29.title = "Stock Status Distribution"

chart29.height = 8
chart29.width = 12

dashboard.add_chart(
    chart29,
    "H248"
)


# ============================================================
# FINAL CHART COUNT
# ============================================================

print(
    "\n29 dashboard charts added successfully!"
)

print(
    "Total charts on Dashboard:",
    len(dashboard._charts)
)


# ============================================================
# 70. FINAL DASHBOARD FORMATTING
# ============================================================

print("\nApplying final dashboard formatting...")


# ------------------------------------------------------------
# DASHBOARD SETTINGS
# ------------------------------------------------------------

dashboard = wb["Dashboard"]
# ============================================================
# STEP 10 - PROFESSIONAL KPI CARDS
# ============================================================

print("\nFormatting professional KPI cards...")


# ------------------------------------------------------------
# KPI CARD RANGES
# ------------------------------------------------------------

kpi_ranges = [
    "A5:B6",
    "C5:D6",
    "E5:F6",
    "G5:H6",
    "I5:J6",
    "K5:L6",
    "M5:N6",

    "A9:B10",
    "C9:D10",
    "E9:F10",
    "G9:H10",
    "I9:J10",
    "K9:L10",
    "M9:N10"
]


# ------------------------------------------------------------
# KPI CARD BORDER
# ------------------------------------------------------------

from openpyxl.styles import Border, Side, Alignment, Font

thin_border = Side(
    style="thin"
)

kpi_border = Border(
    left=thin_border,
    right=thin_border,
    top=thin_border,
    bottom=thin_border
)


# ------------------------------------------------------------
# APPLY KPI CARD FORMATTING
# ------------------------------------------------------------

for cell_range in kpi_ranges:

    for row in dashboard[cell_range]:

        for cell in row:

            cell.border = kpi_border

            cell.alignment = Alignment(
                horizontal="center",
                vertical="center",
                wrap_text=True
            )


# ------------------------------------------------------------
# KPI LABEL ROWS
# ------------------------------------------------------------

kpi_label_cells = [
    "A5",
    "C5",
    "E5",
    "G5",
    "I5",
    "K5",
    "M5",

    "A9",
    "C9",
    "E9",
    "G9",
    "I9",
    "K9",
    "M9"
]


for cell in kpi_label_cells:

    dashboard[cell].font = Font(
        bold=True,
        size=11
    )

    dashboard[cell].alignment = Alignment(
        horizontal="center",
        vertical="center",
        wrap_text=True
    )


# ------------------------------------------------------------
# KPI VALUE CELLS
# ------------------------------------------------------------

kpi_value_cells = [
    "A6",
    "C6",
    "E6",
    "G6",
    "I6",
    "K6",
    "M6",

    "A10",
    "C10",
    "E10",
    "G10",
    "I10",
    "K10",
    "M10"
]


for cell in kpi_value_cells:

    dashboard[cell].font = Font(
        bold=True,
        size=16
    )

    dashboard[cell].alignment = Alignment(
        horizontal="center",
        vertical="center"
    )


print(
    "Professional KPI cards formatted successfully!"
)



# ============================================================
# STEP 9 - PROFESSIONAL DASHBOARD LAYOUT
# ============================================================

print("\nApplying professional dashboard layout...")


# ------------------------------------------------------------
# COLUMN WIDTHS
# ------------------------------------------------------------

dashboard.column_dimensions["A"].width = 16
dashboard.column_dimensions["B"].width = 14
dashboard.column_dimensions["C"].width = 14
dashboard.column_dimensions["D"].width = 14
dashboard.column_dimensions["E"].width = 14
dashboard.column_dimensions["F"].width = 14
dashboard.column_dimensions["G"].width = 14
dashboard.column_dimensions["H"].width = 14
dashboard.column_dimensions["I"].width = 14
dashboard.column_dimensions["J"].width = 14
dashboard.column_dimensions["K"].width = 14
dashboard.column_dimensions["L"].width = 14
dashboard.column_dimensions["M"].width = 14
dashboard.column_dimensions["N"].width = 16


# ------------------------------------------------------------
# ROW HEIGHTS FOR DASHBOARD SECTIONS
# ------------------------------------------------------------

for row_number in range(1, 116):

    if dashboard.row_dimensions[row_number].height is None:

        dashboard.row_dimensions[row_number].height = 20


# ------------------------------------------------------------
# DASHBOARD VIEW
# ------------------------------------------------------------

dashboard.sheet_view.showGridLines = False

dashboard.sheet_view.zoomScale = 85


# ------------------------------------------------------------
# PRINT SETTINGS
# ------------------------------------------------------------

dashboard.page_setup.orientation = "landscape"

dashboard.page_setup.paperSize = dashboard.PAPERSIZE_A4

dashboard.page_setup.fitToWidth = 1

dashboard.page_setup.fitToHeight = 0

dashboard.sheet_properties.pageSetUpPr.fitToPage = True


# ------------------------------------------------------------
# MARGINS
# ------------------------------------------------------------

dashboard.page_margins.left = 0.25

dashboard.page_margins.right = 0.25

dashboard.page_margins.top = 0.5

dashboard.page_margins.bottom = 0.5


print("Professional dashboard layout applied successfully!")

# Hide gridlines
dashboard.sheet_view.showGridLines = False

# Set zoom level
dashboard.sheet_view.zoomScale = 85

# Freeze dashboard
dashboard.freeze_panes = "A5"


# ------------------------------------------------------------
# DASHBOARD ROW HEIGHTS
# ------------------------------------------------------------

dashboard.row_dimensions[1].height = 25
dashboard.row_dimensions[2].height = 25
dashboard.row_dimensions[3].height = 22

dashboard.row_dimensions[5].height = 22
dashboard.row_dimensions[6].height = 28

dashboard.row_dimensions[9].height = 22
dashboard.row_dimensions[10].height = 28

dashboard.row_dimensions[13].height = 25

dashboard.row_dimensions[15].height = 22
dashboard.row_dimensions[16].height = 35

dashboard.row_dimensions[18].height = 24

dashboard.row_dimensions[21].height = 25

dashboard.row_dimensions[23].height = 22
dashboard.row_dimensions[24].height = 35


# ------------------------------------------------------------
# KPI VALUE FORMATTING
# ------------------------------------------------------------

kpi_currency_cells = [
    "G6",
    "I6",
    "C10",
    "M24"
]

for cell in kpi_currency_cells:

    dashboard[cell].number_format = '#,##0.00'


# ------------------------------------------------------------
# KPI NUMBER FORMATTING
# ------------------------------------------------------------

kpi_number_cells = [
    "A6",
    "C6",
    "E6",
    "K6",
    "M6",
    "A10",
    "G10",
    "I10",
    "K10"
]

for cell in kpi_number_cells:

    dashboard[cell].number_format = '#,##0'


# ------------------------------------------------------------
# RATING FORMAT
# ------------------------------------------------------------

dashboard["E10"].number_format = '0.00'


# ------------------------------------------------------------
# PROFIT SECTION FORMATTING
# ------------------------------------------------------------

dashboard["A24"].number_format = '#,##0.00'
dashboard["D24"].number_format = '#,##0.00'


# ------------------------------------------------------------
# BEST PERFORMER VALUES
# ------------------------------------------------------------

for cell in [
    "B18",
    "E18",
    "H18",
    "K18",
    "N18"
]:

    dashboard[cell].number_format = '#,##0.00'


# ------------------------------------------------------------
# ALIGN DASHBOARD CELLS
# ------------------------------------------------------------

for row in dashboard.iter_rows():

    for cell in row:

        if cell.value is not None:

            cell.alignment = Alignment(
                horizontal="center",
                vertical="center",
                wrap_text=True
            )


# ------------------------------------------------------------
# SET PRINT AREA
# ------------------------------------------------------------

dashboard.print_area = "A1:N115"


# ------------------------------------------------------------
# PAGE SETUP
# ------------------------------------------------------------

dashboard.page_setup.orientation = "landscape"

dashboard.page_setup.fitToWidth = 1

dashboard.page_setup.fitToHeight = 0

dashboard.sheet_properties.pageSetUpPr.fitToPage = True


print(
    "Final dashboard formatting applied successfully!"
)


# ============================================================
# 71. FINAL SAVE WORKBOOK
# ============================================================

print("\nSaving final Excel workbook...")


try:

    wb.save(output_file)

    print(
        "\nExcel workbook saved successfully!"
    )

except PermissionError:

    print(
        "\nERROR: Excel file is currently open or locked."
    )

    print(
        "Please close the Excel file and run the script again."
    )

    connection.close()

    raise

except Exception as e:

    print(
        "\nERROR: Could not save Excel workbook."
    )

    print(e)

    connection.close()

    raise


# ============================================================
# 72. CLOSE DATABASE
# ============================================================

try:

    connection.close()

    print(
        "\nDatabase connection closed."
    )

except Exception:

    pass


# ============================================================
# 73. FINAL OUTPUT
# ============================================================

print("\n")

print("=" * 80)

print(
    "EXCEL DASHBOARD CREATED SUCCESSFULLY!"
)

print("=" * 80)


print(
    "\nFile Name:",
    output_file
)


print(
    "\nTotal Sheets:",
    len(wb.sheetnames)
)


print("\nSheets Created:")

for sheet in wb.sheetnames:

    print(
        " -",
        sheet
    )


print("\n")

print("=" * 80)

print(
    "TOTAL DASHBOARD CHARTS:",
    len(dashboard._charts)
)

print("=" * 80)


print(
    "\nSTEP 8 - PROFESSIONAL EXCEL DASHBOARD COMPLETED!"
)

print(
    "\nFINAL EXCEL ANALYSIS READY!"
)

print(
    "\nOutput File:",
    output_file
)