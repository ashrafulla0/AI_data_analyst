import json
import pandas as pd
import streamlit as st

from modules.ai_engine import ask_ai
from modules.session_manager import get_dataset


# ==========================================================
# ANALYZE DATASET
# ==========================================================

def analyze_dataset(df):
    """
    Analyze dataset and return a quality report.
    """

    report = {}

    report["rows"] = len(df)
    report["columns"] = len(df.columns)
    report["duplicates"] = int(df.duplicated().sum())
    report["missing"] = int(df.isna().sum().sum())

    report["column_types"] = {
        c: str(df[c].dtype)
        for c in df.columns
    }

    report["missing_by_column"] = (
        df.isna().sum().to_dict()
    )

    report["numeric_columns"] = list(
        df.select_dtypes(include="number").columns
    )

    report["text_columns"] = list(
        df.select_dtypes(include="object").columns
    )

    report["date_columns"] = [
        c for c in df.columns
        if "date" in c.lower()
    ]

    return report


# ==========================================================
# AI RECOMMENDATIONS
# ==========================================================

def get_ai_recommendations(df):
    """
    Uses Groq AI to recommend ETL steps.
    """

    report = analyze_dataset(df)

    prompt = f"""
You are a Senior Data Engineer and Power BI Consultant.

Analyze the dataset summary below.

Recommend the best ETL pipeline before importing into Power BI.

Return ONLY valid JSON.

Dataset Summary:

{json.dumps(report, indent=2)}

Return EXACTLY this JSON format:

{
    "quality_score":90,
    "dataset_type":"Retail Sales",

    "issues":[
        "Missing values in Salary",
        "Duplicate Employee IDs"
    ],

    "recommendations":[
        "Fill missing salary using median",
        "Remove duplicate Employee IDs"
    ],

    "etl_pipeline":[
        "Remove Duplicates",
        "Fill Missing Values",
        "Convert Dates",
        "Rename Columns"
    ],

    "recommended_charts":[
        "Bar Chart",
        "Pie Chart",
        "Line Chart"
    ],

    "business_insights":[
        "Sales are highest in South region",
        "Profit dropped in March"
    ]
}
"""

    response = ask_ai(
        df.head(10).to_string(index=False),
        prompt,
        mode="chat"
    )

    try:

        # Sometimes Groq returns extra text.
        start = response.find("{")
        end = response.rfind("}") + 1

        json_text = response[start:end]

        return json.loads(json_text)

    except Exception:

        return {
            "quality_score": 0,
            "dataset_type": "Unknown",
            "issues": [
                "Unable to parse AI response."
            ],
            "recommendations": []
        }


# ==========================================================
# AI DATA COPILOT PAGE
# ==========================================================

def run_ai_copilot():

    st.title("🚀 AI Data Copilot")
    st.caption("Analyze your dataset and prepare it for Power BI automatically.")

    df = get_dataset()

    if df is None:
        st.warning("Please upload a dataset first.")
        return

    report = analyze_dataset(df)

    st.subheader("📊 Dataset Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", report["rows"])
    c2.metric("Columns", report["columns"])
    c3.metric("Missing", report["missing"])
    c4.metric("Duplicates", report["duplicates"])

    st.divider()

    if st.button(
        "🚀 Analyze Dataset & Prepare for Power BI",
        use_container_width=True
    ):

        with st.spinner("Analyzing dataset..."):

            result = get_ai_recommendations(df)

        st.success("AI Analysis Completed")

        st.subheader("🎯 Dataset Type")
        st.info(result["dataset_type"])

        st.subheader("⭐ Quality Score")
        st.metric(
            "Quality Score",
            f'{result["quality_score"]}%'
        )

        st.divider()

        st.subheader("⚠ Issues Found")

        if result["issues"]:
            for issue in result["issues"]:
                st.warning(issue)
        else:
            st.success("No issues detected.")

        st.divider()

        st.subheader("💡 AI Recommendations")

        if result["recommendations"]:
            for rec in result["recommendations"]:
                st.success(rec)
        else:
            st.info("No recommendations available.")