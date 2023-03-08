import os

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from gps_uvsq_utils.st_helpers import load_assets, load_html, load_sidebar_footer

st.set_page_config(
    page_title="Accueil",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_assets()

# load html file
descriptions = load_html("html/descriptions.html")


def members():
    st.markdown("<br/>"*3, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br/>"*3, unsafe_allow_html=True)
    st.markdown("""
    <h1 class="text-center" style="background-color:#cad2e0">Membres de l'équipe</h1>
    """, unsafe_allow_html=True)
    st.markdown("<br/>"*3, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="col-11">
                <div class="card bg-transparent border-0" style="background-color:e5e5e5">
                    <img src="https://cdn-icons-png.flaticon.com/512/147/147144.png" alt="Avatar de A" class="card-img-top rounded-circle">
                    <div class="card-body">
                        <h3 class="card-title text-center">Johann Ramanandraitsiory</h3>
                    </div>
                    <div class="card-footer text-center">
                        <h5 class="card-text"><b>Data Analyst</b></h5>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="col-11">
                <div class="card bg-transparent border-0" style="background-color:e5e5e5">
                    <img src="https://cdn-icons-png.flaticon.com/512/147/147144.png" alt="Avatar de A" class="card-img-top rounded-circle">
                    <div class="card-body">
                        <h3 class="card-title text-center">Samuel<br/> Kalfon</h3>
                    </div>
                    <div class="card-footer text-center">
                        <h5 class="card-text"><b>Data Analyst</b></h5>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="col-11">
                <div class="card bg-transparent border-0" style="background-color:e5e5e5">
                    <img src="https://cdn-icons-png.flaticon.com/512/147/147144.png" alt="Avatar de A" class="card-img-top rounded-circle">
                    <div class="card-body">
                    <h3 class="card-title text-center">Abdou Yaya Sadiakhou</h3>
                    </div>
                    <div class="card-footer text-center">
                        <h5 class="card-text"><b>Data Engineer</b></h5>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="col-11">
                <div class="card bg-transparent border-0" style="background-color:e5e5e5">
                    <img src="https://cdn-icons-png.flaticon.com/512/147/147144.png" alt="Avatar de A" class="card-img-top rounded-circle">
                    <div class="card-body">
                        <h3 class="card-title text-center">Gwennael Cannenpasse</h3>
                    </div>
                    <div class="card-footer text-center">
                        <h5 class="card-text"><b>Data Engineer</b></h5>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)


# components.html(file, height=1000)
st.markdown("""
<header class="bg-dark text-center py-2">
    <h5 class="display-5 text-white font-weight-bold">Calculs statistiques
privacy-by-design pour le Cloud personnel</h5>
</header>
""", unsafe_allow_html=True)
st.markdown(descriptions, unsafe_allow_html=True)
members()
load_sidebar_footer("Page d'accueil", "home")
