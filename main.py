from fastapi import FastAPI
import sqlite3

app = FastAPI()

# Function to query the database
def query_db(sql_query):
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.get("/")
def home():
    return {"message": "E-commerce AI Agent is running"}

@app.get("/ask")
def ask(question: str):
    # Basic rule-based answers (we will improve this later)
    question_lower = question.lower()

    if "total sales" in question_lower:
        sql = "SELECT SUM(total_sales) FROM product_total_sales_metrics"
        result = query_db(sql)
        return {"answer": f"Your total sales are {result[0][0]}."}

    elif "highest cpc" in question_lower:
        sql = "SELECT product_id, MAX(cpc) FROM product_ad_sales_metrics"
        result = query_db(sql)
        return {"answer": f"The product with highest CPC is {result[0][0]} with CPC {result[0][1]}."}

    elif "roas" in question_lower:  # Return on Ad Spend
        sql = "SELECT SUM(ad_sales)/SUM(ad_spend) FROM product_ad_sales_metrics"
        result = query_db(sql)
        return {"answer": f"Your RoAS (Return on Ad Spend) is {result[0][0]:.2f}."}

    else:
        return {"answer": "Sorry, I don't understand this question yet."}
