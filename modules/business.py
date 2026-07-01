import streamlit as st


def business_dashboard(df):

    st.subheader("💼 Business Insights")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", len(df))
    c2.metric("Columns", len(df.columns))
    c3.metric("Missing", df.isnull().sum().sum())
    c4.metric("Duplicates", df.duplicated().sum())

    st.divider()

    st.write("### Numeric Summary")

    st.dataframe(df.describe())