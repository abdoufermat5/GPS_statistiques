import streamlit as st
import streamlit.components.v1 as components
from gps_uvsq_utils.st_helpers import load_sidebar_footer, load_assets

st.set_page_config(
    page_title="Objectifs",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Main objective page
load_assets()
load_sidebar_footer("Objectifs", "flag_circle")

st.markdown("""<h2 class="text-center" style="background-color:#cad2e0">Objectifs du projet</h2>""", unsafe_allow_html=True)
st.markdown("---")
# enumerer les objectifs du projet avec des puces
st.markdown("""

<div class="card border shadow">
<div class="card-body">
Le premier objectif de notre travail a été d'effectuer un prétraitement du jeu de données Geolife afin 
de faciliter son analyse ultérieure. Ce prétraitement a consisté à regroupé les relevés GPS en des trajets.
Pour cela nous avons appliquer un ensemble de règles de séparation basé sur le temps et la vitesse. Cela nous a permis 
d'avoir des trajets plus cohérents et plus facilement analysables.
</div>
</div>
<br/>
""", unsafe_allow_html=True)

st.markdown("""
```python
REGLE_TEMPS = 10 * 60  # 10 minutes
REGLE_VITESSE =   {
        "upper": 2, # 2 km/h
        "lower": -2 # -2 km/h
    }
```
""")

st.markdown("""
<div class="card border shadow">
<div class="card-body">
Ensuite, nous avons cherché à déterminer les différents types de transport utilisés par les personnes dans les 
trajectoires. Pour cela, nous avons utilisé une methode heuristique qui consiste à inférer le mode de transport à 
partir de la vitesse moyenne du trajet. Nous sommes partis du principe que les trajets effectués à pied ou à vélo ont 
par exemple une vitesse moyenne inférieure à 10 km/h et 20km/h respectivement, alors que les trajets effectués en 
voiture ont une vitesse moyenne entre 20 et 80 km/h. Nous avons ainsi créé des labels pour chaque trajet, en fonction 
du mode de transport utilisé. Cette classification nous a permis d'obtenir une vision globale des modes de transport 
préférés dans les déplacements de la population étudiée. 
</div>
</div>
<br/>
""", unsafe_allow_html=True)
st.markdown("""
```python
M_VITESSE = {
        "marche": {
            "min": 0,
            "max": 10
        },
        "velo": {
            "min": 10,
            "max": 20
        },
        "voiture/bus/taxi": {
            "min": 20,
            "max": 80
        },
        "train": {
            "min": 80,
            "max": 580
        },
        "airplane": {
            "min": 580,
            "max": 920
        },
        "other": {
            "min": -1,
            "max": -1
        }
    }
""")

st.markdown("""
<div class="card border shadow">
<div class="card-body">
Nous avons donc créé une base de données MongoDB pour stocker les données de manière organisée et facilement 
accessible pour les traitements ultérieurs.
</div>
</div>
<br/>
<div class="card border shadow">
<div class="card-body">
Un autre objectif a été d'identifier les trajets domicile-travail effectués par les utilisateurs. 
Dans cette partie également nous avons adopté une approche heuristique. Nous avons cherché à identifier les trajets
domicile-travail en utilisant les données de localisation des utilisateurs. Un trajet domicile-travail pour un utilisateur
donné est représenté par les deux clusters les plus chargés de points de localisation. Nous avons donc cherché à
identifier ces deux clusters.
</div>
</div>
<br/>
<div class="card border shadow">
<div class="card-body">
Enfin le dernier objectif de notre travail consistait à créer des profiles de personnes en fonction de leurs trajets et
de leurs modes de transport. 
</div>
</div>
""", unsafe_allow_html=True)

