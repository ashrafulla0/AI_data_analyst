import streamlit as st
import pandas as pd
from io import BytesIO


def run_excel_merger():

    st.title("📚 Merge Excel Files")

    uploaded_files = st.file_uploader(
        "Upload Excel Files",
        type=["xlsx", "xls"],
        accept_multiple_files=True
    )

    if uploaded_files:

        dfs = []

        columns = None

        for file in uploaded_files:

            df = pd.read_excel(file)

            if columns is None:
                columns = list(df.columns)

            else:
                if list(df.columns) != columns:
                    st.error(
                        f"❌ Column mismatch found in {file.name}"
                    )
                    return

            dfs.append(df)

        merged_df = pd.concat(
            dfs,
            ignore_index=True
        )

        st.success(
            f"✅ Successfully merged {len(uploaded_files)} files."
        )

        st.dataframe(
            merged_df,
            use_container_width=True
        )

        buffer = BytesIO()

        with pd.ExcelWriter(
            buffer,
            engine="openpyxl"
        ) as writer:

            merged_df.to_excel(
                writer,
                index=False,
                sheet_name="Merged_Data"
            )

        st.download_button(
            "⬇ Download Merged Excel",
            data=buffer.getvalue(),
            file_name="Merged_Data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )