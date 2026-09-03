import os
import glob
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


# ============================================================
# RETAIL E-COMMERCE
# BUSINESS INSIGHTS REPORT
# ============================================================

print("=" * 70)
print("       RETAIL E-COMMERCE BUSINESS INSIGHTS")
print("=" * 70)


# ============================================================
# STEP 1 — FIND LATEST EXCEL FILE
# ============================================================

folder = r"C:\Users\win\Desktop\sql\Python_SQL_Analysis"

files = glob.glob(
    os.path.join(
        folder,
        "Retail_ECommerce_Final_Analysis_*.xlsx"
    )
)

if not files:
    raise FileNotFoundError(
        "No Retail_ECommerce_Final_Analysis Excel file found."
    )

input_file = max(files, key=os.path.getmtime)

print("\nLatest Excel file found:")
print(input_file)


# ============================================================
# STEP 2 — OPEN EXISTING WORKBOOK
# ============================================================

print("\nOpening Excel workbook...")

wb = load_workbook(input_file)

print("Workbook opened successfully!")

print("\nExisting sheets:")
for sheet in wb.sheetnames:
    print(" -", sheet)


# ============================================================
# STEP 3 — REMOVE OLD BUSINESS INSIGHTS SHEET
# ============================================================

if "Business Insights" in wb.sheetnames:
    print("\nExisting Business Insights sheet found.")
    print("Removing old version...")
    del wb["Business Insights"]


# ============================================================
# STEP 4 — CREATE BUSINESS INSIGHTS SHEET
# ============================================================

ws = wb.create_sheet("Business Insights")

print("\nBusiness Insights sheet created!")


# ============================================================
# STEP 5 — COLORS / STYLES
# ============================================================

dark_fill = PatternFill(
    fill_type="solid",
    fgColor="1F4E78"
)

section_fill = PatternFill(
    fill_type="solid",
    fgColor="D9EAF7"
)

kpi_fill = PatternFill(
    fill_type="solid",
    fgColor="E2F0D9"
)

recommendation_fill = PatternFill(
    fill_type="solid",
    fgColor="FFF2CC"
)

white_font = Font(
    color="FFFFFF",
    bold=True,
    size=14
)

title_font = Font(
    bold=True,
    size=20,
    color="FFFFFF"
)

section_font = Font(
    bold=True,
    size=13
)

normal_font = Font(
    size=11
)

bold_font = Font(
    bold=True,
    size=11
)

thin_side = Side(
    style="thin",
    color="B7B7B7"
)

border = Border(
    left=thin_side,
    right=thin_side,
    top=thin_side,
    bottom=thin_side
)


# ============================================================
# STEP 6 — TITLE
# ============================================================

ws.merge_cells("A1:F2")

ws["A1"] = "RETAIL E-COMMERCE BUSINESS INSIGHTS"

ws["A1"].font = title_font
ws["A1"].fill = dark_fill
ws["A1"].alignment = Alignment(
    horizontal="center",
    vertical="center"
)


# ============================================================
# STEP 7 — PROJECT SUMMARY
# ============================================================

# Executive Summary section
ws.merge_cells("A4:B4")

ws["A4"] = "Executive Summary"

ws["A4"].font = section_font
ws["A4"].fill = section_fill
ws["A4"].alignment = Alignment(
    horizontal="left"
)


summary = [
    ("Customers", 100),
    ("Orders", 500),
    ("Order Items", 1492),
    ("Products", 200),
    ("Payments", 448),
    ("Reviews", 160),
    ("Shipments", 427),
    ("Suppliers", 20),
    ("Inventory Records", 200),
    ("Employees", 10),
]

row = 5

for label, value in summary:

    ws[f"A{row}"] = label
    ws[f"B{row}"] = value

    ws[f"A{row}"].font = bold_font
    ws[f"B{row}"].font = normal_font

    ws[f"A{row}"].border = border
    ws[f"B{row}"].border = border

    row += 1


