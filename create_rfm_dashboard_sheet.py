import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart.label import DataLabelList
from openpyxl.utils import get_column_letter
import os
import shutil


# ============================================================
# STEP 1: FILE PATHS
# ============================================================

input_file = "Retail_ECommerce_Final_With_RFM.xlsx"

output_file = "Retail_ECommerce_Final_RFM_Professional.xlsx"


# ============================================================
# STEP 2: CHECK INPUT FILE
# ============================================================

if not os.path.exists(input_file):

    raise FileNotFoundError(
        f"Input file not found: {input_file}"
    )

print("Input workbook found successfully.")


# ============================================================
# STEP 3: REMOVE OLD OUTPUT
# ============================================================

if os.path.exists(output_file):

    try:

        os.remove(output_file)

        print("Old output file removed successfully.")

    except PermissionError:

        raise PermissionError(
            "Please close the output Excel file before running again."
        )


# ============================================================
# STEP 4: COPY ORIGINAL WORKBOOK
# ============================================================

try:

    shutil.copy2(
        input_file,
        output_file
    )

    print("Original workbook copied successfully.")

except PermissionError:

    raise PermissionError(
        "The input workbook is open. "
        "Please close Excel and run again."
    )


# ============================================================
# STEP 5: OPEN WORKBOOK
# ============================================================

wb = openpyxl.load_workbook(
    output_file
)

print("Workbook opened successfully.")

print(
    "Original sheets:",
    len(wb.sheetnames)
)


# ============================================================
# STEP 6: GET DASHBOARD
# ============================================================

if "Dashboard" not in wb.sheetnames:

    raise ValueError(
        "Dashboard sheet not found."
    )

dashboard = wb["Dashboard"]


# ============================================================
# STEP 7: REMOVE PREVIOUS RFM SECTION FROM MAIN DASHBOARD
# ============================================================

print("Cleaning previous RFM section from Dashboard...")


# Remove cells from row 55 onward
# This removes the RFM table and text we previously added.

for row in range(
    55,
    dashboard.max_row + 1
):

    for col in range(
        1,
        dashboard.max_column + 1
    ):

        dashboard.cell(
            row=row,
            column=col
        ).value = None


# Remove charts positioned around row 55 or below.
#
# openpyxl chart anchors use zero-based row numbers.
# Row 55 in Excel corresponds approximately to anchor row 54.

charts_to_remove = []

for chart in dashboard._charts:

    try:

        chart_row = chart.anchor._from.row

        if chart_row >= 54:

            charts_to_remove.append(chart)

    except Exception:

        pass


for chart in charts_to_remove:

    dashboard._charts.remove(chart)


print(
    "Previous RFM section removed from main Dashboard."
)


# ============================================================
# STEP 8: DELETE OLD RFM DASHBOARD SHEET IF EXISTS
# ============================================================

if "RFM Dashboard" in wb.sheetnames:

    del wb["RFM Dashboard"]

    print(
        "Old RFM Dashboard sheet removed."
    )


# ============================================================
# STEP 9: CREATE NEW RFM DASHBOARD
# ============================================================

rfm_dashboard = wb.create_sheet(
    "RFM Dashboard"
)

print(
    "New RFM Dashboard sheet created."
)


# ============================================================
# STEP 10: READ RFM DATA
# ============================================================

if "RFM Segment Counts" not in wb.sheetnames:

    raise ValueError(
        "RFM Segment Counts sheet not found."
    )


rfm_source = wb[
    "RFM Segment Counts"
]


rfm_data = []


for row in rfm_source.iter_rows(
    min_row=2,
    values_only=True
):

    if (
        row[0] is not None
        and row[1] is not None
    ):

        rfm_data.append(
            (
                row[0],
                row[1]
            )
        )


print(
    "RFM data:",
    rfm_data
)


# ============================================================
# STEP 11: DASHBOARD COLUMN WIDTHS
# ============================================================

column_widths = {

    "A": 20,
    "B": 18,
    "C": 4,
    "D": 18,
    "E": 18,
    "F": 4,
    "G": 18,
    "H": 18

}


for column, width in column_widths.items():

    rfm_dashboard.column_dimensions[
        column
    ].width = width


# ============================================================
# STEP 12: COLORS / STYLES
# ============================================================

title_fill = PatternFill(
    fill_type="solid",
    fgColor="1F4E78"
)


section_fill = PatternFill(
    fill_type="solid",
    fgColor="5B2C83"
)


header_fill = PatternFill(
    fill_type="solid",
    fgColor="1F4E78"
)


white_font = Font(
    color="FFFFFF",
    bold=True
)


title_font = Font(
    color="FFFFFF",
    bold=True,
    size=20
)


section_font = Font(
    color="FFFFFF",
    bold=True,
    size=14
)


normal_font = Font(
    size=11
)


thin_border = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin")
)


# ============================================================
# STEP 13: MAIN TITLE
# ============================================================

rfm_dashboard.merge_cells(
    "A1:H2"
)


title = rfm_dashboard["A1"]


