# AI Analytics Agent

An agentic analytics system that converts plain English questions 
into SQL queries and returns business insights automatically.

## What It Does
- Type any business question in plain English
- AI automatically writes the SQL query
- Runs it against a healthcare dataset with 55,500 patient records
- Returns a clear business insight in seconds

## Demo Questions
- What are the top 3 medical conditions by frequency?
- What is the average billing amount by insurance provider?
- Which hospital has the most patients?
- What is the average age of patients by medical condition?

## Built With
- Groq API (LLaMA 3.3 70B)
- DuckDB
- Python (Pandas)
- Streamlit

## How to Run
1. pip install groq duckdb pandas streamlit python-dotenv
2. Add your Groq API key to .env file
3. py setup_database.py
4. py -m streamlit run app.py

## Results
- 55,500 patient records analyzed
- Natural language to SQL in under 2 seconds
- Cut ad-hoc analysis time from hours to minutes

## Built by
Akhila Vitta | Data Scientist and BI Analyst
akhivitta.lovable.app | linkedin.com/in/akhila-vitta
