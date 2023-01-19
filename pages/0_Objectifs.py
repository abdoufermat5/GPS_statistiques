import streamlit as st
import streamlit.components.v1 as components
from gps_uvsq_utils.st_helpers import load_sidebar_footer, load_assets

# Main objective page
load_assets()
load_sidebar_footer("Objectifs", "flag_circle")

st.title("Objectifs du projet")
st.markdown("""
<p>
L'objectif premier est de déterminer a partir des relevés, le <b>moyen de transport utilisé</b> (marche, velo, voiture, train, avion).

Le second objectif est <b>d'identifier les trajets domiciles-travails</b>.

Enfin le troisième objectif est de <b>crée des profils de personnes</b> (classification) par rapport a leur utilisation des moyens de transport. 
</p>""", unsafe_allow_html=True)