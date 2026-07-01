"""
AI Chat Module (Advanced)
AI Data Analyst Pro

Now supports real pandas execution
"""

import pandas as pd


# ==========================
# AI ANALYSIS ENGINE
# ==========================

def analyze_question(df: pd.DataFrame, question: str):

    q = question.lower()

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    # ==========================
    # AVERAGE
    # ==========================
    if "average" in q or "mean" in q:

        for col in numeric_cols:
            if col in q:
                return f"📊 Average of {col}: {df[col].mean():.2f}"

        if numeric_cols:
            col = numeric_cols[0]
            return f"📊 Average of {col}: {df[col].mean():.2f}"

    # ==========================
    # SUM
    # ==========================
    if "sum" in q or "total" in q:

        for col in numeric_cols:
            if col in q:
                return f"➕ Total of {col}: {df[col].sum():.2f}"

    # ==========================
    # MAX
    # ==========================
    if "max" in q or "highest" in q:

        for col in numeric_cols:
            if col in q:
                return f"📈 Max of {col}: {df[col].max()}"

    # ==========================
    # MIN
    # ==========================
    if "min" in q or "lowest" in q:

        for col in numeric_cols:
            if col in q:
                return f"📉 Min of {col}: {df[col].min()}"

    # ==========================
    # COUNT ROWS
    # ==========================
    if "how many" in q or "rows" in q or "count" in q:

        return f"📦 Total rows: {len(df)}"

    # ==========================
    # UNIQUE VALUES
    # ==========================
    if "unique" in q:

        for col in df.columns:
            if col in q:
                return f"🔢 Unique values in {col}: {df[col].nunique()}"

    # ==========================
    # TOP VALUES (VERY USEFUL)
    # ==========================
    if "top" in q:

        for col in df.columns:
            if col in q:
                top_values = df[col].value_counts().head(5)
                return f"🏆 Top values in {col}:\n{top_values}"

    # ==========================
    # DEFAULT RESPONSE
    # ==========================
    return """
🤖 I could not fully understand your question.

Try asking like:
- average sales
- total revenue
- max profit
- how many rows
- top customers
"""