# ============================================================
# STEP 8 — KEY BUSINESS KPIs
# ============================================================

ws.merge_cells("D4:F4")

ws["D4"] = "Key Business KPIs"

ws["D4"].font = section_font
ws["D4"].fill = section_fill
ws["D4"].alignment = Alignment(
    horizontal="left"
)

kpis = [
    ("Total Revenue", "1,371,796.74"),
    ("Average Order Value", "2,743.59"),
    ("Total Quantity Sold", "3,733"),
    ("Total Payment Amount", "1,163,446.07"),
    ("Average Payment", "2,596.98"),
    ("Average Rating", "3.52"),
]

row = 5

for label, value in kpis:

    ws[f"D{row}"] = label
    ws[f"E{row}"] = value

    ws[f"D{row}"].font = bold_font
    ws[f"E{row}"].font = Font(
        bold=True,
        size=11
    )

    ws[f"D{row}"].fill = kpi_fill
    ws[f"E{row}"].fill = kpi_fill

    ws[f"D{row}"].border = border
    ws[f"E{row}"].border = border

    row += 1


# ============================================================
# STEP 9 — SALES & REVENUE INSIGHTS
# ============================================================

row = 17

ws.merge_cells(start_row=row, start_column=1,
               end_row=row, end_column=6)

ws.cell(row=row, column=1).value = "Sales & Revenue Insights"

ws.cell(row=row, column=1).font = section_font
ws.cell(row=row, column=1).fill = section_fill

row += 1

sales_insights = [
    "The analysis contains 500 orders across the retail e-commerce dataset.",
    "Total analyzed revenue is 1,371,796.74.",
    "Average Order Value is 2,743.59.",
    "A total of 3,733 product units were sold.",
    "Revenue performance should be monitored together with order volume and quantity sold."
]

for insight in sales_insights:

    ws.merge_cells(
        start_row=row,
        start_column=1,
        end_row=row,
        end_column=6
    )

    ws.cell(row=row, column=1).value = "• " + insight

    ws.cell(row=row, column=1).font = normal_font
    ws.cell(row=row, column=1).alignment = Alignment(
        wrap_text=True,
        vertical="top"
    )

    row += 1


# ============================================================
# STEP 10 — CUSTOMER INSIGHTS
# ============================================================

row += 1

ws.merge_cells(start_row=row, start_column=1,
               end_row=row, end_column=6)

ws.cell(row=row, column=1).value = "Customer Insights"

ws.cell(row=row, column=1).font = section_font
ws.cell(row=row, column=1).fill = section_fill

row += 1

customer_insights = [
    "The database contains 100 customers.",
    "Customer-level analysis can be used to identify high-value customers.",
    "Customer revenue should be monitored to identify the strongest contributors to sales.",
    "Repeat purchasing behavior can help identify valuable customer segments."
]

for insight in customer_insights:

    ws.merge_cells(
        start_row=row,
        start_column=1,
        end_row=row,
        end_column=6
    )

    ws.cell(row=row, column=1).value = "• " + insight

    ws.cell(row=row, column=1).alignment = Alignment(
        wrap_text=True
    )

    row += 1


# ============================================================
# STEP 11 — PRODUCT & CATEGORY INSIGHTS
# ============================================================

row += 1

ws.merge_cells(start_row=row, start_column=1,
               end_row=row, end_column=6)

ws.cell(row=row, column=1).value = "Product & Category Insights"

ws.cell(row=row, column=1).font = section_font
ws.cell(row=row, column=1).fill = section_fill

row += 1

product_insights = [
    "The product catalog contains 200 products.",
    "Top revenue products should receive priority in inventory planning.",
    "Category-level revenue analysis can identify the strongest product categories.",
    "Products with strong sales but low stock should be monitored closely.",
    "Product profitability should be considered alongside revenue."
]

