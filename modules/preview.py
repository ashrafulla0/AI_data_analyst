"""
preview.py
AI Data Analyst Pro

Dataset preview utilities.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


# ==========================================================
# DATA PREVIEW
# ==========================================================

def show_preview(df: pd.DataFrame, rows: int = 20):
    """
    Display dataframe preview.
    """

    st.subheader("📑 Dataset Preview")

    st.dataframe(
        df.head(rows),
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# DATA SHAPE
# ==========================================================

def show_shape(df: pd.DataFrame):

    col1, col2 = st.columns(2)

    col1.metric(
        "Rows",
        f"{df.shape[0]:,}"
    )

    col2.metric(
        "Columns",
        f"{df.shape[1]:,}"
    )


# ==========================================================
# COLUMN INFORMATION
# ==========================================================

def show_columns(df: pd.DataFrame):

    st.subheader("📋 Columns")

    column_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,
        "Unique Values": [df[c].nunique() for c in df.columns]
    })

    st.dataframe(
        column_df,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# MISSING VALUES
# ==========================================================

def show_missing(df: pd.DataFrame):

    missing = pd.DataFrame({

        "Column": df.columns,

        "Missing Values": df.isnull().sum().values,

        "Percentage":
            (
                df.isnull().sum()
                / len(df)
                * 100
            ).round(2).values

    })

    st.subheader("🚨 Missing Values")

    st.dataframe(
        missing,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# DUPLICATES
# ==========================================================

def show_duplicates(df: pd.DataFrame):

    duplicates = int(df.duplicated().sum())

    st.metric(
        "Duplicate Rows",
        duplicates
    )


# ==========================================================
# DATA TYPES
# ==========================================================

def show_data_types(df: pd.DataFrame):

    st.subheader("📌 Data Types")

    dtype_df = pd.DataFrame({

        "Column": df.columns,

        "Data Type": df.dtypes.astype(str)

    })

    st.dataframe(
        dtype_df,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# NUMERIC COLUMNS
# ==========================================================

def numeric_columns(df):

    return list(
        df.select_dtypes(include="number").columns
    )


# ==========================================================
# CATEGORICAL COLUMNS
# ==========================================================

def categorical_columns(df):

    return list(
        df.select_dtypes(include="object").columns
    )


# ==========================================================
# DATE COLUMNS
# ==========================================================

def datetime_columns(df):

    return list(
        df.select_dtypes(include="datetime").columns
    )


# ==========================================================
# QUICK SUMMARY
# ==========================================================

def quick_summary(df):

    st.subheader("📊 Quick Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Rows",
        f"{len(df):,}"
    )

    c2.metric(
        "Columns",
        len(df.columns)
    )

    c3.metric(
        "Missing",
        int(df.isnull().sum().sum())
    )

    c4.metric(
        "Duplicates",
        int(df.duplicated().sum())
    )