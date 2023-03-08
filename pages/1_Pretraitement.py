import streamlit as st
from geopy.geocoders import Nominatim

from gps_uvsq_utils.st_helpers import load_assets, load_sidebar_footer

geolocator = Nominatim(user_agent="geoapiExercises")
import pandas as pd
import geopy.distance
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Pré-traitement des données",
    page_icon="🚞",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Main objective page
load_assets()
load_sidebar_footer("Pré-traitements", "settings")
st.markdown("""<h2 class="text-center" style="background-color:#cad2e0">Les différents pré-traitement</h2>""", unsafe_allow_html=True)

global count_nbr_trajet
count_nbr_trajet = 0

global list_df
list_df = []

## Cree un data set où chaque tuple correspond a une ligne du fichier .plt
def ouverture_fichier(file):
    file_contents = file.getvalue().decode("utf-8")
    # Split the file contents into lines and extract trajectory data starting from the 7th line
    trajectory_test = [line.split(",") for line in file_contents.split("\n")[6:]]

    headers3 = ["Latitude", "Longitude", "Altitude", "Date", "Horaire"]
    df_test = pd.DataFrame(trajectory_test)
    df_test = df_test.drop([2, 4], axis=1).dropna()
    df_test.columns = headers3
    df_test['Latitude'] = df_test["Latitude"].astype(float)
    df_test['Longitude'] = df_test["Longitude"].astype(float)
    indexAge = df_test[(df_test['Latitude'] > 90)].index
    df_test.drop(indexAge, inplace=True)
    indexAge = df_test[(df_test['Latitude'] < -90)].index
    df_test.drop(indexAge, inplace=True)
    indexAge = df_test[(df_test['Longitude'] > 180)].index
    df_test.drop(indexAge, inplace=True)
    indexAge = df_test[(df_test['Longitude'] < -180)].index
    df_test.drop(indexAge, inplace=True)
    df_test.head(15)
    #print(df_test)
    return df_test

## Application de la regle de temps pour separer les trajet au sein de notre dataframe
## Soit deux revelés 2 a 2 ayant une difference d'horaire superieur a 10min alors nous avons un 2 trajets distincs
## 10min car normalement nous avons un relevé toutes les 5secondes
def regle_temps(dataframe):
    df_sep2 = pd.DataFrame()
    list_releve2 = []
    list_dataframe = []
    headers = ["Latitude", "Longitude", "Date", "Horaire"]
    for i in range(len(dataframe.index) - 1):
        date1 = dataframe.iloc[i]['Date'] + "/" + dataframe.iloc[i]['Horaire']
        date2 = dataframe.iloc[i + 1]['Date'] + "/" + dataframe.iloc[i + 1]['Horaire']

        time_1 = datetime.strptime(date1.strip(), "%Y-%m-%d/%H:%M:%S")
        time_2 = datetime.strptime(date2.strip(), "%Y-%m-%d/%H:%M:%S")
        rule1 = timedelta(minutes=10)
        duration = time_2 - time_1
        list_releve2.append(dataframe.iloc[i])
        # Si on a un ecart entre 2 releve superieur a 10 minutes alors on entre
        if duration > rule1:
            df_sep2 = pd.DataFrame(list_releve2, columns=headers)
            list_dataframe.append(df_sep2)
            df_sep2.drop(df_sep2.index, inplace=False)
            list_releve2.clear()
    list_releve2.append(dataframe.iloc[i+1])
    df_sep2 = pd.DataFrame(list_releve2, columns=headers)
    list_dataframe.append(df_sep2)
    return list_dataframe