title.value = (
    "CUSTOMER RFM ANALYSIS DASHBOARD"
)


title.fill = title_fill


title.font = title_font


title.alignment = Alignment(
    horizontal="center",
    vertical="center"
)


rfm_dashboard.row_dimensions[1].height = 28
rfm_dashboard.row_dimensions[2].height = 28


# ============================================================
# STEP 14: SUBTITLE
# ============================================================

rfm_dashboard.merge_cells(
    "A3:H3"
)


subtitle = rfm_dashboard["A3"]


subtitle.value = (
    "Customer segmentation using Recency, Frequency and Monetary value"
)


subtitle.font = Font(
    italic=True,
    size=11
)


subtitle.alignment = Alignment(
    horizontal="center"
)


# ============================================================
# STEP 15: SEGMENT COUNTS
# ============================================================

segment_dict = {

    segment: count

    for segment, count in rfm_data

}


champions = segment_dict.get(
    "Champions",
    0
)


loyal = segment_dict.get(
    "Loyal",
    0
)


new_customers = segment_dict.get(
    "New",
    0
)


at_risk = segment_dict.get(
    "At Risk",
    0
)


lost = segment_dict.get(
    "Lost",
    0
)


# ============================================================
# STEP 16: KPI CARDS
# ============================================================

kpis = [

    ("CHAMPIONS", champions),

    ("LOYAL", loyal),

    ("NEW", new_customers),

    ("AT RISK", at_risk),

    ("LOST", lost)

]


kpi_positions = [

    ("A", "B"),
    ("C", "D"),
    ("E", "F"),
    ("G", "H"),
    ("A", "B")

]


# First four cards in row 5
card_ranges = [

    ("A5:B6", "CHAMPIONS", champions),

    ("C5:D6", "LOYAL", loyal),

    ("E5:F6", "NEW", new_customers),

    ("G5:H6", "AT RISK", at_risk)

]


for cell_range, label, value in card_ranges:

    rfm_dashboard.merge_cells(
        cell_range
    )

    first_cell = rfm_dashboard[
        cell_range.split(":")[0]
    ]

    first_cell.value = (
        f"{label}\n{value}"
    )

    first_cell.font = Font(
        bold=True,
        size=14
    )

    first_cell.alignment = Alignment(
        horizontal="center",
        vertical="center",
        wrap_text=True
    )

    first_cell.fill = PatternFill(
        fill_type="solid",
        fgColor="D9EAF7"
    )

    first_cell.border = thin_border


# LOST card row 8
rfm_dashboard.merge_cells(
    "A8:B9"
)


lost_card = rfm_dashboard["A8"]


lost_card.value = (
    f"LOST\n{lost}"
)


lost_card.font = Font(
    bold=True,
    size=14
)


lost_card.alignment = Alignment(
    horizontal="center",
    vertical="center",
    wrap_text=True
)


lost_card.fill = PatternFill(
    fill_type="solid",
    fgColor="EADCF8"
)


lost_card.border = thin_border


# ============================================================
# STEP 17: SECTION TITLE
# ============================================================

rfm_dashboard.merge_cells(
    "A11:H11"
)


section = rfm_dashboard["A11"]


section.value = (
    "RFM SEGMENT DISTRIBUTION"
)


section.fill = section_fill


section.font = section_font


section.alignment = Alignment(
    horizontal="center"
)


# ============================================================
# STEP 18: RFM TABLE
# ============================================================

rfm_dashboard["A13"] = "Segment"
rfm_dashboard["B13"] = "Customers"


for cell in [
    rfm_dashboard["A13"],
    rfm_dashboard["B13"]
]:

    cell.fill = header_fill
    cell.font = white_font
    cell.alignment = Alignment(
        horizontal="center"
    )
    cell.border = thin_border


for index, (
    segment,
    count
) in enumerate(
    rfm_data,
    start=14
):

    rfm_dashboard.cell(
        row=index,
        column=1
    ).value = segment

    rfm_dashboard.cell(
        row=index,
        column=2
    ).value = count


    rfm_dashboard.cell(
        row=index,
        column=1
    ).border = thin_border


    rfm_dashboard.cell(
        row=index,
        column=2
    ).border = thin_border


    rfm_dashboard.cell(
        row=index,
        column=1
    ).alignment = Alignment(
        horizontal="center"
    )


    rfm_dashboard.cell(
        row=index,
        column=2
    ).alignment = Alignment(
        horizontal="center"
    )


# ============================================================
# STEP 19: BAR CHART
# ============================================================

chart = BarChart()


chart.type = "col"


chart.title = (
    "Customers by RFM Segment"
)


chart.y_axis.title = (
    "Number of Customers"
)


chart.x_axis.title = (
    "Customer Segment"
)


chart.height = 8


chart.width = 15


data = Reference(
    rfm_dashboard,
    min_col=2,
    min_row=13,
    max_row=13 + len(rfm_data)
)


categories = Reference(
    rfm_dashboard,
    min_col=1,
    min_row=14,
    max_row=13 + len(rfm_data)
)


