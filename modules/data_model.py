"""
Professional Data Modeling Module
AI Data Analyst Pro
"""

from __future__ import annotations

import json
import streamlit as st


# ==========================================================
# PRIMARY KEY DETECTION
# ==========================================================

def detect_primary_keys(df):
    """
    Detect probable primary keys.
    """

    primary_keys = []

    for col in df.columns:

        name = col.lower()

        if (
            name == "id"
            or name.endswith("_id")
            or name.endswith("id")
        ):

            if df[col].is_unique:
                primary_keys.append(col)

    return primary_keys


# ==========================================================
# FOREIGN KEY SUGGESTIONS
# ==========================================================

def detect_foreign_keys(datasets):

    suggestions = []

    names = list(datasets.keys())

    for i in range(len(names)):

        for j in range(i + 1, len(names)):

            left_df = datasets[names[i]]
            right_df = datasets[names[j]]

            common = set(left_df.columns).intersection(right_df.columns)

            for col in common:

                suggestions.append({

                    "left_table": names[i],
                    "left_column": col,

                    "right_table": names[j],
                    "right_column": col,

                    "cardinality": detect_cardinality(
                        left_df,
                        right_df,
                        col,
                        col
                    ),

                    "reason": "Matching column names"

                })

    return suggestions


# ==========================================================
# CARDINALITY
# ==========================================================

def detect_cardinality(df1, df2, col1, col2):

    left_unique = df1[col1].is_unique
    right_unique = df2[col2].is_unique

    if left_unique and right_unique:
        return "1 : 1"

    if left_unique and not right_unique:
        return "1 : M"

    if not left_unique and right_unique:
        return "M : 1"

    return "M : M"


# ==========================================================
# AUTO BUILD RELATIONSHIPS
# ==========================================================

def auto_build_relationships():

    datasets = st.session_state.datasets

    relationships = st.session_state.relationships

    created = 0

    names = list(datasets.keys())

    for i in range(len(names)):

        for j in range(i + 1, len(names)):

            left_df = datasets[names[i]]
            right_df = datasets[names[j]]

            common = set(left_df.columns).intersection(right_df.columns)

            for col in common:

                relation = {

                    "left_table": names[i],
                    "left_column": col,

                    "right_table": names[j],
                    "right_column": col,

                    "cardinality": detect_cardinality(
                        left_df,
                        right_df,
                        col,
                        col
                    )

                }

                if relation not in relationships:

                    relationships.append(relation)

                    created += 1

    return created


# ==========================================================
# ADD RELATIONSHIP
# ==========================================================

def add_relationship(

    left_table,
    left_column,

    right_table,
    right_column,

    cardinality

):

    relation = {

        "left_table": left_table,
        "left_column": left_column,

        "right_table": right_table,
        "right_column": right_column,

        "cardinality": cardinality

    }

    if relation not in st.session_state.relationships:

        st.session_state.relationships.append(relation)

        return True

    return False


# ==========================================================
# DELETE RELATIONSHIP
# ==========================================================

def delete_relationship(index):

    if 0 <= index < len(st.session_state.relationships):

        st.session_state.relationships.pop(index)


# ==========================================================
# UPDATE RELATIONSHIP
# ==========================================================

def update_relationship(index, relation):

    if 0 <= index < len(st.session_state.relationships):

        st.session_state.relationships[index] = relation


# ==========================================================
# SAVE MODEL
# ==========================================================

def save_model(filename="model.json"):

    with open(filename, "w") as f:

        json.dump(

            st.session_state.relationships,

            f,

            indent=4

        )

    return filename


# ==========================================================
# LOAD MODEL
# ==========================================================

def load_model(filename="model.json"):

    try:

        with open(filename) as f:

            st.session_state.relationships = json.load(f)

        return True

    except:

        st.session_state.relationships = []

        return False


# ==========================================================
# AI RECOMMENDATIONS
# ==========================================================

def recommend_relationships(datasets):

    return detect_foreign_keys(datasets)


# ==========================================================
# MODEL HEALTH SCORE
# ==========================================================

def model_score():

    datasets = st.session_state.datasets

    relationships = st.session_state.relationships

    score = 40

    pk = 0

    for df in datasets.values():

        pk += len(detect_primary_keys(df))

    score += pk * 10

    score += len(relationships) * 12

    return min(score, 100)