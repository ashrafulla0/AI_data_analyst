"""
Dashboard Module
AI Data Analyst Pro
"""

import streamlit as st


def show_header(app_name, app_description):
    """Display application header."""

    st.title(f"🤖 {app_name}")
    st.caption(app_description)
    st.divider()


def show_home(dataset_count, version):
    """Home dashboard."""

    st.subheader("🏠 Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric("Datasets", dataset_count)
    c2.metric("Version", version)
    c3.metric("Status", "Ready")

    st.markdown("---")

    st.markdown("### 🚀 AI Data Analyst Pro")

    st.info(
        """
This application allows you to:

✅ Upload CSV & Excel

✅ Analyze datasets

✅ Clean data

✅ Generate charts

✅ Ask AI questions

✅ Generate SQL

✅ Generate Python

✅ Business insights

✅ Reports & Export
"""
    )