chart.add_data(
    data,
    titles_from_data=True
)


chart.set_categories(
    categories
)


chart.dataLabels = DataLabelList()


chart.dataLabels.showVal = True


rfm_dashboard.add_chart(
    chart,
    "D13"
)


# ============================================================
# STEP 20: BUSINESS INSIGHTS
# ============================================================

insight_title_row = 21


rfm_dashboard.merge_cells(
    start_row=insight_title_row,
    start_column=1,
    end_row=insight_title_row,
    end_column=8
)


insight_title = rfm_dashboard.cell(
    row=insight_title_row,
    column=1
)


insight_title.value = (
    "RFM BUSINESS INSIGHTS"
)


insight_title.fill = section_fill


insight_title.font = section_font


insight_title.alignment = Alignment(
    horizontal="center"
)


# ============================================================
# STEP 21: INSIGHT TEXT
# ============================================================

insights = [

    (
        f"• Champions: {champions} customers. "
        "Prioritize retention and premium offers."
    ),

    (
        f"• Loyal: {loyal} customers. "
        "Encourage repeat purchases and cross-selling."
    ),

    (
        f"• New: {new_customers} customers. "
        "Focus on onboarding and second-purchase conversion."
    ),

    (
        f"• At Risk: {at_risk} customers. "
        "Use targeted retention campaigns."
    ),

    (
        f"• Lost: {lost} customers. "
        "Use win-back campaigns to reactivate customers."
    )

]


for index, text in enumerate(
    insights,
    start=23
):

    rfm_dashboard.merge_cells(
        start_row=index,
        start_column=1,
        end_row=index,
        end_column=8
    )


    cell = rfm_dashboard.cell(
        row=index,
        column=1
    )


    cell.value = text


    cell.font = normal_font


    cell.alignment = Alignment(
        wrap_text=True,
        vertical="center"
    )


    rfm_dashboard.row_dimensions[
        index
    ].height = 28


# ============================================================
# STEP 22: METHODOLOGY
# ============================================================

method_row = 30


rfm_dashboard.merge_cells(
    start_row=method_row,
    start_column=1,
    end_row=method_row,
    end_column=8
)


method_title = rfm_dashboard.cell(
    row=method_row,
    column=1
)


method_title.value = (
    "RFM METHODOLOGY"
)


method_title.fill = header_fill


method_title.font = white_font


method_title.alignment = Alignment(
    horizontal="center"
)


# ============================================================
# STEP 23: METHODOLOGY DETAILS
# ============================================================

methodology = [

    "Recency: How recently the customer placed an order.",

    "Frequency: How often the customer placed orders.",

    "Monetary: Total customer revenue generated from orders.",

    "Customers were scored across Recency, Frequency and Monetary dimensions.",

    "Segments: Champions, Loyal, New, At Risk and Lost."

]


for index, text in enumerate(
    methodology,
    start=32
):

    rfm_dashboard.merge_cells(
        start_row=index,
        start_column=1,
        end_row=index,
        end_column=8
    )


    cell = rfm_dashboard.cell(
        row=index,
        column=1
    )


    cell.value = text


    cell.alignment = Alignment(
        wrap_text=True
    )


    rfm_dashboard.row_dimensions[
        index
    ].height = 24


# ============================================================
# STEP 24: FREEZE PANES
# ============================================================

rfm_dashboard.freeze_panes = "A4"


# ============================================================
# STEP 25: PAGE SETTINGS
# ============================================================

rfm_dashboard.sheet_view.showGridLines = False


rfm_dashboard.page_setup.orientation = (
    "landscape"
)


rfm_dashboard.page_setup.fitToWidth = 1


rfm_dashboard.page_setup.fitToHeight = 0


# ============================================================
# STEP 26: MOVE RFM DASHBOARD TO FIRST POSITION
# ============================================================

wb._sheets.remove(
    rfm_dashboard
)

wb._sheets.insert(
    1,
    rfm_dashboard
)


# Dashboard remains first.
# RFM Dashboard becomes second.


# ============================================================
# STEP 27: SAVE
# ============================================================

wb.save(
    output_file
)


# ============================================================
# STEP 28: FINAL VALIDATION
# ============================================================

print()
print("=" * 65)
print("RFM PROFESSIONAL DASHBOARD CREATED SUCCESSFULLY")
print("=" * 65)

print(
    "Output file:",
    output_file
)

print(
    "Total sheets:",
    len(wb.sheetnames)
)

print(
    "Dashboard cleaned:"
    ,
    "YES"
)

print(
    "RFM Dashboard created:"
    ,
    "YES"
)

print(
    "RFM segments:"
    ,
    len(rfm_data)
)

print()
print("RFM Segment Counts:")

for segment, count in rfm_data:

    print(
        f"  {segment}: {count}"
    )

print()
print("Final sheet order:")

for number, sheet in enumerate(
    wb.sheetnames,
    start=1
):

    print(
        number,
        "-",
        sheet
    )

print("=" * 65)