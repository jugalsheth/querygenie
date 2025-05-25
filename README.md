# 🧞‍♂️ QueryGenie — AI SQL Generator & Data Engineering Assistant

[![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-red?logo=streamlit&logoColor=white)](https://streamlit.io/)  
[![OpenAI Powered](https://img.shields.io/badge/Powered%20By-OpenAI-blue?logo=openai&logoColor=white)](https://platform.openai.com/)  
[![MIT License](https://img.shields.io/github/license/jugalsheth/querygenie)](LICENSE)

**QueryGenie** is a smart, AI-powered tool that transforms plain English into optimized SQL queries, conceptual data models (ERDs), and modern ETL pipeline designs.

Perfect for data analysts, engineers, and product teams looking to supercharge their workflow.

---

## 🚀 Features

- 🌟 **Natural Language to SQL**: Describe your data need in plain English.
- 🗂️ **Optional Schema Input**: Improve SQL accuracy by providing table definitions or DDL.
- 🖋️ **Targeted SQL Dialects**: PostgreSQL, MySQL, Snowflake, BigQuery, SQL Server.
- 🧠 **Multiple Output Modes**:
  - SQL Query
  - Data Model (ERD) via Mermaid.js
  - ETL Pipeline Design
- 📊 **Schema Parsing + ERD Visualization**
- 📥 **Download Output as PDF**
- 🧪 **SQL Syntax Check** using [`sqlparse`](https://github.com/andialbrecht/sqlparse)

---

## 🖼️ App Interface

<img width="1512" alt="Screenshot 2025-05-25 at 4 06 42 PM" src="https://github.com/user-attachments/assets/c896727c-eae9-4e91-8540-47a1930387c9" />

---

## ⚙️ Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/jugalsheth/querygenie.git
cd querygenie

2. Set Up Environment
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Add API Key
Create a secrets.toml file in the root directory:

toml
Copy
Edit
OPENAI_API_KEY = "your-openai-api-key-here"

4. Run the App
bash
Copy
Edit
streamlit run querygenie_app.py

📂 Project Structure
bash
Copy
Edit
querygenie/
├── querygenie_app.py        # Main Streamlit App
├── requirements.txt         # Python dependencies
├── secrets.toml             # API keys (not committed)
├── .gitignore
└── assets/
    └── screenshot.png       # App preview image


