import streamlit as st
import streamlit.components.v1 as components
from gps_uvsq_utils.st_helpers import load_sidebar_footer, load_assets


st.set_page_config(
    page_title="Visualisation des données",
    page_icon="🎡",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Main objective page
load_assets()
load_sidebar_footer("Visualisation", "query_stats")
st.title("Visualisation & Statistiques")
