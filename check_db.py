import sqlite3

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# Check columns of product_total_sales_metrics
cursor.execute("PRAGMA table_info(product_total_sales_metrics);")
print("Columns in product_total_sales_metrics:")
print(cursor.fetchall())

# Check columns of product_ad_sales_metrics
cursor.execute("PRAGMA table_info(product_ad_sales_metrics);")
print("\nColumns in product_ad_sales_metrics:")
print(cursor.fetchall())

# Check columns of product_eligibility
cursor.execute("PRAGMA table_info(product_eligibility);")
print("\nColumns in product_eligibility:")
print(cursor.fetchall())

conn.close()
