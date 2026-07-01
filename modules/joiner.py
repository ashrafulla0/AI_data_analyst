import pandas as pd
import streamlit as st


def join_datasets(df1, df2):

    common = list(set(df1.columns).intersection(df2.columns))

    if len(common) == 0:
        st.error("No common columns found.")
        return None

    key = st.selectbox("Join Column", common)

    how = st.selectbox(
        "Join Type",
        ["inner", "left", "right", "outer"]
    )

    if st.button("Join Datasets"):

        joined = pd.merge(
            df1,
            df2,
            on=key,
            how=how
        )

        st.success("Datasets Joined Successfully")

        st.dataframe(joined)

        csv = joined.to_csv(index=False)

        st.download_button(
            "Download Joined Dataset",
            csv,
            "joined_dataset.csv"
        )