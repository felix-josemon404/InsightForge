# 🏪 Store Analytics AI Assistant

> *An AI-powered assistant that allows users to query retail store databases using natural language.*

This project enables users to **ask questions in plain English** about store data and automatically converts those questions into **SQL queries** using a Large Language Model (LLM).  
The system executes the SQL on a database and returns a **clear, human-readable explanation of the results**.

---

# 📌 Project Overview

Retail store data often requires **SQL knowledge** to extract insights.  
This project removes that barrier by allowing users to interact with the database using **natural language queries**.

Instead of writing SQL like:

```sql
SELECT price FROM products WHERE product_name = 'Whole Milk';

A user can simply ask:

> **"What is the price of whole milk?"**

The AI system will:

- Convert the question into **SQL**
- Execute the SQL query on the **database**
- Retrieve the **results**
- Generate a **natural language explanation**

All of this happens through a **Streamlit web interface**.

---

# 🎯 Objectives

- Enable **natural language querying** of structured databases  
- Automatically generate **SQL queries using LLMs**  
- Provide **human-readable explanations of query results**  
- Build an **AI-powered analytics interface**  
- Demonstrate integration of **LLMs with relational databases**

---

# 🧠 Methodology

The system works through a **multi-stage pipeline**.

---

## 1️⃣ Natural Language → SQL

The user enters a question.  
An LLM converts the question into an **SQL query based on the database schema**.

**Responsible module**

```python
sql_planner.py
