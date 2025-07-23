import os
import sqlite3
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse
from dotenv import load_dotenv
import google.generativeai as genai
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()

# Get Gemini API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file. Check your .env file.")

# Configure Gemini
genai.configure(api_key=api_key)

app = FastAPI()
DB_PATH = "ecommerce.db"

# --- Helper: Convert Question to SQL using Gemini ---
def question_to_sql(question: str) -> str:
    # Fallback queries for known questions
    q = question.lower().strip()
    if "total sales" in q:
        return "SELECT SUM(total_sales) AS total_sales FROM product_total_sales_metrics;"
    if "roas" in q or "return on ad spend" in q:
        return "SELECT SUM(ad_sales) / SUM(ad_spend) AS roas FROM product_ad_sales_metrics;"
    if "highest cpc" in q:
        return "SELECT item_id, MAX(ad_spend / NULLIF(clicks, 0)) AS cpc FROM product_ad_sales_metrics;"

    # Ask Gemini for SQL conversion
    prompt = f"""
    Convert the following natural language question into an SQL query 
    for the SQLite database with these tables:
    - product_total_sales_metrics (columns: date, item_id, total_sales, total_units_ordered)
    - product_ad_sales_metrics (columns: date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
    - product_eligibility (columns: eligibility_datetime_utc, item_id, eligibility, message)

    Question: "{question}"
    Only return the SQL query.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip().replace("```sql", "").replace("```", "").strip()

# --- API Endpoint to Ask Questions ---
@app.get("/ask")
def ask(question: str = Query(..., description="Ask a question about sales data")):
    try:
        sql_query = question_to_sql(question)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.close()

        # Format answer for better readability
        answer = ""
        if result:
            if len(result[0]) == 1:
                answer = f"The answer is {result[0][0]}"
            else:
                answer = str(result)
        else:
            answer = "No data found for your query."

        return JSONResponse(content={
            "question": question,
            "sql_query": sql_query,
            "result": result,
            "answer": answer
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

# --- Chart for Total Sales ---
@app.get("/chart/sales")
def chart_sales():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT item_id, SUM(total_sales)
            FROM product_total_sales_metrics
            GROUP BY item_id
            ORDER BY SUM(total_sales) DESC
            LIMIT 10;
        """)
        data = cursor.fetchall()
        conn.close()

        if not data:
            return JSONResponse(content={"error": "No data available."})

        item_ids = [str(row[0]) for row in data]
        sales = [row[1] for row in data]

        plt.figure(figsize=(8, 6))
        plt.bar(item_ids, sales, color="skyblue")
        plt.xlabel("Item ID")
        plt.ylabel("Total Sales")
        plt.title("Top 10 Products by Total Sales")
        plt.tight_layout()

        chart_path = "chart_sales.png"
        plt.savefig(chart_path)
        plt.close()

        return FileResponse(chart_path, media_type="image/png")
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

# --- Chart for Ad Spend ---
@app.get("/chart/ad_spend")
def chart_ad_spend():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT item_id, SUM(ad_spend)
            FROM product_ad_sales_metrics
            GROUP BY item_id
            ORDER BY SUM(ad_spend) DESC
            LIMIT 10;
        """)
        data = cursor.fetchall()
        conn.close()

        if not data:
            return JSONResponse(content={"error": "No data available."})

        item_ids = [str(row[0]) for row in data]
        ad_spend = [row[1] for row in data]

        plt.figure(figsize=(8, 6))
        plt.bar(item_ids, ad_spend, color="lightgreen")
        plt.xlabel("Item ID")
        plt.ylabel("Ad Spend")
        plt.title("Top 10 Products by Ad Spend")
        plt.tight_layout()

        chart_path = "chart_ad_spend.png"
        plt.savefig(chart_path)
        plt.close()

        return FileResponse(chart_path, media_type="image/png")
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
