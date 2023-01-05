import streamlit as st
import streamlit.components.v1 as components
from gps_uvsq_utils.st_helpers import load_assets, load_sidebar_footer

st.set_page_config(
    page_title="Analyse de la base de données MongoDB",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Main objective page
load_assets()
load_sidebar_footer("Analyse BD", "storage")
st.title("Analyse de la base de données MongoDB")