def infer_transport(speed):
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
    if M_VITESSE["marche"]["min"] < speed <= M_VITESSE["marche"]["max"]:
        return "marche"
    elif M_VITESSE["velo"]["min"] < speed <= M_VITESSE["velo"]["max"]:
        return "velo"
    elif M_VITESSE["voiture/bus/taxi"]["min"] < speed <= M_VITESSE["voiture/bus/taxi"]["max"]:
        return "voiture/bus/taxi"
    elif M_VITESSE["train"]["min"] < speed <= M_VITESSE["train"]["max"]:
        return "train"
    elif M_VITESSE["airplane"]["min"] < speed <= M_VITESSE["airplane"]["max"]:
        return "airplane"
    else:
        return "other"

## Application de la regle de vitesse pour séparer les trajets au sein de notre dataframe
## Nous avons grouper les valeurs par 20 pour calculer une vitesse et determiner des changements de cette dernieres 2 a 2 (20 a 20)
## Si la difference de vitesse est superieur a +2 (ou -2) metre/seconde alors l'utilisateur a changé de moyen de transport et
## donc effectue un nouveau trajet
def regle_vitesse(dataframe, user_id,nbr_trajet):
    global count_nbr_trajet
    global list_df
    list_vitesse = []
    distance = 0
    i_temps = dataframe.index[0]
    compteur = 0

    ## Boucle pour calculer la vitesse entre des groupes de 60 relevés dans les data frames separer par la regle du temps
    while (i_temps < dataframe.index[-1] - 60):
        date1 = dataframe.iloc[compteur]['Date'] + "/" + dataframe.iloc[compteur]['Horaire']
        for j in range(60):
            coords_1 = (dataframe.iloc[compteur]['Latitude'], dataframe.iloc[compteur]['Longitude'])
            coords_2 = (dataframe.iloc[compteur + 1]['Latitude'], dataframe.iloc[compteur + 1]['Longitude'])
            distance += geopy.distance.geodesic(coords_1, coords_2).m
            compteur += 1
            i_temps += 1
        date2 = dataframe.iloc[compteur - 1]['Date'] + "/" + dataframe.iloc[compteur - 1]['Horaire']
        time_1 = datetime.strptime(date1.strip(), "%Y-%m-%d/%H:%M:%S")
        time_2 = datetime.strptime(date2.strip(), "%Y-%m-%d/%H:%M:%S")
        duration = time_2 - time_1
        ## calcule Vitesse en metre par seconde
        list_vitesse.append([distance / duration.total_seconds(), i_temps])  ##Listes de Vitesse par groupe de 20
        # print("Duree : ", duration, "Distance : ", distance)
        distance = 0
    compteur = 0

    list_relvite = []
    cptt = 0
    # print("Liste des Vitesse ", list_vitesse)
    state = True
    ## Parcours de la liste de vitesse pour identifier les differences de vitesse 2 a 2
    for element in range(len(list_vitesse) - 1):
        compteur_date = 0
        ## Regle arbitraire + separer en 2 nouvelle trajectoire
        if (list_vitesse[element][0] > list_vitesse[element + 1][0] + 2) or (
                list_vitesse[element][0] < list_vitesse[element + 1][0] - 2):
            state = False
            K = list_vitesse[element][1]
            ## Calcul du temps
            Temps = 0
            date1 = dataframe.iloc[cptt]['Date'] + "/" + dataframe.iloc[cptt]['Horaire']

            ## Parcours du data frame separer par les temps
            ## boucle tant que cptt (notre depart) n'est pas arrivé a notre index de notre liste donc la derniere du groupe de 20
            ## Pour toutes les valeurs on applique le calcul de la distance et du temps et on le stocke dans le data frame
            coord_depart = (dataframe.iloc[cptt]['Latitude'], dataframe.iloc[cptt]['Longitude'])

            distance = 0
            while cptt < K - dataframe.index[0]:
                # print("cptt : ",cptt)
                coords_1 = (dataframe.iloc[cptt]['Latitude'], dataframe.iloc[cptt]['Longitude'])
                coords_2 = (dataframe.iloc[cptt + 1]['Latitude'], dataframe.iloc[cptt + 1]['Longitude'])
                distance += geopy.distance.geodesic(coords_1, coords_2).km
                cptt += 1

            date2 = dataframe.iloc[cptt]['Date'] + "/" + dataframe.iloc[cptt]['Horaire']
            time_1 = datetime.strptime(date1.strip(), "%Y-%m-%d/%H:%M:%S")
            time_2 = datetime.strptime(date2.strip(), "%Y-%m-%d/%H:%M:%S")
            duration = time_2 - time_1
            count_nbr_trajet += 1

            coords_arrive1 = (dataframe.iloc[cptt + 1]['Latitude'], dataframe.iloc[cptt + 1]['Longitude'])
            dist = float(distance)  # iterate the cursor
            # calcul vitesse en Km/h
            time = datetime.strptime(str(duration), "%H:%M:%S").time()
            time = timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
            speed = dist / (time.total_seconds() / 3600.0)
            data = {'USER_ID': user_id, "TRAJET_ID" : nbr_trajet, 'DATE': date1, 'DEPART': coord_depart,
                              'ARRIVE': coords_arrive1, 'DISTANCE': distance,
                              'TEMPS': str(duration), 'TYPE-TRANSPORT': infer_transport(speed)};
            if(distance != 0):
                list_df.append(data)

            cptt = list_vitesse[element][1] - dataframe.index[0]

    ## Cas du dernier trajet
    coord_depart = (dataframe.iloc[cptt]['Latitude'], dataframe.iloc[cptt]['Longitude'])
    date1 = dataframe.iloc[cptt]['Date'] + "/" + dataframe.iloc[cptt]['Horaire']
    distance = 0
    while cptt < len(dataframe.index) - 1:
        coords_1 = (dataframe.iloc[cptt]['Latitude'], dataframe.iloc[cptt]['Longitude'])
        coords_2 = (dataframe.iloc[cptt + 1]['Latitude'], dataframe.iloc[cptt + 1]['Longitude'])
        distance += geopy.distance.geodesic(coords_1, coords_2).km
        cptt += 1
    date2 = dataframe.iloc[cptt]['Date'] + "/" + dataframe.iloc[cptt]['Horaire']
    time_1 = datetime.strptime(date1.strip(), "%Y-%m-%d/%H:%M:%S")
    time_2 = datetime.strptime(date2.strip(), "%Y-%m-%d/%H:%M:%S")
    duration = time_2 - time_1
    count_nbr_trajet += 1

    coords_arrive2 = (dataframe.iloc[cptt - 1]['Latitude'], dataframe.iloc[cptt - 1]['Longitude'])
    dist = float(distance)  # iterate the cursor
    # calcul vitesse en Km/h
    time = datetime.strptime(str(duration), "%H:%M:%S").time()
    time = timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
    speed = dist / (time.total_seconds() / 3600.0)
    data = {'USER_ID': user_id,"TRAJET_ID" : nbr_trajet, 'DATE': date1, 'DEPART': coord_depart,
            'ARRIVE': coords_arrive2, 'DISTANCE': distance,
            'TEMPS': str(duration), 'TYPE-TRANSPORT': infer_transport(speed)};
    if (distance != 0):
        list_df.append(data)

    ## Si il n'y a pas de difference de vitesse
    coord_depart = (dataframe.iloc[0]['Latitude'], dataframe.iloc[0]['Longitude'])
    if state:
        distance = 0
        incre = 0
        for incre in range(len(dataframe.index) - 1):
            coords_1 = (dataframe.iloc[incre]['Latitude'], dataframe.iloc[incre]['Longitude'])
            coords_2 = (dataframe.iloc[incre + 1]['Latitude'], dataframe.iloc[incre + 1]['Longitude'])
            distance += geopy.distance.geodesic(coords_1, coords_2).km
        ## Calcul du temps
        Temps = 0
        date1 = dataframe.iloc[0]['Date'] + "/" + dataframe.iloc[0]['Horaire']
        date2 = dataframe.iloc[len(dataframe.index) - 1]['Date'] + "/" + \
                dataframe.iloc[len(dataframe.index) - 1]['Horaire']
        time_1 = datetime.strptime(date1.strip(), "%Y-%m-%d/%H:%M:%S")
        time_2 = datetime.strptime(date2.strip(), "%Y-%m-%d/%H:%M:%S")
        duration = time_2 - time_1
        count_nbr_trajet += 1
        coords_arrive3 = (dataframe.iloc[incre]['Latitude'], dataframe.iloc[incre]['Longitude'])
        dist = float(distance)  # iterate the cursor
        # calcul vitesse en Km/h
        time = datetime.strptime(str(duration), "%H:%M:%S").time()
        time = timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
        speed = dist / (time.total_seconds() / 3600.0)

        data = {'USER_ID': user_id, "TRAJET_ID" : nbr_trajet,'DATE': date1, 'DEPART': coord_depart,
                'ARRIVE': coords_arrive3, 'DISTANCE': distance,
                'TEMPS': str(duration), 'TYPE-TRANSPORT': infer_transport(speed)};
        if (distance != 0):
            #client["DonneeGPS"]["DATAGPS"].insert_one(data)
            list_df.append(data)
    list_vitesse.clear()

