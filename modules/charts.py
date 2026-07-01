import plotly.express as px
import streamlit as st

def draw_chart(df, result):

    chart_type = result.get("chart_type")
    x = result.get("x")
    y = result.get("y")

    if chart_type == "bar":
        fig = px.bar(df, x=x, y=y)
        st.plotly_chart(fig)

    elif chart_type == "line":
        fig = px.line(df, x=x, y=y)
        st.plotly_chart(fig)

    elif chart_type == "pie":
        fig = px.pie(df, names=x, values=y)
        st.plotly_chart(fig)