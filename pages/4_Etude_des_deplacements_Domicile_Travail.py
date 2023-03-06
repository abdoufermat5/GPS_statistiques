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
trajectories = []
# Sans domicile-travail
uri = 'mongodb+srv://admin:uvsqawsgroupe17@cluster0.nkdni.mongodb.net/?retryWrites=true&w=majority'
myclient = pymongo.MongoClient(uri)

mydb = myclient["DonneeGPS"]
mycol = mydb["DATAGPS"]


x = mycol.find({'USER_ID': '000'})
df_plot = pd.DataFrame.from_dict(x)
df_plot.SOUS_TRAJET[0]

for trajet in df_plot.SOUS_TRAJET.tolist():
    trajectories.append(trajet[0]["DEPART"] + [1])
    trajectories.append(trajet[0]["ARRIVE"] + [1])

data = pd.DataFrame(trajectories)
data.columns = ["latitude","longitude","count"]

fig = px.density_mapbox(data, lat='latitude', lon='longitude', z='count',
                        mapbox_style="stamen-terrain")

st.write(fig)

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
    folium.CircleMarker(center, radius=40, color=center_colors[i],fill=True).add_to(m)

st.write(m)
