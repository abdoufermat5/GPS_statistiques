import io
import os
import glob
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from gps_uvsq_utils.gps_helpers import calc_distance_parcouru_entre_2_coordonnees
from gps_uvsq_utils.st_helpers import load_assets, load_sidebar_footer, display_info, display_k_rows, display_bar_chart

import plotly.express as px

def creation_dataframe_fichier(file):
    # remove last 4 characters of the string
    string = file 
    string = string[:-2]
    data = io.StringIO(string)
    df = pd.read_csv(data,
                     header=None,
                     sep=',',
                     skiprows=6,
                     usecols=[0, 1, 3, 5, 6],
                     names=["latitude", "longitude", "altitude", "date", "horaire"])
    return df

st.set_page_config(
    page_title="Etude des déplacements Domicile/Travail",
    page_icon="🎢",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Main objective page
load_assets()
load_sidebar_footer("Etude des déplacements Domicile/Travail", "area_chart")
st.title("Etude des déplacements Domicile/Travail")

import streamlit as st

# Créer un widget de téléversement de fichiers
fichier_televerse = st.file_uploader("Sélectionnez un fichier markdown à téléverser")

# Vérifier si un fichier a été téléversé
if fichier_televerse:
    # Lire le contenu du fichier
    contenu = fichier_televerse.read().decode("utf-8")

    df = creation_dataframe_fichier(contenu)
    df["count"] = [1 for i in range(len(df.values.tolist()))]
    print(df)
    fig = px.density_mapbox(df, lat='latitude', lon='longitude', z='count',
                        mapbox_style="stamen-terrain")
    st.write(fig)

    # Créer un bouton "Afficher"
    show = st.button("Afficher")
    if show:
        # Afficher le contenu du fichier dans l'application
        components.html(contenu, height=1000, scrolling=True)

        if st.button("Fermer"):
            components.html(contenu, height=0, scrolling=False)
