import streamlit as st
from agent import analyze, get_schema, conn

st.set_page_config(
    page_title="AI Analytics Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Healthcare Analytics Agent")
st.subheader("Ask any question about patient data in plain English")

with st.sidebar:
    st.header("Dataset Info")
    try:
        count = conn.execute("SELECT COUNT(*) FROM main_data").fetchone()[0]
        st.metric("Total Patients", f"{count:,}")
        st.subheader("Available Columns")
        st.code(get_schema())
    except:
        st.write("Loading...")

st.write("**Try these questions:**")
col1, col2 = st.columns(2)
examples = [
    "What are the top 3 medical conditions?",
    "What is the average billing amount?",
    "Which hospital has the most patients?",
    "What is the most common medication prescribed?",
    "How many patients were admitted urgently?",
    "What is the average age by medical condition?"
]
for i, ex in enumerate(examples):
    if i % 2 == 0:
        if col1.button(ex, key=f"btn_{i}"):
            st.session_state.question = ex
    else:
        if col2.button(ex, key=f"btn_{i}"):
            st.session_state.question = ex

question = st.text_input(
    "Your question:",
    value=st.session_state.get("question", ""),
    placeholder="What insights do you need from the patient data?"
)

if st.button("Analyze", type="primary") and question:
    with st.spinner("Analyzing..."):
        col_left, col_right = st.columns([1, 1])
        with col_left:
            st.subheader("Business Insight")
            insight = analyze(question)
            if insight:
                st.success(insight)
        with col_right:
            st.subheader("Data Table")
            try:
                from groq import Groq
                import os
                from dotenv import load_dotenv
                load_dotenv()
                c = Groq(api_key=os.getenv("GROQ_API_KEY"))
                schema = get_schema()
                r = c.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    max_tokens=300,
                    messages=[{"role":"user","content":f"Table: main_data\nColumns:\n{schema}\nSQL only for: {question}"}]
                )
                sql = r.choices[0].message.content.strip().replace("```sql","").replace("```","").strip()
                _, df = __import__('agent').run_sql(sql)
                if df is not None:
                    st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.write("Table loading...")

st.divider()
st.caption("Built by Akhila Vitta | AI Analytics Agent | akhivitta.lovable.app")