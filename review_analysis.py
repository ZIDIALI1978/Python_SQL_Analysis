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
# 2. LOAD REVIEWS
# =====================================================

reviews_query = """
SELECT *
FROM Sales.Reviews
"""

reviews = pd.read_sql(
    reviews_query,
    connection
)

print("\n======================================")
print("REVIEWS DATA")
print("======================================")

print(reviews.head())


# =====================================================
# 3. BASIC INFORMATION
# =====================================================

print("\nReviews Shape:")
print(reviews.shape)

print("\nReviews Columns:")
print(reviews.columns.tolist())

print("\nReviews Information:")
print(reviews.info())


# =====================================================
# 4. CHECK MISSING VALUES
# =====================================================

print("\n======================================")
print("MISSING VALUES")
print("======================================")

print(reviews.isnull().sum())


# =====================================================
# 5. RATING ANALYSIS
# =====================================================

reviews["Rating"] = pd.to_numeric(
    reviews["Rating"],
    errors="coerce"
)

average_rating = reviews["Rating"].mean()

print("\n======================================")
print("RATING ANALYSIS")
print("======================================")

print("\nAverage Rating:")
print(average_rating)

print("\nRating Counts:")
print(
    reviews["Rating"].value_counts().sort_index()
)


# =====================================================
# 6. RATING DISTRIBUTION
# =====================================================

rating_counts = (
    reviews["Rating"]
    .value_counts()
    .sort_index()
)

print("\nRating Distribution:")
print(rating_counts)


# =====================================================
# 7. RATING DISTRIBUTION GRAPH
# =====================================================

plt.figure(figsize=(8, 5))

plt.bar(
    rating_counts.index,
    rating_counts.values,
    color="green"
)

plt.xlabel("Rating")
plt.ylabel("Number of Reviews")
plt.title("Rating Distribution")

plt.xticks(
    [1, 2, 3, 4, 5]
)

plt.tight_layout()
plt.show()


# =====================================================
# 8. LOAD PRODUCTS
# =====================================================

products_query = """
SELECT
    ProductID,
    ProductName
FROM Inventory.Products
"""

products = pd.read_sql(
    products_query,
    connection
)


# =====================================================
# 9. AVERAGE RATING BY PRODUCT
# =====================================================

product_ratings = (
    reviews
    .merge(
        products,
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

print("\n======================================")
print("AVERAGE RATING BY PRODUCT")
print("======================================")

print(
    product_ratings.head(10)
)


# =====================================================
# 10. TOP 10 RATED PRODUCTS
# =====================================================

top_rated_products = (
    product_ratings
    .head(10)
)

print("\nTop 10 Rated Products:")
print(top_rated_products)


# =====================================================
# 11. TOP RATED PRODUCTS GRAPH
# =====================================================

top_rated_df = (
    top_rated_products
    .reset_index()
)

plt.figure(figsize=(10, 6))

plt.bar(
    top_rated_df["ProductName"],
    top_rated_df["Rating"],
    color="pink"
)

plt.xlabel("Product")
plt.ylabel("Average Rating")
plt.title("Top 10 Rated Products")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# =====================================================
# 12. LOWEST RATED PRODUCTS
# =====================================================

lowest_rated_products = (
    product_ratings
    .sort_values(
        ascending=True
    )
    .head(10)
)

print("\n======================================")
print("LOWEST RATED PRODUCTS")
print("======================================")

print(lowest_rated_products)


# =====================================================
# 13. REVIEWS OVER TIME
# =====================================================

reviews["ReviewDate"] = pd.to_datetime(
    reviews["ReviewDate"]
)

monthly_reviews = (
    reviews
    .groupby(
        reviews["ReviewDate"].dt.to_period("M")
    )
    .size()
)

print("\n======================================")
print("REVIEWS BY MONTH")
print("======================================")

print(monthly_reviews)


# =====================================================
# 14. REVIEWS OVER TIME GRAPH
# =====================================================

plt.figure(figsize=(10, 6))

plt.plot(
    monthly_reviews.index.astype(str),
    monthly_reviews.values,
    marker="o",
    color="red"
)

plt.xlabel("Month")
plt.ylabel("Number of Reviews")
plt.title("Reviews Over Time")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# =====================================================
# 15. TOTAL REVIEWS
# =====================================================

total_reviews = reviews["ReviewID"].nunique()

print("\n======================================")
print("FINAL REVIEW INSIGHTS")
print("======================================")

print("\nTotal Reviews:")
print(total_reviews)

print("\nAverage Rating:")
print(average_rating)

print("\nMost Common Rating:")
print(
    rating_counts.idxmax()
)

print("\nNumber of Most Common Rating:")
print(
    rating_counts.max()
)

print("\nHighest Rated Product:")

print(
    top_rated_df.iloc[0]
)

print("\nLowest Rated Product:")

print(
    lowest_rated_products.reset_index().iloc[0]
)


# =====================================================
# 16. CLOSE CONNECTION
# =====================================================

connection.close()

print("\nDatabase connection closed!")