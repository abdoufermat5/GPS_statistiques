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
    # DETECTION DES TRAJETS #
    st.markdown("""
    <br/>
    <div class="card border shadow">
    <div class="card-body text-dark"> 
        <h2 style="text-decoration: underline;">Les difficultés techniques</h2>
        Nous allons dans cette partie du rapport, détailler les différentes difficultés auxquelles 
        nous nous sommes confrontés.
        <h4 style="text-decoration: underline;">A) Détection des trajets</h4>
        Une première interprétation d'un fichier .plt est d'admettre que celui-ci représente un trajet.
        Ce qui est le cas, cependant, en analysant davantage le contenue on remarque qu'il est possible
        de trouver plusieurs trajets au sein même d'un seul fichier .plt.
        C'est pourquoi, la détection clair et précise des différents trajet pour un utilisateur à été une 
        étape importante à résoudre.
    </div>
    </div>""", unsafe_allow_html=True)

    # DETECTION DES TYPE-TRANSPORT #
    st.markdown("""
    <br/>
    <div class="card border shadow">
    <div class="card-body text-dark"> 
        <h4 style="text-decoration: underline;">B) Détection des labels "transport"</h4>
        Après l'analyse du Dataset qui nous était fourni, nous nous sommes aperçu, que les trajets n'étaient pas tous étiquetté. 
        L’un des objectifs de ce projet consiste en l’attribution d’un mode de transport correspondant au trajets.
        Cette information peut amener une notion de déplacement ”Verte”, si nous détectons des trajets réalisés à
        pied ou a vélo plut qu’en engin motorisé. Au vue de l'inégalité de répartition des fichiers "label.txt",
        nous avons du trouver une méthode générale afin d'ajouter un label de type transport pour tous les trajets.
        <br/><br/>
        En revanche, après avoir consulté et traité les données, nous sommes arrivés à la conclusion 
        qu'utiliser ces données n'allait pas avoir de grandes utilités pour notre projet. 
        En effet, les différents trajets dans les trajectoires n'ont pas de références (Id). 
        La seule manière d'attribuer un mode de transport à partir des données existantes serait 
        depuis la date de fin et d'arrivée. Cependant, après notre traitement, nous avons séparé 
        les différentes trajectoires en plusieurs trajets selon une séparation de temps fixe. 
        Comme dans la figure ci-dessous, on remarque d'une part que certains trajets ont des temps 
        aberrants (24h pour certains) mais on peut aussi noter le fait que nous avons les labels 
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
        st.image(image2, caption='Extrait du fichier .plt déjà labélisé', use_column_width=True)
    with col3:
        pass

    # DETECTION DES TYPE-TRANSPORT SOUS-TRAJETS #
    st.markdown("""
    <br/>
    <div class="card border shadow">
    <div class="card-body text-dark"> 
        <h4 style="text-decoration: underline;">C) Sous-trajets et labels "transport"</h4>
        Une fois que la règle de vitesse a été établit, il est simple d'identifier le moyen de déplacement utilisé.
        Cependant, il est possible que pour un trajet, un utilisateur emploi différents type de transport.
        <br/>
        <strong>Exemple : Il part de chez lui à pied, puis prend le bus avant d'arriver au travail.</strong>
        <br/>
        Par conséquent, pour analyser si un trajet à été réalisé à l'aide de plusieurs moyens de transport,
        il faut identifier les sous-trajets présent dans ce même trajet.
    </div>
    </div>""", unsafe_allow_html=True)

def solutions():
    # SOLUTIONS #
    # IDENTIFICATION DES TRAJETS #
    st.markdown("""
    <br/>
    <div class="card border shadow">
    <div class="card-body text-dark"> 
        <h2 style="text-decoration: underline;">Les solutions apportées</h2>
        <h4 style="text-decoration: underline;">A) Identification des trajets</h4>
        Afin de résoudre le problème d'identification des trajets, nous avons stocké
        tous les relevés des fichiers .plt pour chaque utilisateur dans un DataFrame Panda.
        Le DataFrame nous a permis une meilleure manipulation des données. La détection de trajet
        se traduit par une règle de séparation de temps que nous avons établit.
        <br/> Cette règle est la suivante : <br/>
        <strong>Soit deux relevés consécutif ayant une différence de temps supérieur a 10 minutes alors chacun de ces deux relevés est un trajet diffèrent.</strong>
    </div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<br/>""", unsafe_allow_html=True)
        code = '''def regle_temps():
        date1 = dataframe.iloc[i]['Date'] + "/" + dataframe.iloc[i]['Horaire']
        date2 = dataframe.iloc[i + 1]['Date'] + "/" + dataframe.iloc[i + 1]['Horaire']

        time_1 = datetime.strptime(date1.strip(), "%Y-%m-%d/%H:%M:%S")
        time_2 = datetime.strptime(date2.strip(), "%Y-%m-%d/%H:%M:%S")
        rule1 = timedelta(minutes=10)
        duration = time_2 - time_1'''
        st.code(code, language='python')
    with col2:
        st.markdown("""
        <br/>
            <div class="card border shadow">
                <div class="card-body text-dark">
                Pour illustrer cette méthode, nous pouvons observer l'extrait de code ci-contre.
                Soit deux revelés <strong>(time_1 et time_2)</strong>, si on a une difference d'horaire
                <strong>(duration)</strong> superieur a 10min<strong>(rule1)</strong> alors nous avons un 2 trajets distincs.
                </div>
            </div>""", unsafe_allow_html=True)

    # IDENTIFICATION LABEL TRANSPORT #
    st.markdown("""
    <br/>
    <div class="card border shadow">
        <div class="card-body text-dark">
            <h4 style="text-decoration: underline;">B) Identification du label "transport"</h4>
            Pour résoudre ce problème, nous n'avons donc pas utilisé les données labéllisé.
            Pour ce faire, nous avons appliquer les règles décrite dans la partie <strong>Prétraitement</strong>.
        </div>
    </div>""", unsafe_allow_html=True)

    # IDENTIFICATION SOUS-TRAJETS #
    st.markdown("""
    <br/>
    <div class="card border shadow">
        <div class="card-body text-dark">
            <h4 style="text-decoration: underline;">C) Identification des sous-trajets</h4>
            Dans le but de récupérer les sous-trajets détecter à l'intérieur d'un trajet principale,
            nous avons créer une nouvelle colonne dans notre base de données. Celle-ci se nomme 
            <strong>SOUS_TRAJETS</strong> et est assigné à chaque trajets distincts
            (colonne <strong>TRAJET_ID</strong> de la base de données). Le fait d'avoir pour un tuple,
            ces deux éléments permet de mieux comprendre l'analyse du chemin effectué pour un utilisateur.
            <br/>
            De plus, il faut noter que chaque <strong>SOUS_TRAJETS</strong> contient un tableau 
            <strong>List_Point</strong> qui représente les points de coordonnées GPS du sous-trajets.
            Ces listes de points nous permettrons donc de calculer à nouveau la distance et la vitesse pour
            chaque sous-trajet. En d'autre termes, l'étiquette de type-transport pourra être ajouté et donc 
            nous pourrons préciser s'ils existent, les différents outils de transport employé pour un même trajet.
        </div>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    above_pathMongo2 = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    path_dirMongo2 = os.path.join(above_pathMongo2, "html", 'assets', 'Mongo2.png')
    imageMongo2 = Image.open(path_dirMongo2)
    with col1:
        pass
    with col2:
        st.markdown("""<br/>""", unsafe_allow_html=True)
        st.image(imageMongo2, caption='Extrait de la base de données', use_column_width=True)
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
                  <li><strong>PyMongo</strong></li>
                  <li><strong>Pandas</strong></li>
                  <li><strong>GeoPy</strong></li>
                  <li><strong>Folium</strong></li>
                  <li><strong>Plotly</strong></li>
                  <li><strong>Streamlit</strong></li>
                </ul>
            </li>
        </div>
    </div>""", unsafe_allow_html=True)

    # MongoDB #
    st.markdown("""
        <br/>
        <div class="card border shadow">
        <div class="card-body text-dark"> 
            <h4 style="text-decoration: underline;">A) MongoDB</h4>
            Étant donné que nous avons un nombre important de données à analyser, nous avons fait
            le choix de nous orienter vers l'utilisation d'une base de données NoSQL. Cette décision
            se justifie par le fait que la structure de nos données utilise des imbrications. 
            Les données GPS peuvent être très volumineuses et nécessitent donc un stockage et 
            une récupération rapides. MongoDB est conçu pour une performance élevée et 
            peut facilement gérer de gros volumes de données.
            <br/>
            De plus, le stockage des données dans une base de données est primordiale si nous voulons
            par la suite, développer des analyses statistiques. La manipulation de requête SQL nous a 
            été utile dans la réalisation de cette mission.
        </div>
        </div>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    above_pathMongo = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    path_dirMongo = os.path.join(above_pathMongo, "html", 'assets', 'Mongo.png')
    imageMongo = Image.open(path_dirMongo)
    with col1:
        pass
    with col2:
        st.markdown("""<br/>""", unsafe_allow_html=True)
        st.image(imageMongo, caption='Extrait de la base de données', use_column_width=True)
    with col3:
        pass

    # PyMongo #
    st.markdown("""
        <br/>
        <div class="card border shadow">
        <div class="card-body text-dark"> 
            <h4 style="text-decoration: underline;">B) PyMongo</h4>
            Comme il est expliqué dans le paragraphe précédent, nous avons besoin d'une bibliothèque 
            en Python dans le but d'instancier notre base de données MongoDB mais aussi d'effectuer des
            requêtes sur celle-ci.
            <br/>
            PyMongo est un package Python qui permet de travailler avec MongoDB, la base de données
            NoSQL orientée documents. PyMongo fournit une interface simple pour communiquer avec la 
            base de données, permettant de créer, lire, mettre à jour et supprimer des documents dans 
            MongoDB. Il permet également de réaliser des opérations de requêtes et d'agrégation de données. 
            Donc, PyMongo est un outil essentiel pour développer et mettre en place ce projet.
        </div>
        </div>""", unsafe_allow_html=True)

    # Pandas #
    st.markdown("""
        <br/>
        <div class="card border shadow">
        <div class="card-body text-dark"> 
            <h4 style="text-decoration: underline;">C) Pandas</h4>
            Une fois que les informations de notre base de données ont été extrait,
            nous avons manipulé la bibliothèque open-source Pandas car elle 
            fournit des outils de manipulation et d'analyse de données.
            <br/>
            <li>Cette outils à été exploitable pour les fonctionnalités suivantes :
                <ul>
                  <li>
                    La création et la manipulation de DataFrames : une structure de données tabulaire 
                    qui peut contenir des données de différents types et tailles. Toutes les informations
                    sur les trajets d'un utilisateur sont conservé dans un DataFrame.
                  </li>
                  <li>
                    Le nettoyage et la préparation de données : Pandas offre une variété d'outils pour nettoyer 
                    et préparer les données, notamment le traitement des valeurs manquantes, la fusion et le 
                    découpage de DataFrames, la transformation de données et la suppression des doublons.
                    Dans notre cas, on peut citer l'exemple du découpage de DataFrame pour ne garder que 
                    les déplacements pour les statistiques "Écologie".
                  </li>
                  <li>
                    L'analyse de données : Pandas permet de faire des analyses statistiques sur les données 
                    telles que le calcul de la moyenne, la médiane, le mode, la variance, la corrélation et la régression.
                    Exemple : calcul des moyennes sur une année pour un utilisateur.
                  </li>
                </ul>
            </li>
        </div>
        </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<br/>""", unsafe_allow_html=True)
        code = '''def exemple(id_user)
                W000 = myclient["DonneeGPS"]["DATAGPS"].find({'USER_ID': id_user})
                df_plot_000_time = pd.DataFrame.from_dict(W000)'''
        st.code(code, language='python')
    with col2:
        st.markdown("""
                <br/>
                    <div class="card border shadow">
                        <div class="card-body text-dark">
                        Voici un extrait de code du projet montrant l'utilisation de la 
                        bibliothèque PyMongo et Pandas.
                         <li>Les tâches rempli sont :
                            <ul>
                              <li>La récupération des données de la base de données</li>
                              <li>Le transfert des informations dans un DataFrame</li>
                            </ul>
                        </li>
                        Ici <strong>id_user</strong> correspond à un numéro d'utilisateur
                        qui sert d'argument à la fonction.
                        </div>
            </div>""", unsafe_allow_html=True)

    # GeoPy #
    st.markdown("""
            <br/>
            <div class="card border shadow">
            <div class="card-body text-dark"> 
                <h4 style="text-decoration: underline;">D) GeoPy</h4>
                GeoPy est une bibliothèque Python qui permet de réaliser des opérations géospatiales, 
                comme la géocodification et la recherche de distances entre des points géographiques. 
                En d'autres termes, GeoPy permet de récupérer des informations géographiques à partir 
                d'une adresse ou d'un nom de lieu, de calculer des distances entre deux points géographiques, 
                de récupérer des coordonnées géographiques.
                Cela s'est avéré utile dans notre cas, par exemple pour la visualisation de données 
                géographiques, pour l'analyse des déplacements de personnes, notamment pour avoir les informations
                précise de point de départ ou d'arrivée pour un trajet, 
            </div>
            </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<br/>""", unsafe_allow_html=True)
        code = '''def exemple_geopy(id_user):
                # initialize Nominatim API
                geolocator = Nominatim(user_agent="geoapiExercises")
                location_dep = geolocator.reverse(str(point_depart[0]) + "," + str(point_depart[1]), language='en')
                
                address = location_dep.raw['address']
                town_dep = address.get('town', '')
                city_dep = address.get('city', '')
                
                popup_dep = ''
                if town_dep == '':
                    popup_dep = city_dep
                else:
                    popup_dep = town_dep
            '''
        st.code(code, language='python')
    with col2:
        st.markdown("""
                <br/>
                    <div class="card border shadow">
                        <div class="card-body text-dark">
                        Voici un extrait de code du projet montrant l'utilisation de la 
                        bibliothèque Geopy.
                         <li>Les différentes zones géographique récupérées sont :
                            <ul>
                              <li>Town </li>
                              <li>City</li>
                            </ul>
                        </li>
                        Ici on récupère les coordonnées du point de départ d'un trajet.
                        <strong>[(point_depart[0]),(point_depart[1])]</strong>
                        <br/>
                        Par ailleurs, l'attribut <strong>language='en'</strong> est 
                        nécessaire car nous travaillons avec des localisation de données
                        issue de Chine. Cela nous permet donc de traduire les noms des <strong>City</strong>
                        et <strong>Town</strong>.
                        </div>
            </div>""", unsafe_allow_html=True)

    # Folium #
    st.markdown("""
            <br/>
            <div class="card border shadow">
            <div class="card-body text-dark"> 
                <h4 style="text-decoration: underline;">E) Folium</h4>
                Folium est une bibliothèque Python qui permet de créer des cartes interactives en utilisant 
                les données géographiques de différentes sources (par exemple, OpenStreetMap). Elle permet de 
                créer des cartes avec des marqueurs pour représenter des points d'intérêt, et d'autres types de 
                visualisations cartographiques. Folium est facile à utiliser et fournit une interface intuitive 
                pour la création de cartes.
                Folium nous a été indispensable pour les rubriques <strong>Visualisation</strong> et 
                <strong>Etude des déplacement Domicile/Travail</strong>. Les tâches réalisées à l'aide de 
                cette librairie sont multiples. D'une part, nous pouvons tracer sur une carte intéractive,
                les différents chemins d'un utilisateur. D'autre part, nous avons réussi à illustrer 
                une carte composé des cluster des zones "chaudes", qui regroupe les déplacements 
                les plus fréquents d'un individu.
            </div>
            </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<br/>""", unsafe_allow_html=True)
        code = '''def exemple_folium():
                # Initialisation de la Map
                map_itineraire_bd = folium.Map(location=point_depart, zoom_start=13.5)
            
                # Tracer la ligne sur la Map selon le type-transport
                for i in range(len(tab_locations_ss_trajet)):
                    color_line = ""
                    if tab_transport[i] == 'voiture/bus/taxi':
                        color_line = 'black'
                    elif tab_transport[i] == 'velo':
                        color_line = 'red'
                    else:
                        color_line = 'blue'
            
                    wind_line = folium.PolyLine(tab_locations_ss_trajet[i], weight=3, color=color_line)
                    wind_line.add_to(map_itineraire_bd)
            
                # Ajout des points de départ et d'arrivée sur la Map
                map_itineraire_bd.add_child(
                    folium.Marker(location=point_depart, icon=folium.Icon(color='green', icon_color='white'), popup=popup_dep,
                                  tooltip="Départ"))
                map_itineraire_bd.add_child(
                    folium.Marker(location=point_arrivee, icon=folium.Icon(color='gray', icon_color='white'), popup=popup_arr,
                                  tooltip="Arrivée"))
            
                # Affiche la Map
                st_folium(map_itineraire_bd, width=725)
                '''
        st.code(code, language='python')
    with col2:
        st.markdown("""
                    <br/>
                        <div class="card border shadow">
                            <div class="card-body text-dark">
                            Voici un extrait de code du projet montrant l'utilisation de la 
                            bibliothèque Folium.
                            Ici, il s'agit d'un exemple pour dessiner un chemin sur une carte,
                            ainsi que d'ajouter deux points distincts, correspondant au point de départ
                            et au point d'arrivée.
                            </div>
                </div>""", unsafe_allow_html=True)

    # Plotly #
    st.markdown("""
            <br/>
            <div class="card border shadow">
            <div class="card-body text-dark"> 
                <h4 style="text-decoration: underline;">F) Plotly</h4>
                Plotly est une bibliothèque Python pour la création d'outils de visualisation de données 
                interactives. Elle a été employé dans le but de créer des graphiques interactifs et 
                des visualisations de  nos données. Notamment pour les différents graphiques présents
                dans la section <strong>Visualisation</strong>. De surcroît, Plotly offre la possibilité
                d'utiliser plusieurs type de graphique. C'est pourquoi, selon le type d'analyse effectué,
                la visualisation des données change de modèle. Pour exprimer une répartition, un modèle
                Pie Chart est plus approprié, tandis que pour visualiser des valeurs numériques de distance, 
                un Plot Bar est le mieux adapté.
            </div>
            </div>""", unsafe_allow_html=True)

    # Streamlit #
    st.markdown("""
            <br/>
            <div class="card border shadow">
            <div class="card-body text-dark"> 
                <h4 style="text-decoration: underline;">G) Streamlit</h4>
                Streamlit est une bibliothèque open-source en Python qui nous a offert la possibilité de créer 
                l'applications web de manière interactive et intuitive. Cela nous a permis de développer ce tableau
                de bord tout en y introduisant de nombreux éléments comme les graphique ou encore les cartes de
                localisation. En effet, Streamlit possède des fonctions prête à l'emploi pour créer des graphiques, 
                des cartes tout en utilisant les mêmes bibliothèque que nous avons sélectionnées. 
                <strong>(Exemple : Plotly et Folium)</strong>
                <br/>
                Enfin, ce package propose de nombreux widget ou boutons qui ont rendu le design de l'application
                web hiérarchisé et structuré.
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