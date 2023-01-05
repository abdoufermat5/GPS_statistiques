import os

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from gps_uvsq_utils.st_helpers import load_assets, load_html, load_sidebar_footer

st.set_page_config(
    page_title="Accueil",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_assets()

# load html file
descriptions = load_html("html/descriptions.html")
footer = load_html("html/footer.html")
members = load_html("html/members.html")

# components.html(file, height=1000)
st.markdown("""
<header class="bg-dark text-center py-2">
    <h5 class="display-5 text-white font-weight-bold">Calculs statistiques
privacy-by-design pour le Cloud personnel</h5>
</header>
""", unsafe_allow_html=True)
st.markdown(descriptions, unsafe_allow_html=True)
st.markdown(members, unsafe_allow_html=True)
st.markdown(footer, unsafe_allow_html=True)
load_sidebar_footer("Page d'accueil", "home")