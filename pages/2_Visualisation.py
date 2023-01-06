import pymongo
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from gps_uvsq_utils.st_helpers import load_sidebar_footer, load_assets


st.set_page_config(
    page_title="Visualisation des données",
    page_icon="🎡",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Main objective page
load_assets()
load_sidebar_footer("Visualisation", "query_stats")
st.title("Visualisation & Statistiques")
uri = 'mongodb+srv://admin:uvsqawsgroupe17@cluster0.nkdni.mongodb.net/?retryWrites=true&w=majority'
myclient = pymongo.MongoClient(uri)

mydb = myclient["DonneeGPS"]
mycol = mydb["DATAGPS"]
def creat_plot(id_user):

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
    fig = px.bar(df_test001, x="Ville_depart-arrive", title='Trajet user '+id_user, color='Transport Moyen')
    # fig.show()
    st.plotly_chart(fig, theme=None, use_container_width=True)

def main():
    users = myclient["DonneeGPS"]["DATAGPS"].distinct("USER_ID")

#    if st.checkbox("Choisisser votre user"):
    attribute = st.selectbox("Choisir l'user", users)
    creat_plot(attribute)

if __name__ == "__main__":
    main()
