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


st.set_page_config(
    page_title="Analyse des déplacements",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Main objective page
load_assets()
load_sidebar_footer("Analyse des déplacements", "storage")
st.markdown("""<h2 class="text-center" style="background-color:#cad2e0">Analyse des déplacements</h2>""", unsafe_allow_html=True)

# MongoDB
uri = 'mongodb+srv://admin:uvsqawsgroupe17@cluster0.nkdni.mongodb.net/?retryWrites=true&w=majority'
myclient = pymongo.MongoClient(uri)
mydb = myclient["DonneeGPS"]
mycol = mydb["DATAGPS"]


# ---------------------------#
# PARTIE STATS GENERALES #
# ---------------------------#
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
    fig = px.pie(df_plot, values='DISTANCE', names='MONTH', title='REPARTITION DISTANCE PARCOURUS PAR MOIS USER '+id_user)
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
    fig = px.bar(buff, x="DISTANCE", color="DISTANCE", title='DISTANCE TOTAL PAR MOIS USER '+id_user)
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


def chart_transport(id_user, label):
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

    # LABEL = TRAJET
    if label == "trajet":
        # Pie Chart Plot
        fig = px.pie(df_transport, values='count', names='TYPE-TRANSPORT', color="TYPE-TRANSPORT",
                     title='REPARTITION NB TRAJET PAR TYPE-TRANSPORT')
        st.plotly_chart(fig, theme=None, use_container_width=True)

    # LABEL = DISTANCE
    else:
        # Pie Chart Plot
        fig = px.pie(df_transport, values='DISTANCE', names='TYPE-TRANSPORT', color="TYPE-TRANSPORT",
                     title='REPARTITION DISTANCE PARCOURUS PAR TYPE-TRANSPORT')
        st.plotly_chart(fig, theme=None, use_container_width=True)


def bar_transport(id_user, label):
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

    # LABEL = TRAJET
    if label == "trajet":
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

    else:
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


def bar_mois_transport(id_user):
    x = mycol.find({'USER_ID': id_user})
    df_plot = pd.DataFrame.from_dict(x)

    # Add column MONTH
    dates = df_plot.DATE.tolist()
    months = [date[:7] for date in dates]
    df_plot["MONTH"] = months

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

    # Add column TYPE_TRANSPORT_FINAL
    transport_final = []

    for i in range(len(df_plot.TRAJET_ID)):
        test = df_plot.TYPE_TRANSPORT_SS_TRAJET[i].split(',')
        if len(test) > 1 and test[0] != test[1]:
            first_combi = test[0] + "," + test[1]
            second_combi = test[1] + "," + test[0]
            if second_combi not in transport_final:
                transport_final.append(first_combi)
            else :
                transport_final.append(second_combi)
        else:
            transport_final.append(test[0])

    df_plot['TYPE_TRANSPORT_FINAL'] = transport_final

    # La fonction pour le plot par mois
    fig = px.bar(df_plot, x="MONTH", color='TYPE_TRANSPORT_FINAL', barmode='group', height=1000,
                 title='NB TRAJET EFFECTUE PAR MOIS')
    fig.update_traces(dict(marker_line_width=0))
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


def chart_nb_ecologie(id_user, label):
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

    # drop les lignes qui ont plus de 5km de distance
    df_plot_ecologie = df_plot.drop(df_plot[df_plot.DISTANCE > 5.0].index)

    # Fixe les Index drop grâce à un compteur
    num_index = []
    for i in range(len(df_plot_ecologie)):
        num_index.append(i)
    df_plot_ecologie["INDEX_NUMBER"] = num_index
    df_plot_ecologie = df_plot_ecologie.set_index('INDEX_NUMBER')

    # Génère les statistiques nécessaires
    user_ecologie = stats_transport(df_plot_ecologie)

    # Dataframe de statistique écologie par TYPE-TRANSPORT
    data_ecologie = {
        "count": user_ecologie[:3],
        "DISTANCE": user_ecologie[3:],
        "TYPE-TRANSPORT": ['velo', 'voiture/bus/taxi', 'marche']
    }

    # load data into a DataFrame object:
    df_transport_ecologie = pd.DataFrame(data_ecologie)

    # LABEL = TRAJET
    if label == "trajet":
        # Pie Chart Plot
        fig = px.pie(df_transport_ecologie, values='count', names='TYPE-TRANSPORT', color='TYPE-TRANSPORT',
                     title='REPARTITION NB TRAJET PARCOURUS PAR TYPE-TRANSPORT MODELE ECOLOGIE')
        st.plotly_chart(fig, theme=None, use_container_width=True)

    # LABEL = DISTANCE
    else:
        # Pie Chart Plot
        fig = px.pie(df_transport_ecologie, values='DISTANCE', names='TYPE-TRANSPORT', color='TYPE-TRANSPORT',
                     title='REPARTITION DISTANCE PARCOURUS PAR TYPE-TRANSPORT MODELE ECOLOGIE')
        st.plotly_chart(fig, theme=None, use_container_width=True)


def bar_ecologie(id_user, label):
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

    # drop les lignes qui ont plus de 5km de distance
    df_plot_ecologie = df_plot.drop(df_plot[df_plot.DISTANCE > 5.0].index)

    # Fixe les Index drop grâce à un compteur
    num_index = []
    for i in range(len(df_plot_ecologie)):
        num_index.append(i)
    df_plot_ecologie["INDEX_NUMBER"] = num_index
    df_plot_ecologie = df_plot_ecologie.set_index('INDEX_NUMBER')

    # Génère les statistiques nécessaires
    user_ecologie = stats_transport(df_plot_ecologie)

    # Dataframe de statistique écologie par TYPE-TRANSPORT
    data_ecologie = {
        "count": user_ecologie[:3],
        "DISTANCE": user_ecologie[3:],
        "TYPE-TRANSPORT": ['velo', 'voiture/bus/taxi', 'marche']
    }

    # load data into a DataFrame object:
    df_transport_ecologie = pd.DataFrame(data_ecologie)

    # LABEL = TRAJET
    if label == "trajet":
        list_count_ecologie = user_ecologie[:3]
        average_count_ecologie = Average(list_count_ecologie)

        # Bar Plot
        fig = px.bar(df_transport_ecologie, x="TYPE-TRANSPORT", y="count", color="TYPE-TRANSPORT",
                     title='NB TRAJET PAR TYPE-TRANSPORT MODELE ECOLOGIE')

        # add a horizontal "target" line
        fig.add_shape(
            type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
            x0=0, x1=1, xref="paper", y0=average_count_ecologie, y1=average_count_ecologie, yref="y")

        fig.add_annotation(  # add a text callout with arrow
            text="MOYENNE", x="voiture/bus/taxi", y=average_count_ecologie, arrowhead=5, showarrow=True)

        st.plotly_chart(fig, theme=None, use_container_width=True)

    # LABEL = DISTANCE
    else:
        list_distance_ecologie = user_ecologie[3:]
        average_distance_ecologie = Average(list_distance_ecologie)

        # Bar Plot
        fig = px.bar(df_transport_ecologie, x="TYPE-TRANSPORT", y="DISTANCE", color="TYPE-TRANSPORT",
                     title='DISTANCE TOTALE PARCOURUS PAR TYPE-TRANSPORT MODELE ECOLOGIE')

        # add a horizontal "target" line
        fig.add_shape(
            type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
            x0=0, x1=1, xref="paper", y0=average_distance_ecologie, y1=average_distance_ecologie, yref="y",
            name="moyenne")

        fig.add_annotation(  # add a text callout with arrow
            text="MOYENNE", x="voiture/bus/taxi", y=average_distance_ecologie, arrowhead=5, showarrow=True)

        st.plotly_chart(fig, theme=None, use_container_width=True)

def plot_rep_depart_arrive(id_user):

    W000 = myclient["DonneeGPS"]["DATAGPS"].find({'USER_ID': id_user})
    df_plot_000_time = pd.DataFrame.from_dict(W000)

    def get_max_occurrence(strings):
        # Create a dictionary to keep track of the number of occurrences of each string
        occurrences = {}

        # Loop through the strings and update the dictionary
        for string in strings:
            if string in occurrences:
                occurrences[string] += 1
            else:
                occurrences[string] = 1

        # Find the string with the most occurrences
        max_occurrence = 0
        max_string = None
        for string, count in occurrences.items():
            if count > max_occurrence:
                max_occurrence = count
                max_string = string

        # Return the string with the most occurrences
        return max_string

    def findkeys(node, kv):
        if isinstance(node, list):
            for i in node:
                for x in findkeys(i, kv):
                    yield x
        elif isinstance(node, dict):
            if kv in node:
                yield node[kv]
            for j in node.values():
                for x in findkeys(j, kv):
                    yield x

    list_ville_dep = []

    dictio = df_plot_000_time.to_dict('records')
    for elem in dictio:
        address = elem.get('DEPART')
        # traverse the data
        if 'village' in address:
            city_dep = address.get('village', '')
        elif 'town' in address:
            city_dep = address.get('town', '')
        else:
            city_dep = address.get('city', '')
        address = elem.get('ARRIVE')
        # traverse the data
        if 'village' in address:
            city_arriv = address.get('village', '')
        elif 'town' in address:
            city_arriv = address.get('town', '')
        else:
            city_arriv = address.get('city', '')
        trajet = city_dep + " - " + city_arriv
        Transport = list(findkeys(elem, "TYPE-TRANSPORT"))
        list_ville_dep.append([trajet, get_max_occurrence(Transport)])

    headers3 = ["Ville_depart-arrive", "Transport Moyen"]
    df_test001 = pd.DataFrame(list_ville_dep)
    df_test001.columns = headers3
    df2 = df_test001
    df2 = df_test001.groupby(['Ville_depart-arrive'])['Ville_depart-arrive'].count().reset_index(name='count', )
    # print(df2)
    fig = px.bar(df_test001, x="Ville_depart-arrive", title='TRAJET USER '+id_user, color='Transport Moyen')
    # fig.show()
    st.plotly_chart(fig, theme=None, use_container_width=True)

def main():
    users = myclient["DonneeGPS"]["DATAGPS"].distinct("USER_ID")
    trajet = "trajet"
    distance = "distance"

    st.markdown("""
    <div class="card border shadow">
        <div class="card-body text-dark">
        Cette section regroupe les différentes visualisations graphiques réalisé.
        <br/>
        Les schémas ont été effectué grâce à une analyse du Dataset présent dans notre base de données MongoDB.
        </div>
    </div>
    <br/>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card border shadow">
        <div class="card-body text-dark">
        Afin d'étendre l'analyse nous avons expérimenté plusieurs domaines d'études.
        <br/>
        <li>Les différentes parties sont :
            <ul>
              <li>Partie Statistique Générale</li>
              <li>Partie Statistique Type-Transport</li>
              <li>Partie Statistique Écologie</li>
            </ul>
        </li>
        </div>
    </div>
    <br/>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card border shadow">
        <div class="card-body text-dark">
        ⚠️ Veuillez sélectionner un utilisateur avant de choisir un modèle de statistique ⚠️
        </div>
    </div>
    <br/>
    <br/>
    """, unsafe_allow_html=True)

    attribute = st.selectbox("Choisir l'user", users)
    # Définir le nombre de colonnes
    col1, col2, col3 = st.columns(3)

    if col1.button('Statistique Générale'):
        st.markdown("""
        <div class="card border shadow style="text-align:center;">
            <div class="card-body text-dark">
                <center> #--------------------------- PARTIE STATS GENERALES ---------------------------# </center>
            </div>
        </div>
        <br/>
        """, unsafe_allow_html=True)

        chart_dist_mois(attribute)
        bar_dist_mois(attribute)
        plot_rep_depart_arrive(attribute)
        profil_user(attribute)

    if col2.button('Statistique Type-Transport'):
        st.markdown("""
        <div class="card border shadow style="text-align:center;">
            <div class="card-body text-dark">
                <center> #--------------------------- PARTIE TYPE-TRANSPORT ---------------------------# </center>
            </div>
        </div>
        <br/>
        """, unsafe_allow_html=True)

        col2_1, col2_2 = st.columns(2)
        with col2_1:
            chart_transport(attribute, trajet)
        with col2_2:
            chart_transport(attribute, distance)

        bar_transport(attribute, trajet)
        bar_transport(attribute, distance)
        bar_mois_transport(attribute)

    if col3.button('Statistique Écologie'):
        st.markdown("""
                <div class="card border shadow style="text-align:center;">
                    <div class="card-body text-dark">
                        <center> #--------------------------- PARTIE ÉCOLOGIE ---------------------------# </center>
                    </div>
                </div>
                <br/>
        """, unsafe_allow_html=True)

        col3_1, col3_2 = st.columns(2)
        with col3_1:
            chart_nb_ecologie(attribute, trajet)
        with col3_2:
            chart_nb_ecologie(attribute, distance)

        bar_ecologie(attribute, trajet)
        bar_ecologie(attribute, distance)

if __name__ == "__main__":
    main()
