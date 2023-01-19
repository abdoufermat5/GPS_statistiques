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

def main():
    users = myclient["DonneeGPS"]["DATAGPS"].distinct("USER_ID")

#    if st.checkbox("Choisisser votre user"):
    attribute = st.selectbox("Choisir l'user", users)


if __name__ == "__main__":
    main()
