import pymongo
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from gps_uvsq_utils.st_helpers import load_sidebar_footer, load_assets
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import folium

st.set_page_config(
    page_title="Visualisation des données",
    page_icon="🎡",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Main objective page
load_assets()
load_sidebar_footer("Visualisation", "query_stats")
st.markdown("""<h2 class="text-center" style="background-color:#cad2e0">Visualisation d'un Trajet</h2>""", unsafe_allow_html=True)

uri = 'mongodb+srv://admin:uvsqawsgroupe17@cluster0.nkdni.mongodb.net/?retryWrites=true&w=majority'
myclient = pymongo.MongoClient(uri)

mydb = myclient["DonneeGPS"]
mycol = mydb["DATAGPS"]
mycol2 = mydb["DATATEST"]
def map_trajet(id_user,num_trajet):
    if id_user == '000':
        id_user = '001'

    x = mycol.find({'USER_ID': id_user})
    x_bis = mycol2.find({'USER_ID': id_user,'TRAJET_ID':num_trajet})
    df_plot = pd.DataFrame.from_dict(x)
    df_plot_bis = pd.DataFrame.from_dict(x_bis)

    # initialize Nominatim API
    geolocator = Nominatim(user_agent="geoapiExercises")
    tab_locations_ss_trajet = []
    tab_transport = []

    for i in range(len(df_plot_bis.SOUS_TRAJET)):
        print(type(df_plot_bis.SOUS_TRAJET[i]))
        tab_locations_ss_trajet.append(df_plot_bis.SOUS_TRAJET[i][0].get("List_Point"))

        # print("##################" + df_plot.SOUS_TRAJET[num_trajet][i].get('TYPE-TRANSPORT'))
        tab_transport.append(df_plot.SOUS_TRAJET[i][0].get('TYPE-TRANSPORT'))

    print("#############################\n")
    print((df_plot.SOUS_TRAJET[i][0].get('List_Point')))
    # Point de départ
    point_depart = tab_locations_ss_trajet[0][0]

    location_dep = geolocator.reverse(str(point_depart[0]) + "," + str(point_depart[1]), language='en')
    address = location_dep.raw['address']
    town_dep = address.get('town', '')
    city_dep = address.get('city', '')
    popup_dep = ''
    if town_dep == '':
        popup_dep = city_dep
    else:
        popup_dep = town_dep

    # Point d'arrivée
    buff_size = len(tab_locations_ss_trajet) - 1
    buff_size2 = len(tab_locations_ss_trajet[buff_size]) - 1
    point_arrivee = tab_locations_ss_trajet[buff_size][buff_size2]

    location_arr = geolocator.reverse(str(point_arrivee[0]) + "," + str(point_arrivee[1]), language='en')
    address2 = location_arr.raw['address']
    town_arr = address2.get('town', '')
    city_arr = address2.get('city', '')
    popup_arr = ''
    if town_arr == '':
        popup_arr = city_arr
    else:
        popup_arr = town_arr

    # Initialisation de la Map
    map_itineraire_bd = folium.Map(location=point_depart, zoom_start=13.5)

    # Tracer la ligne sur la Map

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


    map_itineraire_bd.add_child(
        folium.Marker(location=point_depart, icon=folium.Icon(color='green', icon_color='white'), popup=popup_dep,
                      tooltip="Départ"))
    map_itineraire_bd.add_child(
        folium.Marker(location=point_arrivee, icon=folium.Icon(color='gray', icon_color='white'), popup=popup_arr,
                      tooltip="Arrivée"))

    st_folium(map_itineraire_bd, width=725)

def main():
    st.markdown("""

    <div class="card border shadow">
        <div class="card-body text-dark">
            Cette section permet de visualiser un trajet présent dans notre base de données.
        </div>
    </div>
    <br/>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="card border shadow">
            <div class="card-body text-dark">
            ⚠️ Veuillez sélectionner un utilisateur avant de choisir un trajet ⚠️
            </div>
        </div>
        <br/>
        <br/>
        """, unsafe_allow_html=True)

    users = myclient["DonneeGPS"]["DATATEST"].distinct("USER_ID")
    attribute = st.selectbox("Choisir l'user", users)

    num_trajet = myclient["DonneeGPS"]["DATATEST"].find({'USER_ID': attribute}).distinct("TRAJET_ID")
    print (myclient["DonneeGPS"]["DATATEST"].find({'USER_ID': attribute}).distinct("TRAJET_ID"))
    attribute_trajet = st.selectbox("Choisir le trajet", num_trajet)

    col1, col2 = st.columns(2)
    with col1:
        map_trajet(attribute,attribute_trajet)
    with col2:
        st.markdown("""
        <div class="card border shadow">
            <div class="card-body text-dark">
            Afin d'étendre l'analyse nous avons expérimenté plusieurs domaines d'études.
            <br/>
            <li>Légende :
                <ul>
                  <li>Le point <span style="color:green;">Vert</span> correspond au point de départ de l'utilisateur</li>
                  <li>Le point <span style="color:gray;">Gris</span> correspond au point de d'arrivée de l'utilisateur</li>
                  <li>Un tracé <span style="color:blue;">Bleu</span> indique un trajet effectué à pied</li>
                  <li>Un tracé <span style="color:red;">Rouge</span> indique un trajet effectué à vélo</li>
                  <li>Un tracé <strong>Noir</strong> indique un trajet effectué en voiture, en bus ou alors en taxi</li>
                </ul>
            </li>
            </div>
        </div>
        <br/>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
