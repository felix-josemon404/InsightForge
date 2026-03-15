🏪 Store Analytics AI Assistant

An AI-powered analytics assistant for retail store data that allows users to ask natural language questions about store operations and automatically generates SQL queries to retrieve insights from the database.

The system uses Large Language Models (LLMs) to convert user questions into SQL queries, execute them on a PostgreSQL database, and generate human-readable explanations of the results.

📌 Overview

Retail store data often requires SQL knowledge to extract insights. This project removes that barrier by enabling natural language interaction with the database.

Users can ask questions like:

What is the price of whole milk?

What products are available in the store?

What are the top selling items?

The system then:

Converts the question into SQL.

Runs the SQL on the database.

Returns the results.

Generates a clear explanation.

The entire workflow is delivered through an interactive Streamlit web interface.

🎯 Objectives

Enable natural language querying of retail databases

Automatically generate correct SQL queries using LLMs

Provide clear explanations of database results

Build a simple AI analytics interface for non-technical users

Demonstrate integration of LLMs with structured databases

🧠 Methodology

The project follows a three-stage AI pipeline:

1. Natural Language → SQL Generation

The user's question is sent to an LLM which generates the appropriate SQL query.

Module responsible:

sql_planner.py
2. SQL Execution

The generated SQL query is executed on the PostgreSQL database.

Module responsible:

sql_executor.py
3. AI Explanation

The raw database result is converted into a human-friendly explanation.

Module responsible:

llm.py
4. User Interface

The system is deployed using Streamlit, allowing users to interact with the system through a simple web interface.

Module responsible:

app.py
🏗️ System Architecture
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
⚙️ Technologies Used
Technology	Purpose
Python	Backend logic
Streamlit	Web interface
PostgreSQL	Database
Google Generative AI	LLM for SQL generation and explanations
Pandas	Data processing
Scikit-learn	Data handling utilities
PyPDF	Document parsing

Project dependencies include packages such as pandas, numpy, streamlit, google-generativeai, scikit-learn, pypdf, and python-dotenv.

📂 Project Structure
project/
│
├── app.py                # Streamlit frontend
├── sql_planner.py        # Converts questions → SQL
├── sql_executor.py       # Executes SQL queries
├── llm.py                # Generates natural language explanations
├── db.py                 # Database connection
│
├── load_products_insert.sql  # Sample data loader
│
├── requirements.txt
└── README.md
🚀 How to Run the Project
1. Clone the Repository
git clone https://github.com/yourusername/store-ai-assistant.git
cd store-ai-assistant
2. Create Virtual Environment
python -m venv venv
source venv/bin/activate

Windows:

venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Setup Environment Variables

Create a .env file:

GOOGLE_API_KEY=your_api_key
DATABASE_URL=your_database_url
5. Run the Application
streamlit run app.py
💬 Example Queries

Example questions you can ask the system:

What is the price of whole milk?
List all pens in the store.
Show the top selling products.
What products cost more than 5 dollars?
📊 Example Output

The system returns:

Natural language answer

Generated SQL query

Raw database output

Example:

Question:
What is the price of Ballpoint Pen?

Answer:
The product Ballpoint Pen (Blue) has a price of 1.5.
📈 Results

The project successfully demonstrates:

Natural language database querying

Automated SQL generation

AI-generated explanations

Interactive analytics interface

This system makes database analytics accessible to non-technical users.

🎓 Learning Outcomes

Through this project we learned:

Integration of LLMs with structured databases

Prompt engineering for SQL generation

Building AI applications using Streamlit

Designing AI-powered analytics tools

Handling database query execution pipelines

🔮 Future Improvements

Possible extensions:

Voice-based query interface

Advanced analytics and visualizations

Query optimization

Multi-database support

Real-time inventory dashboards
