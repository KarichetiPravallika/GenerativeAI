import sqlite3
import pandas as pd

# Load your CSV files (replace with correct filenames)
ad_sales = pd.read_csv("Product-Level Ad Sales and Metrics.csv")
total_sales = pd.read_csv("Product-Level Total Sales and Metrics.csv")
eligibility = pd.read_csv("Product-Level Eligibility Table.csv")

# Create SQLite database
conn = sqlite3.connect("ecommerce.db")

# Store each dataset into its own table
ad_sales.to_sql("product_ad_sales_metrics", conn, if_exists="replace", index=False)
total_sales.to_sql("product_total_sales_metrics", conn, if_exists="replace", index=False)
eligibility.to_sql("product_eligibility", conn, if_exists="replace", index=False)

conn.close()
print("Database ecommerce.db created successfully!")
