"""
statistics.py
AI Data Analyst Pro

Advanced Data Statistics Module
"""

import pandas as pd
import streamlit as st


# ==========================
# BASIC STATS
# ==========================

def basic_stats(df):

    return df.describe(include="all")


# ==========================
# NUMERIC SUMMARY
# ==========================

def numeric_summary(df):

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return None

    return pd.DataFrame({
        "Mean": numeric_df.mean(),
        "Median": numeric_df.median(),
        "Min": numeric_df.min(),
        "Max": numeric_df.max(),
        "Std": numeric_df.std()
    })


# ==========================
# CORRELATION MATRIX
# ==========================

def correlation_matrix(df):

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return None

    return numeric_df.corr()


# ==========================
# COLUMN INSIGHTS
# ==========================

def column_insights(df):

    insights = []

    for col in df.columns:

        if df[col].dtype == "object":

            insights.append({
                "Column": col,
                "Type": "Categorical",
                "Unique Values": df[col].nunique(),
                "Most Frequent": df[col].mode()[0] if not df[col].mode().empty else None
            })

        else:

            insights.append({
                "Column": col,
                "Type": "Numeric",
                "Mean": df[col].mean(),
                "Missing": df[col].isnull().sum()
            })

    return pd.DataFrame(insights)