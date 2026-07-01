import os
from dotenv import load_dotenv
from groq import Groq

# ==========================
# Load Environment Variables
# ==========================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found in .env file")

# ==========================
# Create Groq Client
# ==========================

client = Groq(
    api_key=GROQ_API_KEY
)


# ==========================
# AI Engine
# ==========================

def ask_ai(df_sample, question, mode="chat"):

    # -------------------------
    # SQL Generator
    # -------------------------
    if mode == "sql":

        prompt = f"""
You are an SQL Expert.

Dataset:
{df_sample}

User Question:
{question}

Generate only SQL query.

Do not explain.
"""

    # -------------------------
    # Python Generator
    # -------------------------
    elif mode == "python":

        prompt = f"""
You are a Python Data Analyst.

Dataset:
{df_sample}

User Question:
{question}

Generate only Python code.

Do not explain.
"""

    # -------------------------
    # Excel Formula Generator
    # -------------------------
    elif mode == "excel":

        prompt = f"""
You are an Excel Expert.

User Question:
{question}

Return:

1. Formula
2. Explanation
3. Example

Keep answer professional.
"""

    # -------------------------
    # AI Chat
    # -------------------------
    else:

        prompt = f"""
You are a Professional AI Data Analyst.

Dataset:
{df_sample}

Question:
{question}

Answer clearly and professionally.

If a chart is requested,
suggest the best chart type but do not generate code.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content