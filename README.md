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
```

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

- Enable **natural language querying of structured databases**
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
```

---

## 2️⃣ SQL Execution

The generated SQL query is executed against the **PostgreSQL database**.

**Responsible module**

```python
sql_executor.py
```

---

## 3️⃣ AI Explanation Generation

The database results are converted into a **clear natural language explanation** using the LLM.

**Responsible module**

```python
llm.py
```

---

## 4️⃣ User Interface

A **Streamlit interface** allows users to interact with the system easily.

**Responsible module**

```python
app.py
```

---

# 🏗 System Architecture

```
User Question
     │
     ▼
Streamlit Interface
     │
     ▼
LLM SQL Planner
(Natural Language → SQL)
     │
     ▼
PostgreSQL Database
(SQL Execution)
     │
     ▼
LLM Explanation Generator
     │
     ▼
Final Answer Displayed
```

---

# ⚙️ Technologies Used

| Technology | Purpose |
|------------|--------|
| **Python** | Backend logic |
| **Streamlit** | Web application interface |
| **PostgreSQL** | Database |
| **Google Generative AI** | SQL generation and explanation |
| **Pandas** | Data processing |
| **Scikit-learn** | Data utilities |
| **PyPDF** | Document parsing |

---

# 📂 Project Structure

```
project/
│
├── app.py                     # Streamlit application
├── sql_planner.py             # Converts user question → SQL
├── sql_executor.py            # Executes SQL queries
├── llm.py                     # LLM explanation generator
├── db.py                      # Database connection
│
├── load_products_insert.sql   # Sample dataset
│
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/store-ai-assistant.git
cd store-ai-assistant
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

### Mac / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key
DATABASE_URL=your_database_url
```

---

## 5️⃣ Run the Application

```bash
streamlit run app.py
```

---

# 💬 Example Queries

Users can ask questions like:

```
What is the price of whole milk?
List all pens available in the store.
Show all products that cost more than 5.
What products are in the store?
```

---

# 📊 Example Output

### User Question

> What is the price of Ballpoint Pen?

### System Response

```
The product Ballpoint Pen (Blue) has a price of 1.5.
```

---

# 📈 Results

This project demonstrates how **LLMs can interact with structured databases** to provide insights **without requiring users to write SQL queries**.

The system successfully:

- Converts **natural language into SQL**
- Executes **queries on a database**
- Generates **clear explanations**
- Provides an **interactive analytics interface**

---

# 🎓 Learning Outcomes

Through this project we learned:

- Integration of **LLMs with relational databases**
- Prompt engineering for **SQL generation**
- Building AI applications using **Streamlit**
- Creating **AI-powered analytics tools**
- Designing **modular AI pipelines**

---

# 🔮 Future Improvements

Possible future enhancements include:

- Voice-based query interface
- Data visualization dashboards
- Query optimization
- Multi-database support
- Real-time inventory analytics

---

# 👨‍💻 Author

**Felix Josemon**

Final Year Project  
Artificial Intelligence / Machine Learning
