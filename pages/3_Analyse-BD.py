import streamlit as st
import streamlit.components.v1 as components
from gps_uvsq_utils.st_helpers import load_assets, load_sidebar_footer
import os
import pandas as pd
from datetime import datetime
import geopy.distance
import matplotlib.pyplot as plt
import pymongo
import plotly.express as px
import seaborn as sns

st.set_page_config(
    page_title="Analyse de la base de données MongoDB",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Main objective page
load_assets()
load_sidebar_footer("Analyse BD", "storage")
st.title("Analyse de la base de données MongoDB")

# MongoDB
uri = 'mongodb+srv://admin:uvsqawsgroupe17@cluster0.nkdni.mongodb.net/?retryWrites=true&w=majority'
myclient = pymongo.MongoClient(uri)
mydb = myclient["DonneeGPS"]
mycol = mydb["DATAGPS"]


def chart_dist_mois(id_user):
    x = mycol.find({'USER_ID': id_user})
    df_plot = pd.DataFrame.from_dict(x)

    # Add column MONTH
    dates = df_plot.DATE.tolist()
    months = [date[:7] for date in dates]

    tab_size = []
    tab_transport = []

    for i in range(len(df_plot.SOUS_TRAJET)):
        buff = ""
        buff2 = ""
        tab_size.append(len(df_plot.SOUS_TRAJET[i]))
        for j in range(len(df_plot.SOUS_TRAJET[i])):
            if len(df_plot.SOUS_TRAJET[i]) > 1:
                # Pour éviter d'avoir la virgule au début
                if j == 0:
                    buff2 = df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
                else:
                    buff2 = buff2 + ',' + df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
                    buff = buff2
            else:
                buff = df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
        tab_transport.append(buff)

    df_plot["MONTH"] = months

    # Pie Chart Plot
    fig = px.pie(df_plot, values='DISTANCE', names='MONTH', title='REPARTITION DISTANCE PARCOURUS PAR MOIS')
    st.plotly_chart(fig, theme=None, use_container_width=True)


def bar_dist_mois(id_user):
    x = mycol.find({'USER_ID': id_user})
    df_plot = pd.DataFrame.from_dict(x)

    # Add column MONTH
    dates = df_plot.DATE.tolist()
    months = [date[:7] for date in dates]

    tab_size = []
    tab_transport = []

    for i in range(len(df_plot.SOUS_TRAJET)):
        buff = ""
        buff2 = ""
        tab_size.append(len(df_plot.SOUS_TRAJET[i]))
        for j in range(len(df_plot.SOUS_TRAJET[i])):
            if len(df_plot.SOUS_TRAJET[i]) > 1:
                # Pour éviter d'avoir la virgule au début
                if j == 0:
                    buff2 = df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
                else:
                    buff2 = buff2 + ',' + df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
                    buff = buff2
            else:
                buff = df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
        tab_transport.append(buff)

    df_plot["MONTH"] = months

    # Pie Bar Plot
    buff = df_plot.groupby('MONTH').sum()['DISTANCE'].sort_values()
    fig = px.bar(buff, x="DISTANCE", color="DISTANCE", title='DISTANCE TOTAL PAR MOIS (USER 000)')
    st.plotly_chart(fig, theme=None, use_container_width=True)


# ---------------------------#
# PARTIE TYPE-TRANSPORT #
# ---------------------------#

# Python program to get average of a list
def Average(data_list):
    return sum(data_list) / len(data_list)


# Fonction pour calculer les stats sur type-transport
def stats_transport(dataframe):
    # Calcul du nombre de trajet effectué par TYPE-TRANSPORT
    result_velo = 0
    result_voiture = 0
    result_marche = 0

    # Calcul du nombre de km parcourus par TYPE-TRANSPORT
    distance_velo = 0.0
    distance_voiture = 0.0
    distance_marche = 0.0

    for i in range(len(dataframe.TYPE_TRANSPORT_SS_TRAJET)):
        buff_tab = []

        if dataframe.TYPE_TRANSPORT_SS_TRAJET[i] == 'velo':
            result_velo = result_velo + 1
            distance_velo = distance_velo + dataframe.SOUS_TRAJET[i][0].get("DISTANCE")

        elif dataframe.TYPE_TRANSPORT_SS_TRAJET[i] == 'voiture/bus/taxi':
            result_voiture = result_voiture + 1
            distance_voiture = distance_voiture + dataframe.SOUS_TRAJET[i][0].get("DISTANCE")

        elif dataframe.TYPE_TRANSPORT_SS_TRAJET[i] == 'marche':
            result_marche = result_marche + 1
            distance_marche = distance_marche + dataframe.SOUS_TRAJET[i][0].get("DISTANCE")

        elif "," in dataframe.TYPE_TRANSPORT_SS_TRAJET[i]:
            buff_tab = dataframe.TYPE_TRANSPORT_SS_TRAJET[i].split(",")
            for j in range(len(buff_tab)):
                if buff_tab[j] == 'velo':
                    result_velo = result_velo + 1
                    distance_velo = distance_velo + dataframe.SOUS_TRAJET[i][j].get("DISTANCE")

                elif buff_tab[j] == 'voiture/bus/taxi':
                    result_voiture = result_voiture + 1
                    distance_voiture = distance_voiture + dataframe.SOUS_TRAJET[i][j].get("DISTANCE")

                elif buff_tab[j] == 'marche':
                    result_marche = result_marche + 1
                    distance_marche = distance_marche + dataframe.SOUS_TRAJET[i][0].get("DISTANCE")

    # Tableau des statistiques
    tab_stats = [result_velo, result_voiture, result_marche, distance_velo, distance_voiture, distance_marche]
    return tab_stats


def chart_nb_transport(id_user):
    x = mycol.find({'USER_ID': id_user})
    df_plot = pd.DataFrame.from_dict(x)

    # Add column TYPE_TRANSPORT_SS_TRAJET
    tab_size = []
    tab_transport = []

    for i in range(len(df_plot.SOUS_TRAJET)):
        buff = ""
        buff2 = ""
        tab_size.append(len(df_plot.SOUS_TRAJET[i]))
        for j in range(len(df_plot.SOUS_TRAJET[i])):
            if len(df_plot.SOUS_TRAJET[i]) > 1:
                # Pour éviter d'avoir la virgule au début
                if j == 0:
                    buff2 = df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
                else:
                    buff2 = buff2 + ',' + df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
                    buff = buff2
            else:
                buff = df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
        tab_transport.append(buff)

    df_plot["TYPE_TRANSPORT_SS_TRAJET"] = tab_transport

    # Génère les statistiques nécessaires
    df_buffer = stats_transport(df_plot)

    # Dataframe de statistique par TYPE-TRANSPORT
    data = {
        "count": df_buffer[:3],
        "DISTANCE": df_buffer[3:],
        "TYPE-TRANSPORT": ['velo', 'voiture/bus/taxi', 'marche']
    }

    # load data into a DataFrame object:
    df_transport = pd.DataFrame(data)

    # Pie Chart Plot
    fig = px.pie(df_transport, values='count', names='TYPE-TRANSPORT', color="TYPE-TRANSPORT",
                 title='REPARTITION NB TRAJET PAR TYPE-TRANSPORT')
    st.plotly_chart(fig, theme=None, use_container_width=True)


def chart_dist_transport(id_user):
    x = mycol.find({'USER_ID': id_user})
    df_plot = pd.DataFrame.from_dict(x)

    # Add column TYPE_TRANSPORT_SS_TRAJET
    tab_size = []
    tab_transport = []

    for i in range(len(df_plot.SOUS_TRAJET)):
        buff = ""
        buff2 = ""
        tab_size.append(len(df_plot.SOUS_TRAJET[i]))
        for j in range(len(df_plot.SOUS_TRAJET[i])):
            if len(df_plot.SOUS_TRAJET[i]) > 1:
                # Pour éviter d'avoir la virgule au début
                if j == 0:
                    buff2 = df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
                else:
                    buff2 = buff2 + ',' + df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
                    buff = buff2
            else:
                buff = df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
        tab_transport.append(buff)

    df_plot["TYPE_TRANSPORT_SS_TRAJET"] = tab_transport

    # Génère les statistiques nécessaires
    df_buffer = stats_transport(df_plot)

    # Dataframe de statistique par TYPE-TRANSPORT
    data = {
        "count": df_buffer[:3],
        "DISTANCE": df_buffer[3:],
        "TYPE-TRANSPORT": ['velo', 'voiture/bus/taxi', 'marche']
    }

    # load data into a DataFrame object:
    df_transport = pd.DataFrame(data)

    # Pie Chart Plot
    fig = px.pie(df_transport, values='DISTANCE', names='TYPE-TRANSPORT', color="TYPE-TRANSPORT",
                 title='REPARTITION DISTANCE PARCOURUS PAR TYPE-TRANSPORT')
    st.plotly_chart(fig, theme=None, use_container_width=True)


def bar_nb_transport(id_user):
    x = mycol.find({'USER_ID': id_user})
    df_plot = pd.DataFrame.from_dict(x)

    # Add column TYPE_TRANSPORT_SS_TRAJET
    tab_size = []
    tab_transport = []

    for i in range(len(df_plot.SOUS_TRAJET)):
        buff = ""
        buff2 = ""
        tab_size.append(len(df_plot.SOUS_TRAJET[i]))
        for j in range(len(df_plot.SOUS_TRAJET[i])):
            if len(df_plot.SOUS_TRAJET[i]) > 1:
                # Pour éviter d'avoir la virgule au début
                if j == 0:
                    buff2 = df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
                else:
                    buff2 = buff2 + ',' + df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
                    buff = buff2
            else:
                buff = df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
        tab_transport.append(buff)

    df_plot["TYPE_TRANSPORT_SS_TRAJET"] = tab_transport

    # Génère les statistiques nécessaires
    df_buffer = stats_transport(df_plot)

    # Dataframe de statistique par TYPE-TRANSPORT
    data = {
        "count": df_buffer[:3],
        "DISTANCE": df_buffer[3:],
        "TYPE-TRANSPORT": ['velo', 'voiture/bus/taxi', 'marche']
    }

    # load data into a DataFrame object:
    df_transport = pd.DataFrame(data)

    # Moyenne pour plot NB TRAJET
    list_count_transport = df_transport["count"].to_list()
    avg_count_transport = Average(list_count_transport)

    # Bar Plot
    fig = px.bar(df_transport, x="TYPE-TRANSPORT", y="count", color="TYPE-TRANSPORT",
                 title='NB TRAJET PAR TYPE-TRANSPORT')
    fig.add_shape(  # add a horizontal "target" line
        type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
        x0=0, x1=1, xref="paper", y0=avg_count_transport, y1=avg_count_transport, yref="y", name="moyenne"
    )
    fig.add_annotation(  # add a text callout with arrow
        text="MOYENNE", x="voiture/bus/taxi", y=avg_count_transport, arrowhead=5, showarrow=True
    )
    st.plotly_chart(fig, theme=None, use_container_width=True)


def bar_dist_transport(id_user):
    x = mycol.find({'USER_ID': id_user})
    df_plot = pd.DataFrame.from_dict(x)

    # Add column TYPE_TRANSPORT_SS_TRAJET
    tab_size = []
    tab_transport = []

    for i in range(len(df_plot.SOUS_TRAJET)):
        buff = ""
        buff2 = ""
        tab_size.append(len(df_plot.SOUS_TRAJET[i]))
        for j in range(len(df_plot.SOUS_TRAJET[i])):
            if len(df_plot.SOUS_TRAJET[i]) > 1:
                # Pour éviter d'avoir la virgule au début
                if j == 0:
                    buff2 = df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
                else:
                    buff2 = buff2 + ',' + df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
                    buff = buff2
            else:
                buff = df_plot.SOUS_TRAJET[i][j].get("TYPE-TRANSPORT")
        tab_transport.append(buff)

    df_plot["TYPE_TRANSPORT_SS_TRAJET"] = tab_transport

    # Génère les statistiques nécessaires
    df_buffer = stats_transport(df_plot)

    # Dataframe de statistique par TYPE-TRANSPORT
    data = {
        "count": df_buffer[:3],
        "DISTANCE": df_buffer[3:],
        "TYPE-TRANSPORT": ['velo', 'voiture/bus/taxi', 'marche']
    }

    # load data into a DataFrame object:
    df_transport = pd.DataFrame(data)

    # Moyenne pour plot DISTANCE PARCOURUS
    list_distance_transport = df_transport["DISTANCE"].to_list()
    avg_distance_transport = Average(list_distance_transport)

    # Bar Plot
    fig = px.bar(df_transport, x="TYPE-TRANSPORT", y="DISTANCE", color="TYPE-TRANSPORT",
                 title='DISTANCE TOTALE PARCOURUS PAR TYPE-TRANSPORT (en km)')
    fig.add_shape(  # add a horizontal "target" line
        type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
        x0=0, x1=1, xref="paper", y0=avg_distance_transport, y1=avg_distance_transport, yref="y", name="moyenne"
    )
    fig.add_annotation(  # add a text callout with arrow
        text="MOYENNE", x="velo", y=avg_distance_transport, arrowhead=5, showarrow=True
    )
    st.plotly_chart(fig, theme=None, use_container_width=True)


# ---------------------------#
# PROFIL USER #
# ---------------------------#

def profil_user(id_user):
    x = mycol.find({'USER_ID': id_user})
    df_plot = pd.DataFrame.from_dict(x)

    # L'index devient la DATE du trajet afin de faire des stats dessus
    df_plot.DATE = pd.to_datetime(df_plot.DATE)
    df_plot.set_index('DATE', inplace=True)

    # Tableau qui contient TOUTES les statistiques regrouper par semaine
    df_plot.DISTANCE = df_plot.DISTANCE.astype(float)

    m = df_plot['DISTANCE'].resample('W').agg(['mean', 'min', 'max'])
    m = m.dropna(axis=0)

    # On va récupérer toutes les années:
    m["DATES"] = m.index
    years = []
    for i in range(len(m.DATES)):
        test = str(m.DATES[i])
        test = test.split('-')
        if test[0] in years:
            continue
        else:
            years.append(test[0])

    fig = plt.figure(figsize=(8, 5))
    for j in range(len(years)):
        m['mean'][years[j]].plot(label='moyenne en ' + years[j], lw=2, ls='--', alpha=0.8)

    plt.ylabel('DISTANCE(km)')

    # displaying the legend and the title
    plt.legend()
    plt.title("Distance moyenne parcouru au cours des années")
    st.pyplot(fig, clear_figure=False)


def main():
    users = myclient["DonneeGPS"]["DATAGPS"].distinct("USER_ID")

    attribute = st.selectbox("Choisir l'user", users)
    chart_dist_mois(attribute)
    bar_dist_mois(attribute)
    chart_nb_transport(attribute)
    chart_dist_transport(attribute)
    bar_nb_transport(attribute)
    bar_dist_transport(attribute)
    profil_user(attribute)

if __name__ == "__main__":
    main()
