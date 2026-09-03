import pandas as pd
import matplotlib.pyplot as plt
import os


# ============================================================
# STEP 1: LOAD RETENTION MATRIX
# ============================================================

input_file = "cohort_retention_matrix.csv"

if not os.path.exists(input_file):

    raise FileNotFoundError(
        f"{input_file} not found. "
        "Please run cohort_clv_analysis.py first."
    )

print("Retention matrix file found successfully.")


retention = pd.read_csv(
    input_file,
    index_col=0
)


print("Retention matrix loaded successfully.")

print(
    "Rows:",
    retention.shape[0]
)

print(
    "Columns:",
    retention.shape[1]
)


# ============================================================
# STEP 2: CLEAN COLUMN NAMES
# ============================================================

retention.columns = [
    str(column)
    for column in retention.columns
]


# ============================================================
# STEP 3: DISPLAY RETENTION MATRIX
# ============================================================

print()
print("=" * 60)
print("RETENTION MATRIX")
print("=" * 60)

print(
    retention.round(2)
)


# ============================================================
# STEP 4: CREATE HEATMAP
# ============================================================

plt.figure(
    figsize=(16, 9)
)


plt.imshow(
    retention,
    aspect="auto",
    interpolation="nearest"
)


plt.colorbar(
    label="Retention %"
)


# ============================================================
# STEP 5: X-AXIS
# ============================================================

plt.xticks(
    range(len(retention.columns)),
    retention.columns,
    rotation=45
)


# ============================================================
# STEP 6: Y-AXIS
# ============================================================

plt.yticks(
    range(len(retention.index)),
    retention.index
)


# ============================================================
# STEP 7: TITLE
# ============================================================

plt.title(
    "Customer Cohort Retention Heatmap",
    fontsize=18
)


plt.xlabel(
    "Months Since First Purchase"
)


plt.ylabel(
    "Customer Cohort Month"
)


# ============================================================
# STEP 8: ADD RETENTION VALUES
# ============================================================

for i in range(
    len(retention.index)
):

    for j in range(
        len(retention.columns)
    ):

        value = retention.iloc[
            i,
            j
        ]

        if pd.notna(value):

            plt.text(
                j,
                i,
                f"{value:.1f}%",
                ha="center",
                va="center",
                fontsize=8
            )


# ============================================================
# STEP 9: SAVE IMAGE
# ============================================================

output_image = (
    "cohort_retention_heatmap.png"
)


plt.tight_layout()


plt.savefig(
    output_image,
    dpi=300,
    bbox_inches="tight"
)


plt.show()


print()
print(
    "Retention heatmap created successfully."
)

print(
    "Output:",
    output_image
)


# ============================================================
# STEP 10: RETENTION INSIGHTS
# ============================================================

print()
print("=" * 60)
print("COHORT RETENTION INSIGHTS")
print("=" * 60)


# Month 1 is normally 100%.
# Therefore we focus on Month 2 onward.

if len(retention.columns) >= 2:

    month_2 = retention.iloc[:, 1]

    month_2_valid = month_2.dropna()


    if len(month_2_valid) > 0:

        average_month_2 = (
            month_2_valid.mean()
        )

        print(
            f"Average Month-2 Retention: "
            f"{average_month_2:.2f}%"
        )


# Find strongest observed retention
# after the first purchase month.

if retention.shape[1] > 1:

    later_retention = retention.iloc[
        :,
        1:
    ]


    max_retention = (
        later_retention
        .stack()
        .max()
    )


    print(
        f"Highest observed retention "
        f"after Month 1: {max_retention:.2f}%"
    )


print()
print("=" * 60)
print("RETENTION VISUALIZATION COMPLETED")
print("=" * 60)