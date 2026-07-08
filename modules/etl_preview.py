import streamlit as st
import pandas as pd
import re

from modules.preview_engine import PreviewEngine
from modules.session_manager import get_dataset


def run_etl_preview():

    st.title("🧹 AI ETL Preview")
    st.caption("Preview ETL changes before applying them.")

    df = get_dataset()

    if df is None:
        st.warning("⚠ Please upload a dataset first.")
        return

    st.success("✅ Dataset Loaded Successfully")

    st.subheader("📊 Original Dataset")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

    prompt = st.text_area(
        "💬 Describe ETL Operations",
        height=180,
        placeholder="""
Remove duplicates

Fill missing values

Convert dates

Rename Name to Full Name

Drop Salary
"""
    )

    if st.button("🚀 Generate Preview"):

        if prompt.strip() == "":
            st.warning("Please enter ETL instructions.")
            return

        engine = PreviewEngine(df)

        prompt_lower = prompt.lower()

        # ==========================================
        # Remove Duplicates
        # ==========================================

        if "duplicate" in prompt_lower:
            engine.remove_duplicates()

        # ==========================================
        # Fill Missing Values
        # ==========================================

        if "missing" in prompt_lower:
            engine.fill_missing()

        # ==========================================
        # Convert Dates
        # ==========================================

        if "date" in prompt_lower:
            engine.convert_dates()
        # ==========================================
# Split Column
# Example:
# Split Name
# Split Full Name
# ==========================================

        split_match = re.search(
            r"split\s+(.+)",
            prompt,
            flags=re.IGNORECASE
        )
        if split_match:
            column_name = split_match.group(1).strip()
            engine.split_column(column_name)
        
        merge_match = re.search(
            r"merge\s+(.+?)\s+(.+)",
            prompt,
            flags=re.IGNORECASE
        )

        if merge_match:
            col1 = merge_match.group(1).strip()
            col2 = merge_match.group(2).strip()
            engine.merge_columns(col1, col2)
        
        #replacing values==========
        # ---------------------------------
# Replace Values
# Example:
# Replace male with Male
# ---------------------------------

            replace_match = re.search(
                r"replace\s+(.+?)\s+with\s+(.+)",
                prompt,
                flags=re.IGNORECASE
            )

            if replace_match:
                old_value = replace_match.group(1).strip()
                new_value = replace_match.group(2).strip()
                engine.replace_value(
                    old_value,
                    new_value
                )
        # ---------------------------------
        # Change Data Type
        #          # Example:
        # Convert Salary to integer
        # ---------------------------------

        dtype_match = re.search(
            r"convert\s+(.+?)\s+to\s+(integer|int|float|double|string|text|date|datetime)",
            prompt,
            flags=re.IGNORECASE
        )

        if dtype_match:
            column = dtype_match.group(1).strip()
            dtype = dtype_match.group(2).strip()
            engine.change_dtype(
                column,
                dtype
            )
        # ---------------------------------
        # Create Column
        # Example:
        # Create Total = Qty * Price
        # ---------------------------------

        create_match = re.search(
            r"create\s+(.+?)\s*=\s*(.+)",
            prompt,
            flags=re.IGNORECASE
        )

        if create_match:
            new_column = create_match.group(1).strip()
            formula = create_match.group(2).strip()
            engine.create_column(
                new_column,
                formula
            )
# ---------------------------------
# Filter Rows
# Example:
# Filter Salary > 50000
# ---------------------------------

        filter_match = re.search(
            r"filter\s+(.+)",
            prompt,
            flags=re.IGNORECASE
        )

        if filter_match:
            condition = filter_match.group(1).strip()

            engine.filter_rows(condition)


        # ==========================================
        # Rename Column
        # Example:
        # Rename Salary to Monthly Salary
        # ==========================================

        match = re.search(
            r"rename\s+(.+?)\s+to\s+(.+)",
            prompt,
            flags=re.IGNORECASE
        )

        if match:

            old_name = match.group(1).strip()
            new_name = match.group(2).strip()

            engine.rename_column(
                old_name,
                new_name
            )
        # ---------------------------------
        # Group By
        # Examples:
        # Group by Department Sum Salary
        # Group by Product Average Price
        # Group by City Count EmployeeID
        # ---------------------------------

        group_match = re.search(
            r"group\s+by\s+(.+?)\s+(sum|average|avg|mean|count|max|min)\s+(.+)",
            prompt,
            flags=re.IGNORECASE
        )

        if group_match:
            group_column = group_match.group(1).strip()
            operation = group_match.group(2).strip().lower()
            value_column = group_match.group(3).strip()

        # Convert aliases
        if operation == "average":
            operation = "mean"

        if operation == "avg":
            operation = "mean"

        engine.group_by(
            group_column,
            value_column,
            operation
        )
        # ==========================================
        # Drop Column
        # Example:
        # Drop Salary
        # Remove Salary
        # ==========================================

        drop_match = re.search(
            r"(drop|remove)\s+([a-zA-Z0-9_ ]+)",
            prompt,
            flags=re.IGNORECASE
        )

        if drop_match:

            column_name = drop_match.group(2).strip()

            engine.drop_column(column_name)

        # ==========================================
        # Preview Result
        # ==========================================

        result = engine.get_preview()

        st.success("✅ Preview Generated Successfully")

        st.divider()

        st.subheader("✨ Preview Dataset")

        st.dataframe(
            result["preview_df"].head(20),
            use_container_width=True
        )

        st.divider()

        st.subheader("📋 ETL Summary")

        if len(result["summary"]) > 0:

            st.dataframe(
                pd.DataFrame(result["summary"]),
                use_container_width=True
            )

        else:

            st.info("No ETL operations were detected.")

        st.divider()

        stats = result["statistics"]

        st.subheader("📈 Statistics")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Rows",
            stats["rows_after"],
            stats["rows_after"] - stats["rows_before"]
        )

        c2.metric(
            "Missing",
            stats["missing_after"],
            stats["missing_after"] - stats["missing_before"]
        )

        c3.metric(
            "Duplicates",
            stats["duplicates_after"],
            stats["duplicates_after"] - stats["duplicates_before"]
        )

        c4.metric(
            "Columns",
            stats["columns_after"],
            stats["columns_after"] - stats["columns_before"]
        )

        st.divider()

        st.subheader("⬇ Download Preview Dataset")

        csv = result["preview_df"].to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Preview CSV",
            data=csv,
            file_name="preview_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )
