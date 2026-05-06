from groq import Groq
import duckdb
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
conn = duckdb.connect('data.db')

def get_schema():
    try:
        result = conn.execute("DESCRIBE main_data").df()
        columns = []
        for _, row in result.iterrows():
            columns.append(f"{row['column_name']} ({row['column_type']})")
        return "\n".join(columns)
    except:
        return "Table: main_data"

def run_sql(query):
    try:
        query = query.strip().replace("```sql","").replace("```","").strip()
        result = conn.execute(query).df()
        return result.to_string(index=False), result
    except Exception as e:
        return f"Error: {str(e)}", None

def analyze(question):
    schema = get_schema()
    print(f"\nQuestion: {question}")
    print("Thinking...")

    sql_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""You are a SQL expert working with DuckDB.
Table name: main_data
Columns:
{schema}

Write a SQL query to answer: "{question}"
Return ONLY the SQL query. No explanation. No markdown."""
        }]
    )

    sql_query = sql_response.choices[0].message.content.strip()
    print(f"\nSQL Generated:\n{sql_query}")

    data_text, data_df = run_sql(sql_query)

    if "Error" in data_text:
        print(f"Error: {data_text}")
        return None

    print(f"\nData:\n{data_text}")

    insight_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": f"""You are a senior data analyst.
Question: "{question}"
Data:
{data_text}

Give a 2 sentence business insight.
Start with the key number. End with one recommendation."""
        }]
    )

    insight = insight_response.choices[0].message.content
    print(f"\nInsight:\n{insight}")
    return insight

if __name__ == "__main__":
    print("AI Analytics Agent Ready")
    print("=" * 50)
    questions = [
        "How many patients are in the dataset?",
        "What are the top 3 medical conditions by frequency?",
        "What is the average age of patients?",
        "Which blood type is most common?"
    ]
    for q in questions:
        analyze(q)
        print("=" * 50)