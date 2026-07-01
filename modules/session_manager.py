"""
Session Manager
AI Data Analyst Pro

This module initializes and manages Streamlit session state.
"""

from __future__ import annotations

import streamlit as st


def initialize_session():
    """
    Initialize all session state variables.
    Safe to call multiple times.
    """

    defaults = {

    # ==========================
    # Uploaded Datasets
    # ==========================
    "datasets": {},
    "dataset_names": [],
    "active_dataset": None,

    # ==========================
    # Excel Information
    # ==========================
    "excel_sheets": {},
    "selected_sheet": None,

    # ==========================
    # AI Chat
    # ==========================
    "chat_history": [],
    "conversation_memory": [],

    # ==========================
    # Reports
    # ==========================
    "reports": [],

    # ==========================
    # Charts
    # ==========================
    "generated_charts": [],

    # ==========================
    # SQL
    # ==========================
    "generated_sql": [],

    # ==========================
    # Python
    # ==========================
    "generated_python": [],

    # ==========================
    # Excel Formulas
    # ==========================
    "generated_excel": [],

    # ==========================
    # Business Insights
    # ==========================
    "business_insights": [],

    # ==========================
    # Cleaning History
    # ==========================
    "cleaning_history": [],

    # ==========================
    # Undo
    # ==========================
    "undo_stack": [],

    # ==========================
    # Logs
    # ==========================
    "logs": [],

    # ==========================
    # Current Page
    # ==========================
    "current_page": "🏠 Home",

    # ==========================
    # User Settings
    # ==========================
    "theme": "Light",
    "language": "English",

    # ==========================
    # AI Suggestions
    # ==========================
    "ai_suggestions": [],

    # ==========================
    # Join Results
    # ==========================
    "joined_dataset": None,

    # =====================================================
    # POWER BI DATA MODELING (NEW)
    # =====================================================

    # Relationships
    "relationships": [],

    # Primary Keys
    "primary_keys": {},

    # Foreign Keys
    "foreign_keys": {},

    # Cardinality
    "cardinality": {},

    # Table positions (future draggable layout)
    "table_positions": {},

    # Saved models
    "saved_models": {},

    # Current model
    "data_model": {},

    # AI recommendations
    "relationship_suggestions": [],

    # Selected relationship
    "selected_relationship": None,

    # Relationship history
    "relationship_history": []
}

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ==========================================================
# DATASET FUNCTIONS
# ==========================================================

def add_dataset(name, dataframe):
    """Store dataset."""

    st.session_state.datasets[name] = dataframe

    if name not in st.session_state.dataset_names:
        st.session_state.dataset_names.append(name)

    st.session_state.active_dataset = name


def get_dataset(name=None):
    """Return dataframe."""

    if name is None:
        name = st.session_state.active_dataset

    if name is None:
        return None

    return st.session_state.datasets.get(name)


def get_dataset_names():
    """Return all dataset names."""

    return st.session_state.dataset_names


def set_active_dataset(name):
    """Select active dataset."""

    if name in st.session_state.datasets:
        st.session_state.active_dataset = name


def remove_dataset(name):
    """Delete dataset."""

    if name in st.session_state.datasets:
        del st.session_state.datasets[name]

    if name in st.session_state.dataset_names:
        st.session_state.dataset_names.remove(name)

    if st.session_state.active_dataset == name:
        st.session_state.active_dataset = None


# ==========================================================
# CHAT
# ==========================================================

def add_chat(role, message):
    """Save chat."""

    st.session_state.chat_history.append({
        "role": role,
        "message": message
    })


def clear_chat():
    st.session_state.chat_history = []


# ==========================================================
# LOGS
# ==========================================================

def add_log(message):
    st.session_state.logs.append(message)


# ==========================================================
# REPORTS
# ==========================================================

def save_report(report):
    st.session_state.reports.append(report)


# ==========================================================
# CHARTS
# ==========================================================

def save_chart(chart):
    st.session_state.generated_charts.append(chart)


# ==========================================================
# SQL
# ==========================================================

def save_sql(sql):
    st.session_state.generated_sql.append(sql)


# ==========================================================
# PYTHON
# ==========================================================

def save_python(code):
    st.session_state.generated_python.append(code)


# ==========================================================
# EXCEL
# ==========================================================

def save_excel_formula(formula):
    st.session_state.generated_excel.append(formula)


# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

def save_business_insight(insight):
    st.session_state.business_insights.append(insight)


# ==========================================================
# CLEANING HISTORY
# ==========================================================

def add_cleaning_step(step):
    st.session_state.cleaning_history.append(step)


# ==========================================================
# UNDO
# ==========================================================

def push_undo(dataframe):
    st.session_state.undo_stack.append(dataframe.copy())


def pop_undo():

    if st.session_state.undo_stack:
        return st.session_state.undo_stack.pop()

    return None