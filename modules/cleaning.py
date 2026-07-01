"""
cleaning.py
AI Data Analyst Pro

Data Cleaning Module
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


# ==========================================================
# REMOVE DUPLICATES
# ==========================================================

def remove_duplicates(df):

    before = len(df)

    df = df.drop_duplicates()

    removed = before - len(df)

    return df, removed


# ==========================================================
# DROP MISSING ROWS
# ==========================================================

def drop_missing(df):

    before = len(df)

    df = df.dropna()

    removed = before - len(df)

    return df, removed


# ==========================================================
# FILL MISSING VALUES
# ==========================================================

def fill_missing(df, method, column=None, value=None):

    df = df.copy()

    if column is None:
        return df

    if method == "Mean":

        df[column] = df[column].fillna(df[column].mean())

    elif method == "Median":

        df[column] = df[column].fillna(df[column].median())

    elif method == "Mode":

        df[column] = df[column].fillna(df[column].mode()[0])

    elif method == "Custom":

        df[column] = df[column].fillna(value)

    return df


# ==========================================================
# REMOVE COLUMNS
# ==========================================================

def remove_columns(df, columns):

    return df.drop(columns=columns)


# ==========================================================
# RENAME COLUMN
# ==========================================================

def rename_column(df, old, new):

    return df.rename(columns={old: new})


# ==========================================================
# CHANGE DATA TYPE
# ==========================================================

def change_dtype(df, column, dtype):

    df = df.copy()

    try:

        if dtype == "int":

            df[column] = df[column].astype("Int64")

        elif dtype == "float":

            df[column] = df[column].astype(float)

        elif dtype == "string":

            df[column] = df[column].astype(str)

        elif dtype == "datetime":

            df[column] = pd.to_datetime(df[column])

        elif dtype == "bool":

            df[column] = df[column].astype(bool)

    except Exception as e:

        st.error(e)

    return df


# ==========================================================
# DATA QUALITY SCORE
# ==========================================================

def quality_score(df):

    total = df.shape[0] * df.shape[1]

    if total == 0:
        return 0

    missing = df.isnull().sum().sum()

    duplicate = df.duplicated().sum()

    score = 100

    score -= (missing / total) * 50

    score -= (duplicate / len(df)) * 50

    return round(max(score, 0), 2)