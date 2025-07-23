# E-commerce AI Agent

This project is an **AI-powered agent** that answers questions related to e-commerce data using natural language queries.  
It uses **Google Gemini (LLM)** to convert questions into SQL queries, fetches data from **SQLite**, and returns meaningful answers via a **FastAPI-based API**.

---

## **Features**
- Answer natural language questions like:
  - *"What is my total sales?"*
  - *"Calculate the RoAS (Return on Ad Spend)."*
  - *"Which product had the highest CPC (Cost Per Click)?"*
- REST API with FastAPI.
- Auto-generated SQL queries using Google Gemini.
- Visual charts (bar graphs for top products).
- Extensible design for additional questions and datasets.

---

## **Datasets**
The following datasets are included and imported into the SQLite database (`ecommerce.db`):
1. **Product-Level Ad Sales and Metrics** (`Product-Level Ad Sales and Metrics.csv`)
2. **Product-Level Total Sales and Metrics** (`Product-Level Total Sales and Metrics.csv`)
3. **Product-Level Eligibility Table** (`Product-Level Eligibility Table.csv`)

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/karichetipravallika/ecommerce_ai_agent.git
cd ecommerce_ai_agent
