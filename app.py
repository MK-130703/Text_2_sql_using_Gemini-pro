from dotenv import load_dotenv
import os
import sqlite3
import streamlit as st
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("GOOGLE_API_KEY not found in environment. Please check your .env file.")
    st.stop()

# Configure the Gemini API
genai.configure(api_key=api_key)

# Function to get SQL from Gemini based on prompt and question
def get_gemini_response(prompt, question):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt + "\n" + question)
        return response.text.strip()
    except Exception as e:
        return f"Error generating SQL: {e}. You may have exceeded the free quota. Please try again later or upgrade your API limits."



# Function to execute SQL query on SQLite DB
def read_sql_query(sql, db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        raise RuntimeError(f"SQL Execution Error: {e}")

# SQL Prompt Setup
prompt = """
You are an expert in converting English questions to SQL query!
The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION.

Example 1 - How many entries of records are present?
→ SELECT COUNT(*) FROM STUDENT;

Example 2 - Tell me all the students studying in section A?
→ SELECT * FROM STUDENT WHERE SECTION='A';

Rules:
- Output should be only the SQL query.
- Do not include ``` or the word "sql" in the response.
"""

# Streamlit App UI
st.set_page_config(page_title="Text-to-SQL Generator")
st.title("🧠 Text-to-SQL using Gemini-Pro")
st.markdown("Enter your natural language question about the STUDENT database:")

# User input
question = st.text_input("💬 Your Question:")

# Submit button
if st.button("Generate SQL and Run"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        sql_query = get_gemini_response(prompt, question)
        st.subheader("🧾 Generated SQL Query")
        st.code(sql_query, language='sql')

        # Execute the query
        try:
            results = read_sql_query(sql_query, "student.db")
            st.subheader("📊 Query Results")
            if results:
                for row in results:
                    st.write(row)
            else:
                st.info("Query executed successfully but returned no results.")
        except Exception as e:
            st.error(str(e))