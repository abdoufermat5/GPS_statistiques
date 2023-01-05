import streamlit as st
import streamlit.components.v1 as components
from gps_uvsq_utils.st_helpers import load_sidebar_footer, load_assets

# Main objective page
load_assets()
load_sidebar_footer("Objectifs", "flag_circle")
st.title("Objectifs du projet")
st.markdown("""
<h5 class="text-primary"><u>Generer les labels</u></h5>
<p>
L'un des objectifs de ce projet consiste en l'attribution d'un mode de transport correspondant au 
trajets. Cette information peut amener une notion de déplacement "Verte", si nous détectons des trajets réalisés à 
pied ou a vélo plut qu'en engin motorisé. Comme expliqué précédemment, chaque dossier user contient une liste de 
trajectoires avec autant de fichiers correspondant. Certains de ces dossiers d'utilisateur contiennent un fichier 
**labels.txt**. Ce fichier présent pour 69 des 182 utilisateurs contient pour chaque ligne une <b>date de 
début</b>, <b>de fin</b> et un <b>mode de transport</b>. Une fois ces lignes récupérés, on vient générer un 
DataFrame englobant les lignes de tous les fichiers avec les ID des utilisateurs correspondant à chaque trajet.
</p>""", unsafe_allow_html=True)