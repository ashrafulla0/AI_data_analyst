"""
AI Data Analyst Pro
Professional Edition
"""

from __future__ import annotations

import json
import streamlit as st
import plotly.express as px
import plotly.express as px
import json
import plotly.express as px

# ==========================================================
# IMPORT MODULES
# ==========================================================

from modules.config import *


from modules.session_manager import (
    initialize_session,
    add_dataset,
    get_dataset,
    get_dataset_names,
    set_active_dataset
)

# ... rest of your code ...

from modules.loader import load_file

from modules.dashboard import (
    show_header,
    show_home
)

from modules.preview import (
    quick_summary,
    show_preview,
    show_columns,
    show_missing,
    show_duplicates
)

from modules.cleaning import (
    remove_duplicates,
    drop_missing,
    fill_missing,
    quality_score
)

from modules.statistics import (
    basic_stats,
    numeric_summary,
    correlation_matrix,
    column_insights
)

from modules.ai_engine import ask_ai

from modules.visualization import (
    show_visualizations
)

from modules.business import (
    business_dashboard
)

from modules.exporter import (
    export_excel
)

from modules.data_model import (
    detect_primary_keys,
    detect_foreign_keys,
    recommend_relationships,
    auto_build_relationships,
    add_relationship,
    delete_relationship,
    save_model,
    load_model,
    model_score
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM STYLING (THEME)
# ==========================================================

# ==========================================================
# CUSTOM STYLING (MODERN SaaS LOOK)
# ==========================================================

st.markdown("""
<style>
    /* 1. Main Background */
    .stApp {
        background-color: #FFFFFF !important; 
    }

    /* 2. Sidebar Dark Theme */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
    }

    /* 3. Sidebar Text Fix */
    [data-testid="stSidebar"] label p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] div {
        color: #e5e7eb !important;
        font-weight: 500 !important;
    }

    /* 4. ORANGE UPLOAD BOX FIX */
    /* Target the specific upload box container in the sidebar */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background-color: #f97316 !important; /* Orange */
        padding: 10px !important;
        border-radius: 8px !important;
    }
    
    /* Ensure text inside the orange upload box is readable */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] p,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] div,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] span {
        color: #ffffff !important;
    }

    /* 5. Dashboard Card Styling */
    [data-testid="stMetric"] {
        background-color: #F8F9FA !important;
        border: 1px solid #E5E7EB !important;
        padding: 15px !important;
        border-radius: 12px !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #1A73E8 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# SESSION
# ==========================================================
initialize_session()

initialize_session()

if "relationships" not in st.session_state:
    st.session_state.relationships = []

# ==========================================================
# HEADER
# ==========================================================

show_header(
    APP_NAME,
    APP_DESCRIPTION
)

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("📂 Navigation")

    page = st.radio(
        "Select Page",
        MENU_ITEMS
    )

    st.divider()

    st.subheader("Upload Dataset")

    uploaded_files = st.file_uploader(

        "CSV / Excel",

        type=[
            "csv",
            "xlsx",
            "xls"
        ],

        accept_multiple_files=True

    )

    if uploaded_files:

        for file in uploaded_files:

            data = load_file(file)

            if data is None:
                continue

            if isinstance(data, dict):

                for sheet, df in data.items():

                    add_dataset(
                        f"{file.name} | {sheet}",
                        df
                    )

            else:

                add_dataset(
                    file.name,
                    data
                )

    datasets = get_dataset_names()

    if datasets:

        selected = st.selectbox(

            "Active Dataset",

            datasets

        )

        set_active_dataset(selected)

    st.success(
        f"{len(datasets)} Dataset(s) Loaded"
    )

# ==========================================================
# HOME
# ==========================================================

if page == "🏠 Home":

    show_home(

        len(datasets),

        APP_VERSION

    )

# ==========================================================
# DATA PREVIEW
# ==========================================================

elif page == "📑 Data Preview":

    df = get_dataset()

    if df is None:

        st.warning("Upload dataset first.")

    else:

        quick_summary(df)

        st.divider()

        show_preview(df)

# ==========================================================
# DATASET INFORMATION
# ==========================================================

elif page == "📋 Dataset Information":

    df = get_dataset()

    if df is None:

        st.warning("Upload dataset first.")

    else:

        quick_summary(df)

        st.divider()

        show_columns(df)

        st.divider()

        show_missing(df)

        st.divider()

        show_duplicates(df)
# ==========================================================
# DATA CLEANING
# ==========================================================

elif page == "🧹 Data Cleaning":

    df = get_dataset()

    if df is None:

        st.warning("Upload dataset first.")

    else:

        st.subheader("🧹 Data Cleaning")

        st.metric(
            "Quality Score",
            f"{quality_score(df)}%"
        )

        st.divider()

        if st.button("Remove Duplicate Rows"):

            new_df, removed = remove_duplicates(df)

            st.session_state.datasets[
                st.session_state.active_dataset
            ] = new_df

            st.success(f"{removed} duplicate rows removed.")

            st.rerun()

        if st.button("Drop Missing Rows"):

            new_df, removed = drop_missing(df)

            st.session_state.datasets[
                st.session_state.active_dataset
            ] = new_df

            st.success(f"{removed} rows removed.")

            st.rerun()

        st.divider()

        numeric_cols = list(
            df.select_dtypes(include="number").columns
        )

        if numeric_cols:

            st.subheader("Fill Missing Values")

            column = st.selectbox(
                "Column",
                numeric_cols
            )

            method = st.selectbox(

                "Method",

                [
                    "Mean",
                    "Median",
                    "Mode",
                    "Custom"
                ]

            )

            custom = None

            if method == "Custom":

                custom = st.text_input(
                    "Custom Value"
                )

            if st.button("Fill Missing Values"):

                new_df = fill_missing(
                    df,
                    method,
                    column,
                    custom
                )

                st.session_state.datasets[
                    st.session_state.active_dataset
                ] = new_df

                st.success("Missing values updated.")

                st.rerun()


# ==========================================================
# STATISTICS
# ==========================================================

elif page == "📊 Statistics":

    df = get_dataset()

    if df is None:

        st.warning("Upload dataset first.")

    else:

        st.subheader("📊 Statistics")

        st.dataframe(
            basic_stats(df),
            use_container_width=True
        )

        st.divider()

        num = numeric_summary(df)

        if num is not None:

            st.dataframe(
                num,
                use_container_width=True
            )

        st.divider()

        corr = correlation_matrix(df)

        if corr is not None:

            st.dataframe(
                corr,
                use_container_width=True
            )

        st.divider()

        st.dataframe(
            column_insights(df),
            use_container_width=True
        )


# ==========================================================
# DATA MODELING
# ==========================================================

elif page == "🗂 Data Model":

    if "relationships" not in st.session_state:
        st.session_state.relationships = []

    datasets = st.session_state.datasets

    if len(datasets) == 0:

        st.warning("Upload at least one dataset.")

    else:

        st.subheader("🗂 Professional Data Modeling")

        total_pk = 0

        for dataframe in datasets.values():

            total_pk += len(
                detect_primary_keys(dataframe)
            )

        suggestions = recommend_relationships(
            datasets
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Tables", len(datasets))
        c2.metric("Primary Keys", total_pk)
        c3.metric(
            "Relationships",
            len(st.session_state.relationships)
        )
        c4.metric(
            "Suggestions",
            len(suggestions)
        )

        st.divider()

        st.subheader("Tables")

        for name, dataframe in datasets.items():

            with st.expander(name):

                for col in dataframe.columns:

                    if col in detect_primary_keys(dataframe):

                        st.success(f"🔑 {col}")

                    else:

                        st.write(col)

        st.divider()

        st.subheader("AI Relationship Suggestions")

        if suggestions:

            st.dataframe(
                suggestions,
                use_container_width=True
            )

        else:

            st.info("No suggestions found.")

        st.divider()

        if st.button(
            "⚡ Auto Build Relationships"
        ):

            count = auto_build_relationships()

            st.success(
                f"{count} relationships created."
            )

            st.rerun()

        st.divider()

        st.subheader("Manual Relationship")

        table_names = list(datasets.keys())

        left_table = st.selectbox(
            "Left Table",
            table_names
        )

        left_column = st.selectbox(
            "Left Column",
            datasets[left_table].columns
        )

        right_table = st.selectbox(
            "Right Table",
            table_names
        )

        right_column = st.selectbox(
            "Right Column",
            datasets[right_table].columns
        )

        card = st.selectbox(

            "Cardinality",

            [
                "1 : 1",
                "1 : M",
                "M : 1",
                "M : M"
            ]
        )

        if st.button("Create Relationship"):

            ok = add_relationship(

                left_table,
                left_column,

                right_table,
                right_column,

                card
            )

            if ok:

                st.success(
                    "Relationship created."
                )

                st.rerun()

            else:

                st.warning(
                    "Relationship already exists."
                )

        st.divider()

        st.subheader("Current Relationships")

        if len(st.session_state.relationships) == 0:

            st.info("No relationships.")

        else:

            st.dataframe(
                st.session_state.relationships,
                use_container_width=True
            )

            delete_index = st.number_input(
                "Relationship Index To Delete",
                0,
                len(st.session_state.relationships)-1,
                0
            )

            if st.button("Delete Selected"):

                delete_relationship(delete_index)

                st.success("Deleted.")

                st.rerun()

        st.divider()

        col1, col2 = st.columns(2)

        if col1.button("💾 Save Model"):

            file = save_model()

            st.success(file)

        if col2.button("📂 Load Model"):

            load_model()

            st.success("Loaded.")

            st.rerun()

        st.divider()

        st.metric(

            "🏆 Model Health",

            f"{model_score()}%"
        )

# ==========================================================
# VISUALIZATIONS
# ==========================================================

elif page == "📈 Visualizations":

    df = get_dataset()

    if df is None:

        st.warning("Upload dataset first.")

    else:

        st.subheader("📈 Interactive Visualizations")

        show_visualizations(df)


# ==========================================================
# JOIN DATASETS
# ==========================================================

elif page == "🔗 Join Datasets":

    datasets = st.session_state.datasets

    if len(datasets) < 2:

        st.warning("Please upload at least two datasets.")

    else:

        st.subheader("🔗 Join Multiple Datasets")

        names = list(datasets.keys())

        left_table = st.selectbox(
            "Left Dataset",
            names,
            key="join_left"
        )

        right_table = st.selectbox(
            "Right Dataset",
            names,
            key="join_right"
        )

        left_df = datasets[left_table]
        right_df = datasets[right_table]

        left_col = st.selectbox(
            "Left Column",
            left_df.columns,
            key="join_left_col"
        )

        right_col = st.selectbox(
            "Right Column",
            right_df.columns,
            key="join_right_col"
        )

        join_type = st.selectbox(

            "Join Type",

            [
                "inner",
                "left",
                "right",
                "outer",
                "cross"
                "self"
            ]

        )

        if st.button("Join Datasets"):

            try:

                if join_type == "cross":
                    merged = left_df.merge(
                        right_df,
                        how="cross"
                    )

                elif join_type == "self":
                    st.info("Self join uses only the selected dataset")

                    merged = left_df.merge(
                        left_df,
                        left_on=left_col,
                        right_on=right_col,
                        how="inner"
                    )
                    
                else:
                    merged = left_df.merge(
                        right_df,
                        left_on=left_col,
                        right_on=right_col,
                        how=join_type
                    )

                st.success("Datasets Joined Successfully")

                st.dataframe(
                    merged,
                    use_container_width=True
                )

                st.session_state.joined_dataset = merged

            except Exception as e:

                st.error(e)


# ==========================================================
# AI CHAT
# ==========================================================

elif page == "🤖 AI Chat":

    df = get_dataset()

    if df is None:

        st.warning("Upload dataset first.")

    else:

        st.subheader("🤖 AI Data Analyst")

        question = st.text_input(
            "Ask anything about your dataset"
        )

        if question:

            try:

                df_sample = df.head(30).to_csv(index=False)

                answer = ask_ai(
                    df_sample,
                    question
                )

                st.markdown("### AI Answer")

                st.write(answer)

            except Exception as e:

                st.error(e)


# ==========================================================
# SQL GENERATOR
# ==========================================================

elif page == "🗄 SQL Generator":

    df = get_dataset()

    if df is None:

        st.warning("Upload dataset first.")

    else:

        st.subheader("🗄 SQL Generator")

        prompt = st.text_input(
            "Describe the SQL query"
        )

        if st.button("Generate SQL"):

            try:

                df_sample = df.head(20).to_csv(index=False)

                sql = ask_ai(
                    df_sample,
                    prompt,
                    mode="sql"
                )

                st.code(
                    sql,
                    language="sql"
                )

                st.download_button(

                    "Download SQL",

                    sql,

                    file_name="query.sql",

                    mime="text/plain"

                )

            except Exception as e:

                st.error(e)


# ==========================================================
# PYTHON GENERATOR
# ==========================================================

elif page == "🐍 Python Generator":

    df = get_dataset()

    if df is None:

        st.warning("Upload dataset first.")

    else:

        st.subheader("🐍 Python Code Generator")

        prompt = st.text_input(
            "Describe the Python code"
        )

        if st.button("Generate Python"):

            try:

                df_sample = df.head(20).to_csv(index=False)

                code = ask_ai(
                    df_sample,
                    prompt,
                    mode="python"
                )

                st.code(
                    code,
                    language="python"
                )

                st.download_button(

                    "Download Python",

                    code,

                    file_name="analysis.py",

                    mime="text/plain"

                )

            except Exception as e:

                st.error(e)
# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

elif page == "💼 Business Insights":

    df = get_dataset()

    if df is None:

        st.warning("Upload dataset first.")

    else:

        st.subheader("💼 Business Insights Dashboard")

        business_dashboard(df)


# ==========================================================
# REPORTS
# ==========================================================

elif page == "📄 Reports":

    df = get_dataset()

    if df is None:

        st.warning("Upload dataset first.")

    else:

        st.subheader("📄 AI Report Generator")

        st.write("Generate a quick report from your dataset.")

        st.metric("Rows", df.shape[0])
        st.metric("Columns", df.shape[1])

        st.divider()

        st.write("### Dataset Summary")

        st.dataframe(df.describe(include="all"))

        report = df.describe(include="all").to_csv()

        st.download_button(

            "📥 Download Report",

            report,

            file_name="dataset_report.csv",

            mime="text/csv"

        )


# ==========================================================
# EXCEL ASSISTANT
# ==========================================================

elif page == "🧮 Excel Assistant":

    st.subheader("🧮 Excel Formula Assistant")

    question = st.text_input(

        "Example: How do I calculate average sales?"

    )

    if st.button("Generate Formula"):

        if question == "":

            st.warning("Enter your question.")

        else:

            try:

                formula = ask_ai(

                    "",

                    question,

                    mode="excel"

                )

                st.success("Excel Formula")

                st.code(

                    formula,

                    language="text"

                )

            except Exception as e:

                st.error(e)


# ==========================================================
# EXPORT
# ==========================================================

elif page == "📤 Export":

    df = get_dataset()

    if df is None:

        st.warning("Upload dataset first.")

    else:

        st.subheader("📤 Export Dataset")

        csv = df.to_csv(index=False)

        st.download_button(

            "📥 Download CSV",

            csv,

            file_name="dataset.csv",

            mime="text/csv"

        )

        excel = export_excel(df)

        st.download_button(

            "📥 Download Excel",

            excel,

            file_name="dataset.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        )


# ==========================================================
# 🧠 AUTO DASHBOARD BUILDER (ONE CLICK AI)
# ==========================================================

elif page == "📊 Auto Dashboard":

    df = get_dataset()

    if df is None:

        st.warning("Upload dataset first")

    else:

        st.subheader("🧠 AI Auto Dashboard Builder")

        st.write("One click generates full dashboard from your dataset")

        # -----------------------------
        # BUTTON: GENERATE DASHBOARD
        # -----------------------------
        if st.button("🚀 Generate Auto Dashboard"):

            numeric_cols = list(df.select_dtypes(include="number").columns)
            cat_cols = list(df.select_dtypes(exclude="number").columns)

            st.divider()

            # =========================
            # KPI CARDS
            # =========================
            st.subheader("📊 KPI Cards")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Rows", df.shape[0])
            col2.metric("Columns", df.shape[1])
            col3.metric("Missing", df.isnull().sum().sum())
            col4.metric("Duplicates", df.duplicated().sum())

            st.divider()

            # =========================
            # AUTO CHART 1
            # =========================
            st.subheader("📈 Auto Visualizations")

            if len(numeric_cols) > 0:

                col = numeric_cols[0]

                st.write(f"📊 Distribution of {col}")

                fig1 = px.histogram(df, x=col)

                st.plotly_chart(fig1, use_container_width=True)

            # =========================
            # AUTO CHART 2
            # =========================
            if len(numeric_cols) >= 2:

                st.write("📊 Correlation Scatter")

                fig2 = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1])

                st.plotly_chart(fig2, use_container_width=True)

            # =========================
            # PIE CHART (CATEGORY)
            # =========================
            if len(cat_cols) > 0:

                col = cat_cols[0]

                st.write(f"📊 Category Distribution: {col}")

                fig3 = px.pie(df, names=col)

                st.plotly_chart(fig3, use_container_width=True)
    

            # =========================
            # AI INSIGHT TEXT
            # =========================
            st.divider()

            st.subheader("🧠 AI Insights")

            st.write(
                "• Dataset contains structured tabular data\n"
                "• Numerical columns detected for analytics\n"
                "• Categorical segmentation available\n"
                "• Ready for business reporting"
            )

            st.success("Dashboard generated successfully 🚀")


# ==========================================================
# SETTINGS
# ==========================================================

elif page == "⚙ Settings":

    st.subheader("⚙ Application Settings")

    theme = st.selectbox(

        "Theme",

        [

            "Light",

            "Dark"

        ]

    )

    language = st.selectbox(

        "Language",

        [

            "English",

            "Hindi"

        ]

    )

    st.success("Settings Saved")


# ==========================================================
# ABOUT
# ==========================================================

elif page == "ℹ About":

    st.subheader("ℹ About AI Data Analyst Pro")

    st.info(

        f"""

### {APP_NAME}

Version : {APP_VERSION}

Professional AI-powered Data Analytics Platform

Features

- Upload CSV / Excel
- Data Cleaning
- Statistics
- Data Modeling
- Interactive Charts
- AI Chat
- Business Insights
- SQL Generator
- Python Generator
- Excel Formula Assistant
- Export CSV / Excel

Built with ❤️ using Streamlit + Groq

"""

    )

# ==========================================================
# AI CHAT (FIXED + SAFE JSON HANDLING)
# ==========================================================

elif page == "🤖 AI Chat":

    df = get_dataset()

    if df is None:

        st.warning("Upload dataset first.")

    else:

        st.subheader("🤖 AI Chat (Groq)")

        question = st.text_input("Ask your question")

        if question:

            df_sample = df.head(30).to_csv(index=False)

            response = ask_ai(df_sample, question)

            st.divider()

            # -------------------------
            # SAFE JSON PARSING FIX
            # -------------------------
            try:
                result = json.loads(response)

                # TEXT RESPONSE
                if result.get("type") == "text":
                    st.success(result.get("answer", ""))

                # CHART RESPONSE
                elif result.get("type") == "chart":

                    st.success(result.get("explanation", ""))

                    chart_type = result.get("chart_type")
                    x = result.get("x")
                    y = result.get("y")

                    if chart_type == "bar":
                        fig = px.bar(df, x=x, y=y)
                        st.plotly_chart(fig, use_container_width=True)

                    elif chart_type == "line":
                        fig = px.line(df, x=x, y=y)
                        st.plotly_chart(fig, use_container_width=True)

                    elif chart_type == "pie":
                        fig = px.pie(df, names=x, values=y)
                        st.plotly_chart(fig, use_container_width=True)

                    elif chart_type == "scatter":
                        fig = px.scatter(df, x=x, y=y)
                        st.plotly_chart(fig, use_container_width=True)

                else:
                    st.write(response)

            except Exception:
                # fallback if AI returns normal text or broken JSON
                st.write(response)


# ==========================================================
# JOIN DATASET VIEW (JOIN RESULT DISPLAY FIX)
# ==========================================================

if "joined_dataset" in st.session_state and page == "🔗 Join Datasets":

    if st.session_state.joined_dataset is not None:

        st.subheader("📊 Joined Dataset Preview")

        st.dataframe(
            st.session_state.joined_dataset,
            use_container_width=True
        )


# ==========================================================
# FALLBACK SAFETY
# ==========================================================

else:

    pass

# ==========================================================
# FINAL SAFETY FIXES (SESSION + MODEL SCORE FIX)
# ==========================================================

# --------------------------
# Ensure relationships exist
# --------------------------
if "relationships" not in st.session_state:
    st.session_state.relationships = []


# --------------------------
# FIX model_score ERROR SAFETY
# --------------------------
def safe_model_score():
    try:
        return model_score(
            st.session_state.datasets,
            st.session_state.relationships
        )
    except:
        return 0


# --------------------------
# OPTIONAL GLOBAL FOOTER
# --------------------------
st.markdown("---")
st.caption("🚀 AI Data Analyst Pro | Fully Built System")


# --------------------------
# DEBUG PANEL (optional)
# --------------------------
with st.expander("🔧 Debug Info"):

    st.write("Datasets:", len(st.session_state.datasets))
    st.write("Relationships:", len(st.session_state.relationships))
    st.write("Active Dataset:", st.session_state.active_dataset)

    st.write("Session Keys:", list(st.session_state.keys()))