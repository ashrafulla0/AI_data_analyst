import streamlit as st
import pandas as pd
from io import BytesIO


def run_replace_values():

    st.title("🔄 Replace Values")

    uploaded_file = st.file_uploader(
        "📂 Upload Excel File",
        type=["xlsx", "xls", "csv"]
    )

    if uploaded_file is None:
        return

    # Read file
    # Load file only once
    if "replace_df" not in st.session_state:
        if uploaded_file.name.endswith(".csv"):
            st.session_state.replace_df = pd.read_csv(uploaded_file)
        else:
            st.session_state.replace_df = pd.read_excel(uploaded_file)

    df = st.session_state.replace_df
    st.subheader("👀 Dataset Preview")
    st.dataframe(df, use_container_width=True)

    st.divider()

    # Show Replace button
    if "show_replace" not in st.session_state:
        st.session_state.show_replace = False

    if st.button("🔄 Replace Values"):
        st.session_state.show_replace = True

    if st.session_state.show_replace:

        st.subheader("🔄 Replace Values")

        column = st.selectbox(
            "Select Column",
            df.columns
        )

        old_value = st.text_input(
            "Find Value"
        )

        new_value = st.text_input(
            "Replace With"
        )

        if st.button("✅ Replace"):

            count = (
                df[column]
                .astype(str)
                .eq(old_value)
                .sum()
            )

            df[column] = (
                df[column]
                .astype(str)
                .replace(old_value, new_value)
            )
            st.session_state.replace_df = df

            st.success(f"✅ {count} value(s) replaced successfully.")

            st.subheader("📋 Updated Dataset")

            st.dataframe(
                df,
                use_container_width=True
            )

            output = BytesIO()

            if uploaded_file.name.endswith(".csv"):

                csv = df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    "⬇ Download Updated CSV",
                    csv,
                    file_name="Updated_Data.csv",
                    mime="text/csv"
                )

            else:

                with pd.ExcelWriter(
                    output,
                    engine="openpyxl"
                ) as writer:

                    df.to_excel(
                        writer,
                        index=False
                    )

                st.download_button(
                    "⬇ Download Updated Excel",
                    output.getvalue(),
                    file_name="Updated_Data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )