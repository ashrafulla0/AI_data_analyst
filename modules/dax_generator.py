import streamlit as st

from modules.session_manager import get_dataset
from modules.ai_engine import ask_ai


def run_dax_generator():

    st.title("📊 AI DAX Generator")

    st.caption(
        "Generate Power BI DAX formulas using natural language."
    )

    # ------------------------------------
    # Get Dataset
    # ------------------------------------

    df = get_dataset()

    if df is None:
        st.warning("⚠ Please upload a dataset first.")
        return

    st.success("✅ Dataset Loaded Successfully")

    # ------------------------------------
    # Show Columns
    # ------------------------------------

    st.subheader("📋 Detected Columns")

    st.write(list(df.columns))

    # ------------------------------------
    # User Prompt
    # ------------------------------------

    prompt = st.text_area(
        "💬 Describe the DAX formula you need",
        height=180,
        placeholder="""
Examples:

Calculate Total Sales

Average Salary

Running Total Sales

Profit Margin

Year To Date Sales

Top 10 Customers by Revenue

Rank Products by Sales

Calculate Previous Month Sales

Create a Sales Growth %

Create Customer Count
"""
    )

    # ------------------------------------
    # Generate DAX
    # ------------------------------------

    if st.button("🚀 Generate DAX"):

        if prompt.strip() == "":
            st.warning("Please enter your request.")
            return

        with st.spinner("Generating DAX Formula..."):

            response = ask_ai(
                df.head(20).to_string(index=False),
                prompt,
                mode="dax"
            )

        st.success("✅ DAX Generated Successfully")

        st.subheader("📄 Generated DAX Formula")

        st.code(
            response,
            language="sql"
        )