import streamlit as st
import pandas as pd

# Import tab modules
import workforce
import attrition_retention as attrition
import career
import survey
import aboutus

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="ACJ Dashboard", 
    layout="wide",
    page_icon="📊"
)

# -----------------------------
# Load CSS file globally
# -----------------------------
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -----------------------------
# Load Excel outputs with caching
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("HR_Analysis_Output.xlsx", sheet_name=None)
    df_raw = pd.read_excel("HR Cleaned Data 01.09.26.xlsx", sheet_name="Data")
    df_attrition = pd.read_excel("Attrition-Vol and Invol.xlsx")
    return df, df_raw, df_attrition

# Load data once using cache
df, df_raw, df_attrition = load_data()

# -----------------------------
# Ensure Year column exists
# -----------------------------
if "Year" not in df_raw.columns and "Calendar Year" in df_raw.columns:
    df_raw["Year"] = pd.to_datetime(df_raw["Calendar Year"]).dt.year

if "Year" not in df_attrition.columns and "Calendar Year" in df_attrition.columns:
    df_attrition["Year"] = pd.to_datetime(df_attrition["Calendar Year"]).dt.year

# -----------------------------
# App Title
# -----------------------------
st.title("ACJ Company Dashboard")

# -----------------------------
# Global Year Selector
# -----------------------------
year_options = ["All"] + list(range(2020, 2026))
selected_year = st.radio("Select Year", year_options, index=0, horizontal=True)

# -----------------------------
# Initialize session state for active tab
# -----------------------------
if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0

# -----------------------------
# Custom CSS for tab buttons
# -----------------------------
st.markdown("""
<style>
    /* Style for inactive tab buttons */
    div[data-testid="column"] > div > div > button[kind="secondary"] {
        width: 100%;
        border-radius: 5px;
        border: 2px solid #e0e0e0;
        background-color: white;
        color: #333;
        font-weight: 500;
        padding: 10px;
        transition: all 0.3s;
    }
    
    /* Hover state for inactive tabs */
    div[data-testid="column"] > div > div > button[kind="secondary"]:hover {
        border-color: #6495ED;
        background-color: #f0f8ff;
        color: #00008B;
    }
    
    /* Style for active tab button */
    div[data-testid="column"] > div > div > button[kind="primary"] {
        width: 100%;
        border-radius: 5px;
        border: 2px solid #00008B;
        background-color: #00008B;
        color: white;
        font-weight: 600;
        padding: 10px;
        transition: all 0.3s;
    }
    
    /* Hover state for active tab */
    div[data-testid="column"] > div > div > button[kind="primary"]:hover {
        background-color: #000070;
        border-color: #000070;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Tab navigation with buttons
# -----------------------------
tab_names = [
    "👥 Workforce",
    "🔄 Attrition & Retention",
    "🎯 Career Progression",
    "💬 Survey & Feedback",
    "📚 About Us"
]

# Create tab buttons
tab_cols = st.columns(len(tab_names))
for idx, (col, name) in enumerate(zip(tab_cols, tab_names)):
    # Highlight active tab
    button_type = "primary" if st.session_state.active_tab == idx else "secondary"
    if col.button(name, key=f"tab_{idx}", use_container_width=True, type=button_type):
        st.session_state.active_tab = idx
        st.rerun()

st.markdown("---")

# -----------------------------
# Render content based on active tab
# -----------------------------
active_tab = st.session_state.active_tab

if active_tab == 0:  # Workforce
    workforce.render(df, df_raw, selected_year)

elif active_tab == 1:  # Attrition & Retention
    attrition.render(df, df_raw, selected_year, df_attrition)

elif active_tab == 2:  # Career Progression
    career.render(df, df_raw, selected_year)

elif active_tab == 3:  # Survey & Feedback
    survey.render(df, df_raw, selected_year)

elif active_tab == 4:  # About Us
    aboutus.render(df, df_raw, selected_year)
