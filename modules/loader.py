"""
loader.py
AI Data Analyst Pro

Handles:
- CSV files
- Excel files (.xlsx/.xls)
- Multiple Excel sheets
- File validation
- Dataset information
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import streamlit as st

from modules.config import SUPPORTED_FILE_TYPES


# ==========================================================
# FILE VALIDATION
# ==========================================================

def validate_file(uploaded_file):
    """
    Validate uploaded file.

    Returns:
        (True, "") if valid
        (False, error_message) if invalid
    """

    if uploaded_file is None:
        return False, "No file selected."

    extension = uploaded_file.name.split(".")[-1].lower()

    if extension not in SUPPORTED_FILE_TYPES:
        return False, f"Unsupported file type: {extension}"

    return True, ""


# ==========================================================
# LOAD CSV
# ==========================================================

def load_csv(uploaded_file):
    """
    Load CSV file.
    """

    try:
        df = pd.read_csv(uploaded_file)
        return df

    except UnicodeDecodeError:
        # Try another encoding
        df = pd.read_csv(uploaded_file, encoding="latin1")
        return df

    except Exception as e:
        st.error(f"CSV Error : {e}")
        return None


# ==========================================================
# LOAD EXCEL
# ==========================================================

def load_excel(uploaded_file):
    """
    Load Excel file.

    Returns:
        dictionary of sheets
    """

    try:

        excel = pd.ExcelFile(uploaded_file)

        sheets = {}

        for sheet in excel.sheet_names:
            sheets[sheet] = pd.read_excel(
                excel,
                sheet_name=sheet
            )

        return sheets

    except Exception as e:

        st.error(f"Excel Error : {e}")

        return None


# ==========================================================
# UNIVERSAL LOADER
# ==========================================================

def load_file(uploaded_file):
    """
    Automatically detect file type
    and load it.
    """

    valid, message = validate_file(uploaded_file)

    if not valid:
        st.error(message)
        return None

    extension = uploaded_file.name.split(".")[-1].lower()

    if extension == "csv":
        return load_csv(uploaded_file)

    if extension in ["xlsx", "xls"]:
        return load_excel(uploaded_file)

    return None


# ==========================================================
# DATASET INFO
# ==========================================================

def dataset_info(df):
    """
    Returns basic dataset information.
    """

    return {

        "Rows": df.shape[0],

        "Columns": df.shape[1],

        "Column Names": list(df.columns),

        "Data Types": df.dtypes.astype(str).to_dict(),

        "Missing Values": df.isnull().sum().to_dict(),

        "Duplicate Rows": int(df.duplicated().sum()),

        "Memory (MB)": round(
            df.memory_usage(deep=True).sum() / (1024 ** 2),
            2
        ),

        "Numeric Columns": list(
            df.select_dtypes(include="number").columns
        ),

        "Categorical Columns": list(
            df.select_dtypes(include="object").columns
        ),

        "Date Columns": list(
            df.select_dtypes(include="datetime").columns
        )
    }


# ==========================================================
# FILE DETAILS
# ==========================================================

def file_details(uploaded_file):
    """
    Returns uploaded file details.
    """

    extension = uploaded_file.name.split(".")[-1].lower()

    return {

        "Filename": uploaded_file.name,

        "Extension": extension,

        "Size (KB)": round(
            uploaded_file.size / 1024,
            2
        )

    }


# ==========================================================
# SHEET NAMES
# ==========================================================

def get_sheet_names(uploaded_file):
    """
    Return Excel sheet names.
    """

    try:

        excel = pd.ExcelFile(uploaded_file)

        return excel.sheet_names

    except Exception:

        return []


# ==========================================================
# LOAD SINGLE SHEET
# ==========================================================

def load_sheet(uploaded_file, sheet_name):
    """
    Load one Excel sheet.
    """

    try:

        df = pd.read_excel(
            uploaded_file,
            sheet_name=sheet_name
        )

        return df

    except Exception as e:

        st.error(e)

        return None


# ==========================================================
# DATA QUALITY SCORE
# ==========================================================

def data_quality_score(df):
    """
    Calculate a simple data quality score (0–100).
    """

    total_cells = df.shape[0] * df.shape[1]

    if total_cells == 0:
        return 0

    missing = df.isnull().sum().sum()

    duplicates = df.duplicated().sum()

    score = 100

    score -= (missing / total_cells) * 50

    score -= (duplicates / max(len(df), 1)) * 50

    return round(max(score, 0), 2)