def main():
    # Select the CSV file to load
    st.write(
        "Nous avons fais le choix de pré-traiter nos données afin de les préparer a l'analyse finale. L'objectif ici est double, d'une part avoir les trajets de chaque utilisateurs pour pouvoir déterminer les trajets domicile travail et d'autre part d'avoir pour chaque trajet l'ensemble des sous trajets séparé par une différence de vitesse pour déterminer les type de transports utilisés.")
    st.header("Traitement des fichiers .plt sur la regle du temps ⏱")
    st.write("Pour chaque utilisateur (181), nous avons stocké tous ses relevés dans un data frame puis nous avons déterminé des trajets au sein de ses relevés. Nous avons tout d'abord appliqué une règle de séparation suivant le temps, **soit deux relevés consécutif ayant une différence de temps supérieur a 10 minutes alors chacun de ces deux relevés est un trajet diffèrent**.")
    st.header("Traitement des fichiers .plt sur la regle de vitesse 💨")
    st.write("Par la suite nous avons appliqué une règle de séparation par rapport a la vitesse sur nos relevés séparé par le temps, **soit deux groupes de 60 relevés consécutif ayant une différence de vitesse de +2,-2 mètre/seconde alors l'utilisateur a changé de moyen de transport et nous avons donc un nouveau sous trajet**.")
    st.write("Enfin, nous calculons pour chaque trajet la distance en km et le temps. Nous obtenons donc l'ensemble des trajets pour chaque utilisateurs séparé par le temps et un ensemble de sous trajet séparé par la vitesse. Chacun de ces ensembles sont stockés dans une collection MongoDB.")
    st.header("Determination du type de transport 🚅")
    st.write("Concercenant la determination du type de transport, nous avons appliqué des regles de determination de vitesse par exemple si la vitesse est comprise etre 0 et 10 KM/H alors le moyen de transport est la marche.")
    st.header("Demonstration, choissez un fichier .plt et voyez comment nous le transformons.")
    file = st.file_uploader("Choisir un fichier", type="plt")
    headers2 = ["USER_ID", "TRAJET_ID", "DATE", "DEPART", "ARRIVE", "DISTANCE", "TEMPS", "TYPE-TRANSPORT"]
    df_final = pd.DataFrame(columns=headers2)
    nbr_trajet = 0
    recup_id = 0
    if file is not None:
        df_test = ouverture_fichier(file)
        aled = regle_temps(df_test)
        for df in aled:
            regle_vitesse(df, recup_id, nbr_trajet)
            nbr_trajet += 1
        for elem in list_df:
            df_final = df_final.append(elem, ignore_index=True)
    st.dataframe(df_final,width=700)

if __name__ == "__main__":
    main()
