import io
import os
import glob
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from gps_uvsq_utils.gps_helpers import calc_distance_parcouru_entre_2_coordonnees
from gps_uvsq_utils.st_helpers import load_assets, load_sidebar_footer, display_info, display_k_rows, display_bar_chart

import pymongo 
import numpy as np
import math
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Etude des déplacements Domicile/Travail",
    page_icon="🎢",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Main objective page
load_assets()
load_sidebar_footer("Etude des déplacements Domicile/Travail", "area_chart")
st.markdown("""<h2 class="text-center" style="background-color:#cad2e0">Etude des déplacements Domicile/Travail</h2>""", unsafe_allow_html=True)

def funct(users):
    def get_distance(coord1, coord2):
        """
        Calculates the distance between two coordinates on the surface of a sphere using the Haversine formula.

        Args:
        coord1 (tuple): A tuple representing the (latitude, longitude) coordinates of the first point.
        coord2 (tuple): A tuple representing the (latitude, longitude) coordinates of the second point.

        Returns:
        float: The distance between the two points in meters.
        """
        # Convert the coordinates from degrees to radians
        lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
        lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Radius of the Earth in kilometers
        distance = c * r * 1000  # Convert to meters

        return distance

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

    trajectories = []
    # Sans domicile-travail
    uri = 'mongodb+srv://admin:uvsqawsgroupe17@cluster0.nkdni.mongodb.net/?retryWrites=true&w=majority'
    myclient = pymongo.MongoClient(uri)

    mydb = myclient["DonneeGPS"]
    mycol = mydb["DATAGPS"]


    x = mycol.find({'USER_ID': users})
    df_plot = pd.DataFrame.from_dict(x)

    for trajet in df_plot.SOUS_TRAJET.tolist():
        trajectories.append(trajet[0]["DEPART"] + [1])
        trajectories.append(trajet[0]["ARRIVE"] + [1])

    data = pd.DataFrame(trajectories)
    data.columns = ["latitude","longitude","count"]

    fig = px.density_mapbox(data, lat='latitude', lon='longitude', z='count',
                            mapbox_style="stamen-terrain")
    
    st.header("Density Map (coordonées)")
    st.write("""Ci-dessous se trouve la "Heatmap" des différents points de départs et arrivées de l'utilisateur sur toutes les trajectoires chargées.
    Nous considérons chaque point comme une entité singulière avec ses coordonnées en latitude et longitude. De ce fait, des clusters de positions vont se former selon la valeur de zoom sur la map ce qui va faire ressortir différents niveau d'aggrégat d'emplacements""")
    st.write("""Par exemple : pour un utilisateur donnée au zoom minimal, nous pouvons remarquer un seul cluster principal en Chine, puis en zoomant sur la Chine nous pouvons distinctement remarquer deux zones de démarcations sur 2 principales villes puis sur des quartiers, des rues, etc...""")
    st.plotly_chart(fig)

    coordinates = [val[:2] for val in data.values.tolist()]

    # Set the radius of the clusters
    cluster_radius = 30

    # Create a list to store the coordinates that will be used for clustering
    clustering_coordinates = coordinates.copy()

    # Initialize a list to store the clusters
    clusters = []

    # Iterate through the coordinates and create clusters until all coordinates have been assigned to a cluster
    while len(clustering_coordinates) > 0:
        # Initialize a new cluster
        new_cluster = []

        # Choose a random coordinate from the remaining clustering_coordinates
        current_coord = clustering_coordinates[np.random.randint(len(clustering_coordinates))]

        # Add the current coordinate to the new cluster
        new_cluster.append(current_coord)

        # Remove the current coordinate from the remaining clustering_coordinates
        clustering_coordinates.remove(current_coord)

        # Initialize a list to store the coordinates that are within the cluster radius of the current coordinate
        close_coordinates = []

        # Iterate through the remaining clustering_coordinates and add any coordinates that are within the cluster radius of the current coordinate to the close_coordinates list
        for coord in clustering_coordinates:
            if get_distance(coord, current_coord) <= cluster_radius:
                close_coordinates.append(coord)

        # Add the close_coordinates to the new cluster
        new_cluster.extend(close_coordinates)

        # Remove the close_coordinates from the remaining clustering_coordinates
        clustering_coordinates = [x for x in clustering_coordinates if x not in close_coordinates]

        # Add the new cluster to the clusters list
        clusters.append(new_cluster)

    from geopy.point import Point

    def get_centroid(cluster):
        lat = []
        long = []
        for coord in cluster:
            lat.append(coord[0])
            long.append(coord[1])
        return [round(sum(lat)/len(lat),7),round(sum(long)/len(long),7)]

    def get_top_n_clusters(clusters,n):
        return sorted(clusters, key=lambda x: len(x),reverse = True)[:n]

    top_2_clusters = get_top_n_clusters(clusters,2)
    centers = [get_centroid(cluster) for cluster in top_2_clusters]

    m = folium.Map(location=centers[0], zoom_start=13)

    cluster_colors = ["red","blue"]
    for coord in coordinates:
        if coord in top_2_clusters[0]:
            folium.CircleMarker(coord, radius=5, color=cluster_colors[0],fill=True).add_to(m)
        elif coord in top_2_clusters[1]:
            folium.CircleMarker(coord, radius=5, color=cluster_colors[1],fill=True).add_to(m)
        else:
            folium.CircleMarker(coord, radius=2, color="black",fill=True).add_to(m)

    center_colors = ["purple","yellow"]
    for i,center in enumerate(centers):
        folium.CircleMarker(center, radius=30, color=center_colors[i],fill=True).add_to(m)

    st.header("Calcul des positions domicile-travail")
    st.write("""Vient ensuite la fonction permettant d'estimer la position du domicile et du travail de l'utilisateur. Nous sommes partis d'un postulat simple, le principe est que les deux principaux clusters de coordonnées d'un utilisateur (càd celui contenant le plus de points) étaient respectivement le domicile et le travail. 
    En revanche ces clusters sont calculées selon des paramètres et fonction précis""")

    st.subheader("Méthode de clustering")
    st.write("""Afin de calculer les différents clusters d'un utilisateur mais sans se baser sur les nombre de clusters (qu'on ne connait pas au préalable), mais sur une valeur parametrée, le rayon du cluster, pour notre cas vaut 15m (ce que l'on considère comme étant le rayon d'un lieu à l'echelle du bâtiment)
    pour exprimer la distance entre 2 points nous utilison la fonction de distance Haversine qui est tou simplement celle permettant de donner la distance entre deux points appartenant à une même sphère.
    Donc la méthode de clustering va prendre en entrée tous les points des trajectoires d'un utilisateur, puis va selecitonner aléatoirement une coordonnée et va se poser une question, existe t-il un cluster dont le centroid est à moins de 15 mètres de moi. Si cette question est répondue par l'affirmative alors le point sera assigné au cluster dont le centroid est le plus proche, sinon ce point formera un nouveau cluster.
    Le point est ensuite retiré de la liste des points disponibles à assigner.""")

    st.subheader("Résultats et affichage")
    st.write("""Nous obtenons donc plusieurs clusters de diamètre = 30m, contenant chacun 1 à n points. Nous allons ensuite les trier par nombre de points contenus en eux. une fois cette liste de clusters générées et triées
    nous allons extraire les 2 premiers élèments de la liste ce qui correspondra donc respectivement au domicile et au travail.
    Afin de visualiser ces valeurs et les comparer, nous plaçons donc sur une carte les différents points des trajectoires. Si le point n'appartient à aucun cluster, il sera noir, rouge s'il appartient au domicile et bleau pour le travail. 
    Nous affichons aussi la zone du cluster (violet,jaune) indiquant la région du lieu trouvé (domicile,travail)""")
    m.save('map.html')

    col1, col2 = st.columns(2)
    with col1:
        with open('map.html', 'r') as f:
            import streamlit.components.v1 as components
            components.html(f.read(), width=500, height=500)
    with col2:
        st.markdown("""
            <div class="card border shadow">
                <div class="card-body text-dark">
                <br/>
                <li>Légende :
                    <ul>
                      <li>Le cercle <span style="color:yellow;">Jaune</span> correspond à la zone du domicile de l'utilisateur</li>
                      <li>Le cercle <span style="color:purple;">Violet</span> correspond à la zone de travail de l'utilisateur</li>
                      <li>Les points <span style="color:blue;">Bleu</span> appartiennent à la zone du domicile</li>
                      <li>Les points <span style="color:red;">Rouge</span> appartiennent à la zone de travail</li>
                    </ul>
                </li>
                </div>
            </div>
            <br/>
            """, unsafe_allow_html=True)

def main():
    uri = 'mongodb+srv://admin:uvsqawsgroupe17@cluster0.nkdni.mongodb.net/?retryWrites=true&w=majority'
    myclient = pymongo.MongoClient(uri)
    users = myclient["DonneeGPS"]["DATAGPS"].distinct("USER_ID")

    attribute = st.selectbox("Choisir l'user", users)

    st.write("Nous venons de choisir l'id du user parmi ceux présents dans la base afin de charger toutes ses trajectoires ces données seront utilisées afin de calculer les 2 principaux clusters de la personne selon une fonction précise.")
    funct(attribute)

    st.header("Aller plus loin")
    st.write("""
    Nous obtenons des regroupements de points que nous définissons comme domicile et travail. Pour être plus précis nous donnons la positiion exacte de ces lieux en prenant le centre de ces clusters.
    Nous pouvons augmenter la confiance de la précision de la prédiction en corrélant ces points avec les horaires afin de bien séparer le domicile du travail.
    Enfin nous pouvons à présent trouver les différents moyens de transport de l'utilisateur lorsqu'il pratique son trajet domicile-travail.""")

if __name__ == "__main__":
    main()
