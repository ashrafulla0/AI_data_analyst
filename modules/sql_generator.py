import streamlit as st
from modules.ai_engine import ask_ai


def run_sql_generator(df):
    """
    AI SQL Generator
    Generates SQL queries from natural language.
    """

    st.title("🛢️ AI SQL Generator")

    st.write("Generate SQL queries using AI.")

    question = st.text_area(
        "Describe the SQL Query",
        placeholder="Example: Show top 10 customers by sales"
    )

    if st.button("🚀 Generate SQL"):

        if question.strip() == "":
            st.warning("Please enter your question.")
            return

        sample = df.head(20).to_string()

        prompt = f"""
You are an expert SQL Developer.

Dataset Columns:
{list(df.columns)}

Sample Data:
{sample}

User Request:
{question}

Rules:
1. Generate ONLY SQL.
2. Use table name 'data'.
3. Do not explain.
4. No markdown.
5. No ```sql tags.
"""

        sql = ask_ai(
            df_sample=sample,
            question=prompt,
            mode="chat"
        )

        st.subheader("Generated SQL")

        st.code(sql, language="sql")

        st.download_button(
            "⬇ Download SQL",
            data=sql,
            file_name="generated_query.sql",
            mime="text/plain"
        )