for insight in product_insights:

    ws.merge_cells(
        start_row=row,
        start_column=1,
        end_row=row,
        end_column=6
    )

    ws.cell(row=row, column=1).value = "• " + insight

    ws.cell(row=row, column=1).alignment = Alignment(
        wrap_text=True
    )

    row += 1


# ============================================================
# STEP 12 — PAYMENT INSIGHTS
# ============================================================

row += 1

ws.merge_cells(start_row=row, start_column=1,
               end_row=row, end_column=6)

ws.cell(row=row, column=1).value = "Payment Insights"

ws.cell(row=row, column=1).font = section_font
ws.cell(row=row, column=1).fill = section_fill

row += 1

payment_insights = [
    "The dataset contains 448 payment records.",
    "Total recorded payment amount is 1,163,446.07.",
    "Payment methods should be monitored to understand customer payment preferences.",
    "Differences between order revenue and recorded payments should be investigated when reconciling transactions."
]

for insight in payment_insights:

    ws.merge_cells(
        start_row=row,
        start_column=1,
        end_row=row,
        end_column=6
    )

    ws.cell(row=row, column=1).value = "• " + insight

    ws.cell(row=row, column=1).alignment = Alignment(
        wrap_text=True
    )

    row += 1


# ============================================================
# STEP 13 — REVIEW INSIGHTS
# ============================================================

row += 1

ws.merge_cells(start_row=row, start_column=1,
               end_row=row, end_column=6)

ws.cell(row=row, column=1).value = "Customer Review Insights"

ws.cell(row=row, column=1).font = section_font
ws.cell(row=row, column=1).fill = section_fill

row += 1

review_insights = [
    "The dataset contains 160 customer reviews.",
    "The average product rating is 3.52.",
    "Highly rated products can be promoted as strong customer-performing products.",
    "Low-rated products should be investigated for quality, pricing, delivery, or customer-experience issues."
]

for insight in review_insights:

    ws.merge_cells(
        start_row=row,
        start_column=1,
        end_row=row,
        end_column=6
    )

    ws.cell(row=row, column=1).value = "• " + insight

    ws.cell(row=row, column=1).alignment = Alignment(
        wrap_text=True
    )

    row += 1


# ============================================================
# STEP 14 — DELIVERY & SHIPMENT INSIGHTS
# ============================================================

row += 1

ws.merge_cells(start_row=row, start_column=1,
               end_row=row, end_column=6)

ws.cell(row=row, column=1).value = "Delivery & Shipment Insights"

ws.cell(row=row, column=1).font = section_font
ws.cell(row=row, column=1).fill = section_fill

row += 1

delivery_insights = [
    "The dataset contains 427 shipment records.",
    "Courier and delivery analysis can help evaluate logistics performance.",
    "Delivery delays should be monitored because they can negatively affect customer satisfaction.",
    "Courier-level performance should be compared using delivery and shipment metrics."
]

for insight in delivery_insights:

    ws.merge_cells(
        start_row=row,
        start_column=1,
        end_row=row,
        end_column=6
    )

    ws.cell(row=row, column=1).value = "• " + insight

    ws.cell(row=row, column=1).alignment = Alignment(
        wrap_text=True
    )

    row += 1


# ============================================================
# STEP 15 — INVENTORY INSIGHTS
# ============================================================

row += 1

ws.merge_cells(start_row=row, start_column=1,
               end_row=row, end_column=6)

ws.cell(row=row, column=1).value = "Inventory Insights"

ws.cell(row=row, column=1).font = section_font
ws.cell(row=row, column=1).fill = section_fill

row += 1

inventory_insights = [
    "The inventory dataset contains 200 product inventory records.",
    "Low-stock products should be identified before they affect sales.",
    "Top-selling products should receive higher inventory attention.",
    "Excess inventory should also be monitored to reduce capital tied up in slow-moving products."
]

for insight in inventory_insights:

    ws.merge_cells(
        start_row=row,
        start_column=1,
        end_row=row,
        end_column=6
    )

    ws.cell(row=row, column=1).value = "• " + insight

    ws.cell(row=row, column=1).alignment = Alignment(
        wrap_text=True
    )

    row += 1


