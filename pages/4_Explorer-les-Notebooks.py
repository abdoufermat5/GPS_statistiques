import io
import os
import glob
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from gps_uvsq_utils.st_helpers import load_assets, load_sidebar_footer, load_html

st.set_page_config(
    page_title="Explorer les notebooks",
    page_icon="🎢",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Main objective page
load_assets()
load_sidebar_footer("Exploration de notebooks", "area_chart")
st.title("Exploration des notebooks")

import streamlit as st

# Créer un widget de téléversement de fichiers
fichier_televerse = st.file_uploader("Sélectionnez un fichier markdown à téléverser")

# Vérifier si un fichier a été téléversé
if fichier_televerse:
    # Lire le contenu du fichier
    contenu = fichier_televerse.read().decode("utf-8")

    # Créer un bouton "Afficher"
    show = st.button("Afficher")
    if show:
        # Afficher le contenu du fichier dans l'application
        components.html(contenu, height=1000, scrolling=True)

        if st.button("Fermer"):
            components.html(contenu, height=0, scrolling=False)
