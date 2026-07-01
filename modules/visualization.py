import streamlit as st
import plotly.express as px


def show_visualizations(df):

    st.subheader("📈 Interactive Visualizations")

    numeric = list(df.select_dtypes(include="number").columns)
    categorical = list(df.select_dtypes(exclude="number").columns)

    chart = st.selectbox(
        "Chart",
        ["Bar", "Line", "Scatter", "Pie", "Histogram", "Box"]
    )

    if chart == "Pie":

        x = st.selectbox("Category", categorical)
        y = st.selectbox("Values", numeric)

        fig = px.pie(df, names=x, values=y)

    elif chart == "Bar":

        x = st.selectbox("X", df.columns)
        y = st.selectbox("Y", numeric)

        fig = px.bar(df, x=x, y=y)

    elif chart == "Line":

        x = st.selectbox("X", df.columns)
        y = st.selectbox("Y", numeric)

        fig = px.line(df, x=x, y=y)

    elif chart == "Scatter":

        x = st.selectbox("X", numeric)
        y = st.selectbox("Y", numeric)

        fig = px.scatter(df, x=x, y=y)

    elif chart == "Histogram":

        x = st.selectbox("Column", numeric)

        fig = px.histogram(df, x=x)

    else:

        y = st.selectbox("Column", numeric)

        fig = px.box(df, y=y)

    st.plotly_chart(fig, use_container_width=True)