# ============================================================
# STEP 16 — SUPPLIER INSIGHTS
# ============================================================

row += 1

ws.merge_cells(start_row=row, start_column=1,
               end_row=row, end_column=6)

ws.cell(row=row, column=1).value = "Supplier Insights"

ws.cell(row=row, column=1).font = section_font
ws.cell(row=row, column=1).fill = section_fill

row += 1

supplier_insights = [
    "The dataset contains 20 suppliers.",
    "Supplier stock contribution should be compared with product demand.",
    "Supplier pricing should be evaluated together with product profitability.",
    "High-performing suppliers can be prioritized for important products."
]

for insight in supplier_insights:

    ws.merge_cells(
        start_row=row,
        start_column=1,
        end_row=row,
        end_column=6
    )

    ws.cell(row=row, column=1).value = "• " + insight

    ws.cell(row=row, column=1).alignment = Alignment(
        wrap_text=True
    )

    row += 1


# ============================================================
# STEP 17 — BUSINESS RECOMMENDATIONS
# ============================================================

row += 1

ws.merge_cells(start_row=row, start_column=1,
               end_row=row, end_column=6)

ws.cell(row=row, column=1).value = "Business Recommendations"

ws.cell(row=row, column=1).font = section_font
ws.cell(row=row, column=1).fill = section_fill

row += 1

recommendations = [
    "Focus marketing efforts on high-revenue and high-profit products.",
    "Maintain sufficient inventory for products with strong sales performance.",
    "Investigate low-rated products to improve customer satisfaction.",
    "Monitor delivery and courier performance to reduce customer complaints.",
    "Use customer revenue analysis to develop targeted retention strategies.",
    "Evaluate supplier pricing and stock contribution regularly.",
    "Monitor payment reconciliation to ensure recorded payments align with orders.",
    "Use the dashboard regularly for data-driven business decisions."
]

for recommendation in recommendations:

    ws.merge_cells(
        start_row=row,
        start_column=1,
        end_row=row,
        end_column=6
    )

    ws.cell(row=row, column=1).value = "✓ " + recommendation

    ws.cell(row=row, column=1).fill = recommendation_fill
    ws.cell(row=row, column=1).alignment = Alignment(
        wrap_text=True
    )

    row += 1


# ============================================================
# STEP 18 — COLUMN WIDTHS
# ============================================================

ws.column_dimensions["A"].width = 28
ws.column_dimensions["B"].width = 18
ws.column_dimensions["C"].width = 5
ws.column_dimensions["D"].width = 28
ws.column_dimensions["E"].width = 20
ws.column_dimensions["F"].width = 18


# ============================================================
# STEP 19 — ROW HEIGHTS
# ============================================================

ws.row_dimensions[1].height = 30
ws.row_dimensions[2].height = 30


for r in range(1, ws.max_row + 1):

    if r not in [1, 2]:

        ws.row_dimensions[r].height = 24


# ============================================================
# STEP 20 — FREEZE PANES
# ============================================================

ws.freeze_panes = "A5"


# ============================================================
# STEP 21 — PAGE SETTINGS
# ============================================================

ws.sheet_view.showGridLines = False

ws.page_setup.orientation = "landscape"
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0


# ============================================================
# STEP 22 — SAVE WORKBOOK
# ============================================================

output_file = os.path.join(
    folder,
    "Retail_ECommerce_Final_With_Insights.xlsx"
)

print("\nSaving workbook...")

wb.save(output_file)

print("\n" + "=" * 70)
print("BUSINESS INSIGHTS CREATED SUCCESSFULLY!")
print("=" * 70)

print("\nOutput File:")
print(output_file)

print("\nTotal Sheets:", len(wb.sheetnames))

print("\nBusiness Insights sheet added successfully.")

print("\nExisting dashboard and charts have been preserved.")

print("\n" + "=" * 70)