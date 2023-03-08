import streamlit as st
import streamlit.components.v1 as components
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

st.markdown("""
<br/>
<div class="card border shadow">
<div class="card-body"> En conclusion, notre travail avait pour objectifs de prétraiter le jeu de données Geolife, 
de déterminer les modes de transport utilisés par les utilisateurs, de stocker les données de manière organisée dans 
une base de données MongoDB, d'identifier les trajets domicile-travail et de créer des profils de personnes en 
fonction de leurs habitudes de déplacement. Ces objectifs ont été atteints en utilisant des méthodes heuristiques 
(règle basé sur la vitesse et le temps pour determiner les trajets, inference type transport, clustering) qui 
nous ont permis d'extraire des informations pertinentes à partir des données GPS collectées. 
</div>
</div>""", unsafe_allow_html=True)
