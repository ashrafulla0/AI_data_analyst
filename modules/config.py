"""
Application Configuration
AI Data Analyst Pro
"""

from pathlib import Path

# ==========================================================
# APP INFORMATION
# ==========================================================

APP_NAME = "AI Data analyst Assistance"

APP_VERSION = "1.0.0"

APP_ICON = "🕸️"

APP_DESCRIPTION = (
    "Upload datasets, analyze data, AI generate charts, "
    "ask AI questions, create reports, SQL and Python code."
)

# ==========================================================
# DIRECTORIES
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_FOLDER = BASE_DIR / "uploads"

REPORT_FOLDER = BASE_DIR / "reports"

EXPORT_FOLDER = BASE_DIR / "exports"

CHART_FOLDER = BASE_DIR / "charts"

DATA_FOLDER = BASE_DIR / "data"

ASSET_FOLDER = BASE_DIR / "assets"

# Create folders automatically
for folder in [
    UPLOAD_FOLDER,
    REPORT_FOLDER,
    EXPORT_FOLDER,
    CHART_FOLDER,
    DATA_FOLDER,
    ASSET_FOLDER,
]:
    folder.mkdir(parents=True, exist_ok=True)

# ==========================================================
# FILE SETTINGS
# ==========================================================

SUPPORTED_FILE_TYPES = [
    "csv",
    "xlsx",
    "xls"
]

MAX_UPLOAD_SIZE_MB = 200

# ==========================================================
# UI SETTINGS
# ==========================================================

THEME_COLOR = "#1f77b4"

SIDEBAR_WIDTH = 320

ROWS_TO_PREVIEW = 20

# ==========================================================
# AI SETTINGS
# ==========================================================

DEFAULT_MODEL = "gemini-2.5-flash"

AI_TEMPERATURE = 0.3

MAX_CHAT_HISTORY = 20

# ==========================================================
# JOIN TYPES
# ==========================================================

JOIN_TYPES = [
    "Inner Join",
    "Left Join",
    "Right Join",
    "Outer Join"
]

# ==========================================================
# CHART TYPES
# ==========================================================

CHART_TYPES = [
    "Auto",
    "Bar",
    "Line",
    "Scatter",
    "Histogram",
    "Pie",
    "Box",
    "Heatmap",
    "Area"
]

# ==========================================================
# EXPORT TYPES
# ==========================================================

EXPORT_TYPES = [
    "CSV",
    "Excel",
    "PDF",
    "Word"
]

# ==========================================================
# NAVIGATION MENU
# ==========================================================
MENU_ITEMS = [
    "🏠 Home",
    "📑 Data Preview",
    "📋 Dataset Information",
    "🧹 Data Cleaning",
    "📊 Statistics",
    "🗂 Data Model",
    "📈 Visualizations",
    "🔗 Join Datasets",
    "🤖 AI Chat",
    "🧠 AI Dashboard Builder",  # Use this name exactly
    "💼 Business Insights",
    "📄 Reports",
    "🧮 Excel Assistant",
    "🗄 SQL Generator",
    "🐍 Python Generator",
    "📤 Export",
    "⚙ Settings",
    "ℹ About"
]

