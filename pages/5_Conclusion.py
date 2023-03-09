import os

import streamlit as st
from PIL import Image

from gps_uvsq_utils.st_helpers import load_assets, load_sidebar_footer

st.set_page_config(
    page_title="Conclusion",
    page_icon="🎢",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Main objective page
load_assets()
load_sidebar_footer("Conclusion", "area_chart")
st.markdown("""<h2 class="text-center" style="background-color:#cad2e0">Conclusion</h2>""", unsafe_allow_html=True)

# get path 1 above the current file

above_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
path_dir = os.path.join(above_path, "html", 'assets', 'architecture.png')

col1, col2, col3 = st.columns([1, 2, 1])
image = Image.open(path_dir)
with col1:
    pass
with col2:
    st.image(image, caption='Vue global', use_column_width=True)
with col3:
    pass

st.markdown("""
<br/>
<div class="card border shadow">
<div class="card-body text-dark"> En conclusion, notre travail avait pour objectifs de prétraiter le jeu de données Geolife, 
de déterminer les modes de transport utilisés par les utilisateurs, de stocker les données de manière organisée dans 
une base de données MongoDB, d'identifier les trajets domicile-travail et de créer des profils de personnes en 
fonction de leurs habitudes de déplacement. Ces objectifs ont été atteints en utilisant des méthodes heuristiques 
(règle basé sur la vitesse et le temps pour determiner les trajets, inference type transport, clustering) qui 
nous ont permis d'extraire des informations pertinentes à partir des données GPS collectées. 
</div>
</div>""", unsafe_allow_html=True)
