import streamlit as st
from openai import OpenAI
from datetime import datetime
import pandas as pd
from fpdf import FPDF
import random
import io
import re

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="QueryGenie — AI SQL Generator", layout="wide")

st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
            background-color: #0f111a;
            color: #e0e0e0;
        }
        .stTextInput>div>div>input, .stTextArea textarea {
            background-color: #1f222e;
            color: white;
            border: 1px solid #333;
            border-radius: 6px;
        }
        .stButton>button {
            background-color: #007acc;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
        }
        .stMarkdown code {
            background-color: #1a1c25;
            color: #00ffae;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🧞 QueryGenie — AI SQL Generator & Data Engineering Assistant")
st.caption("Generate SQL, ERDs, ETL pipelines, visualize schemas, and validate SQL from natural language.")

st.markdown("---")

st.subheader("🔍 Describe Your Use Case")
user_input = st.text_area("Example: Show me active users who signed up in the last 7 days", height=100)

st.subheader("🗃️ (Optional) Paste Your Schema")
schema_input = st.text_area("Paste your table schema or DDL to enhance SQL accuracy", height=150)

col1, col2, col3 = st.columns(3)

with col1:
    db_type = st.selectbox("Target SQL Dialect", ["PostgreSQL", "Snowflake", "MySQL", "BigQuery", "SQL Server"])

with col2:
    explanation_level = st.selectbox("Explanation Detail", ["Short", "Detailed"])

with col3:
    action = st.selectbox("🧠 What to Generate", ["SQL Query", "Data Model (ERD)", "ETL Design"])

# --- Smart Schema Viewer ---
def extract_table_names(schema):
    return re.findall(r'CREATE TABLE (\w+)', schema, re.IGNORECASE)

def extract_columns(schema):
    tables = {}
    blocks = re.findall(r'CREATE TABLE (\w+) \((.*?)\);', schema, re.DOTALL | re.IGNORECASE)
    for table, cols in blocks:
        tables[table] = [line.strip().split()[0] for line in cols.strip().split(',') if line.strip()]
    return tables

if schema_input:
    with st.expander("🧾 Parsed Schema Preview"):
        tables = extract_columns(schema_input)
        for tname, columns in tables.items():
            st.markdown(f"**{tname}**")
            st.code("\n".join(columns))

        mermaid_code = "graph TD\n"
        for tname, columns in tables.items():
            mermaid_code += f"{tname}[{tname}]\n"
            for col in columns:
                mermaid_code += f"{tname} --> {tname}_{col}[{col}]\n"

        st.markdown("### 📊 ERD Diagram (Conceptual)")
        st.markdown(f"```mermaid\n{mermaid_code}```")

# --- Output Generation ---
if st.button("✨ Generate Output"):
    with st.spinner("Thinking deeply about your data..."):
        # Build prompt based on action
        if action == "SQL Query":
            prompt = f"""
            You are a helpful data engineer. Based on the input request and schema, generate an optimized {db_type} SQL query.
            Add a {explanation_level.lower()} explanation underneath.

            Request: {user_input}
            Schema:
            {schema_input if schema_input else 'No schema provided.'}
            """
        elif action == "Data Model (ERD)":
            prompt = f"""
            Design a logical ERD model from the scenario below. Include entities, primary keys, foreign keys, and relationships.

            Scenario: {user_input}
            """
        elif action == "ETL Design":
            prompt = f"""
            Given the following use case, design an ETL pipeline with best-practice stages, validation checks, and modern tooling.

            Use Case: {user_input}
            """

        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a senior data engineer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )

        result = response.choices[0].message.content

        st.markdown("---")
        st.subheader("📄 Generated Output")
        st.code(result)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in result.split('\n'):
            pdf.multi_cell(0, 10, line)

        # Export to binary string
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        pdf_output = io.BytesIO(pdf_bytes)

        st.download_button(
        label="📥 Download as PDF",
        file_name=f"QueryGenie_{action.replace(' ', '_')}.pdf",
        mime="application/pdf",
        data=pdf_output,
        key=f"download_{action.replace(' ', '_').lower()}"
)

        st.download_button(
            label="📥 Download as PDF",
            file_name=f"QueryGenie_{action.replace(' ', '_')}.pdf",
            mime="application/pdf",
            data=pdf_output
        )

        # SQL Syntax Check
        if action == "SQL Query" and result.lower().startswith("select"):
            st.subheader("🧪 Real-time SQL Check")
            try:
                import sqlparse
                parsed = sqlparse.parse(result)
                if parsed:
                    st.success("✅ SQL syntax appears valid.")
                else:
                    st.warning("⚠️ Could not validate SQL. Please double-check manually.")
            except Exception as e:
                st.error(f"Error parsing SQL: {e}")

st.markdown("""
---
✅ Built with Streamlit + OpenAI | v3.1  
🧠 Now with ERD visualization + SQL syntax check  
👨‍💻 Author: [@jugalsheth](https://github.com/jugalsheth)
""")
