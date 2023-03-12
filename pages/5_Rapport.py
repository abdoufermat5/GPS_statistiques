import os

import streamlit as st
from PIL import Image

from gps_uvsq_utils.st_helpers import load_assets, load_sidebar_footer

st.set_page_config(
    page_title="Rapport",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Main objective page
load_assets()
load_sidebar_footer("Rapport", "area_chart")
st.markdown("""<h2 class="text-center" style="background-color:#cad2e0">Rapport du Projet</h2>""", unsafe_allow_html=True)

st.markdown("""
<br/>
<div class="card border shadow">
<div class="card-body text-dark"> 
    Dans cette partie de notre application web, nous avons regroupé tous les détails du projet sous forme de rapport. 
    Ce rapport contient une section sur les difficultés et challenges techniques rencontrés pendant le développement du projet ainsi que les solutions apportées pour les surmonter. 
    Une autre section est consacrée à l'implémentation du projet, y compris les outils logiciels utilisés pour sa réalisation. 
    Enfin, nous avons également rendu disponible le code source du projet et expliqué comment il peut être utilisé si vous souhaitez vous en servir. 
</div>
</div>""", unsafe_allow_html=True)

def presentation():
    # PRÉSENTATION DU JEUX DE DONNÉES #
    st.markdown("""
    <br/>
    <div class="card border shadow">
    <div class="card-body text-dark"> 
        <h2 style="text-decoration: underline;">Jeux de données</h2>
        Une fois que les fichiers ont été téléchargé via Geolife, nous avons obtenue l'arborescence de fichier suivante :
    </div>
    </div>""", unsafe_allow_html=True)

    above_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    path_dir = os.path.join(above_path, "html", 'assets', 'Arborescence_Data.png')

    col1, col2 = st.columns(2)
    image = Image.open(path_dir)
    with col1:
        st.markdown("""<br/>""", unsafe_allow_html=True)
        st.image(image, caption='Arborescence du jeux de données', use_column_width=True)
    with col2:
        st.markdown("""
        <br/>
            <div class="card border shadow">
                <div class="card-body text-dark">
                    <li> Les chiffres important à noté sont qu'on a un total de :
                        <ul>
                          <li>182 dossiers utilisateurs</li>
                          <li>
                            17 621 fichiers .plt
                            <br/>
                            Ces fichiers présent pour 69 des 182 utilisateurs contient pour chaque ligne une date de début, de fin et un mode de transport.
                          </li>
                        </ul>
                    </li>
                    <li>Légende :
                        <ul>
                          <li>Un fichier .plt correspond au trajet d'un utilisateur</li>
                          <li>Un fichier Label.txt correspond à la l'étiquetage d'un trajet d'un utilisateur</li>
                        </ul>
                    </li>
                </div>
            </div>
            <br/>
    """, unsafe_allow_html=True)

def difficultes():
# DIFFICULTÉS TECHNIQUES #
    st.markdown("""
    <br/>
    <div class="card border shadow">
    <div class="card-body text-dark"> 
        <h2 style="text-decoration: underline;">Les difficultés techniques</h2>
        Dans cette partie de notre application web, nous avons regroupé tous les détails du projet sous forme de rapport. 
        Ce rapport contient une présentation du jeux de données, une section sur les difficultés et challenges techniques rencontrés pendant le développement du projet ainsi que les solutions apportées pour les surmonter. 
        Une autre section est consacrée à l'implémentation du projet, y compris les outils logiciels utilisés pour sa réalisation. 
        Enfin, nous avons également rendu disponible le code source du projet et expliqué comment il peut être utilisé si vous souhaitez vous en servir. 
    </div>
    </div>""", unsafe_allow_html=True)

def solutions():
    # SOLUTIONS #
    st.markdown("""
    <br/>
    <div class="card border shadow">
    <div class="card-body text-dark"> 
        <h2 style="text-decoration: underline;">Les solutions apportées</h2>
        <h4 style="text-decoration: underline;">A) Générer les labels</h4>
        Après l'analyse du Dataset qui nous était fourni, nous nous sommes aperçu, que les trajets n'étaient pas tous étiquetté. 
        L'un des objectifs de ce projet consiste en l'attribution d'un mode de transport correspondant au trajets. 
        Cette information peut amener une notion de déplacement "Verte", si nous détectons des trajets réalisés à pied ou a vélo plut qu'en engin motorisé.
        <br/>
        En revanche, après avoir consulté et traité les données, nous sommes arrivés à la conclusion qu'utiliser ces données n'allait pas avoir de grandes utilités pour notre projet. 
        En effet, les différents trajets dans les trajectoires n'ont pas de références (Id). La seule manière d'attribuer un mode de transport à partir des données existantes serait 
        depuis la date de fin et d'arrivée. Cependant, après notre traitement, nous avons séparé les différentes trajectoires en plusieurs trajets selon une séparation de temps fixe. 
        Comme dans la figure ci-dessous, on remarque d'une part que certains trajets ont des temps aberrants (24h pour certains) mais on peut aussi noter le fait que nous avons les labels 
        pour 14 700 trajets alors que notre base en contient plus de 400 000.
    
    </div>
    </div>""", unsafe_allow_html=True)
    above_path2 = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    path_dir2 = os.path.join(above_path2, "html", 'assets', 'df_labels.png')

    col1, col2, col3 = st.columns(3)
    image2 = Image.open(path_dir2)
    with col1:
        pass
    with col2:
        st.markdown("""<br/>""", unsafe_allow_html=True)
        st.image(image2, caption='Extrait de la base de données', use_column_width=True)
    with col3:
        pass

def implementation():
    # IMPLÉMENTATION (outil logiciels) #
    st.markdown("""
    <br/>
    <div class="card border shadow">
        <div class="card-body text-dark"> 
            <h2 style="text-decoration: underline;">Implémentation</h2>
            En prenant en considération la difficulté du sujet ainsi que du langage de programmation le plus adapté 
            pour répondre aux besoins, nous avons fait le choix de s'orienter vers le langage Python. La richesse des
            bibliothèques disponibles en Python a été un point important dans l'implémentation du projet.
            <br/>
            <li>Nous avons utiliser principalement les outils suivants :
                <ul>
                  <li><strong>MongoDB</strong></li>
                  <li><strong>Pymongo</strong></li>
                  <li><strong>Panda</strong></li>
                  <li><strong>Geopy</strong></li>
                  <li><strong>Folium</strong></li>
                  <li><strong>Plotly</strong></li>
                  <li><strong>Streamlit</strong></li>
                </ul>
            </li>
        </div>
    </div>""", unsafe_allow_html=True)

def github():
    # DISPONIBILITÉ DU CODE GITHUB #
    st.markdown("""
    <div class="card border shadow">
    <div class="card-body text-dark"> 
        <h2 style="text-decoration: underline;">Github</h2>
        <a href="https://github.com/abdoufermat5/GPS_statistiques">Github du Projet</a>
        <br/>
        Afin de collaborer et de partager les différents fichiers de code source entre les membres du groupes,
        nous avons utilisé GitHub. Le projet informatique est hebergé sur un dépôt publique, ce qui permet la disponibilité
        de celui-ci accessible à tous.
        De ce fait, toute personne possédant le lien du Github peut se procurer les codes sources. Un README à été
        ajouté pour expliquer comment installer et lancer le projet si l'on veut s'en servir.
    </div>
    </div>""", unsafe_allow_html=True)
    above_path3 = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    path_dir3 = os.path.join(above_path3, "html", 'assets', 'Github.png')

    col1, col2 = st.columns(2)
    image3 = Image.open(path_dir3)
    with col1:
        st.markdown("""<br/>""", unsafe_allow_html=True)
        st.image(image3, caption='Logo Github',use_column_width=True)
    with col2:
        st.markdown("""
        <br/>
            <div class="card border shadow">
                <div class="card-body text-dark">
                    <li>Les liens Github des différents membre du projet :
                        <ul>
                            <li><a href="https://github.com/samkal26">Samuel KALFON</a></li>
                            <li><a href="https://github.com/samkal26">Gwennaël CANNENPASSE</a></li>
                            <li><a href="https://github.com/uvsq21805057">Johann RAMANANDRAITSIORY</a></li>
                            <li><a href="https://github.com/abdoufermat5">Abdou Yaya SADIAKHOU</a></li>
                        </ul>
                    </li>
                </div>
            </div>
            <br/>
        """, unsafe_allow_html=True)

def main():
    st.markdown("""
    <br/>
    <div class="card border shadow">
        <div class="card-body text-dark">
        ️️ ✍️ Veuillez sélectionner un chapitre du Rapport ✍️
        </div>
    </div>
    <br/>
    """, unsafe_allow_html=True)

    # Définir le nombre de colonnes
    col1, col2, col3, col4, col5 = st.columns(5)

    if col1.button('Jeux de données'):
        presentation()

    if col2.button('Les difficultés techniques'):
        difficultes()

    if col3.button('Les solutions apportées'):
        solutions()

    if col4.button('Implémentation'):
        implementation()

    if col5.button('Disponibilité du code'):
        github()

if __name__ == "__main__":
    main()