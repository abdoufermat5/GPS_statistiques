from datetime import datetime
from io import StringIO

import geopy.distance
import pandas as pd
import streamlit as st


def get_date_depart(file):
    with open(file) as f:
        data = f.readlines()[6]
        buff_data = data.replace("\n", "").split(",")
        date = buff_data[5]
    return date


def get_datetime_depart(file):
    with open(file) as f:
        data = f.readlines()[6]
        buff_data = data.replace("\n", "").split(",")
    depart_horaire = buff_data[5] + "/" + buff_data[6]

    return depart_horaire


def get_date_arrivee(file):
    with open(file) as f:
        data = f.readlines()[-1]
        buff_data = data.replace("\n", "").split(",")
        date = buff_data[5]
    return date


def get_datetime_arrivee(file):
    with open(file) as f:
        data = f.readlines()[-1]
        buff_data = data.replace("\n", "").split(",")
    arrivee_horaire = buff_data[5] + "/" + buff_data[6]

    return arrivee_horaire


def get_coord_depart(file):
    with open(file) as f:
        data = f.readlines()[6]
        buff_data = data.replace("\n", "").split(",")
    depart_coord = [buff_data[0], buff_data[1]]

    return depart_coord


def get_coord_arrivee(file):
    with open(file) as f:
        data = f.readlines()[-1]
        buff_data = data.replace("\n", "").split(",")
    arrivee_coord = [buff_data[0], buff_data[1]]

    return arrivee_coord


def delta_temps(t1, t2):
    t1 = datetime.strptime(t1, "%Y-%m-%d/%H:%M:%S")
    t2 = datetime.strptime(t2, "%Y-%m-%d/%H:%M:%S")
    delta = t2 - t1
    return delta


def calcul_distance_2_points(point1, point2):
    distance = geopy.distance.geodesic(point1, point2).km
    return distance


def calcul_dist(df, m_df):
    lat2 = m_df["latitude"].shift(1)[df.name]
    lon2 = m_df["longitude"].shift(1)[df.name]
    lat1 = df["latitude"]
    lon1 = df["longitude"]
    try:
        return geopy.distance.geodesic((lat1, lon1), (lat2, lon2)).km
    except:
        return 0


def calc_distance_parcouru_entre_2_coordonnees(df, start_idx, end_idx):
    df = df.iloc[start_idx:end_idx + 1]  # Select the relevant rows
    df['distance'] = df.apply(calcul_dist, axis=1, args=(df,))  # Calculate the distance
    distance_traveled = df['distance'].cumsum().iloc[-1]  # Cumulative sum of distances
    return distance_traveled


def calcul_distance_trajet(file):
    with open(file) as f:
        data = f.readlines()
        distance = 0
        for i in range(6, len(data) - 2):
            buff_data = data[i].replace("\n", "").split(",")
            buff_data2 = data[i + 1].replace("\n", "").split(",")
            distance += calcul_distance_2_points((float(buff_data[0]), float(buff_data[1])),
                                                 (float(buff_data2[0]), float(buff_data2[1])))
    return distance


def calcul_temps_trajet(file):
    depart = get_datetime_depart(file)
    arrivee = get_datetime_arrivee(file)
    delta = delta_temps(depart, arrivee)
    return delta


def calcul_vitesse_moyenne(file, unit="km/h"):
    distance = calcul_distance_trajet(file)
    delta = calcul_temps_trajet(file)
    if unit == "km/h":
        vitesse = distance / delta.total_seconds() * 3600
    elif unit == "m/s":
        vitesse = distance / delta.total_seconds()
    else:
        raise ValueError("Unit must be km/h or m/s")

    return vitesse


@st.cache
def creation_dataframe_fichier(file):
    file = file.read()
    string = file.decode("utf-8")
    # remove last 4 characters of the string
    string = string[:-2]
    data = StringIO(string)
    df = pd.read_csv(data,
                     header=None,
                     sep=',',
                     skiprows=6,
                     usecols=[0, 1, 3, 5, 6],
                     names=["latitude", "longitude", "altitude", "date", "horaire"])
    return df
