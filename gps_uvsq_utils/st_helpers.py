import os

import pandas as pd
import streamlit as st
from PIL import Image
from streamlit.components.v1 import html


# load html file
def load_html(html_file):
    with open(html_file) as f:
        html = f.read()
    return html


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def load_js(file_name):
    with open(file_name) as f:
        html(f'<script>{f.read()}</script>')


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def remote_js(url):
    st.markdown(f'<script src="{url}"></script>', unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


def insert_icon(icon_name):
    return f'<i class="material-icons" style="font-size:30px; vertical-align: middle;">{icon_name}</i>'


def load_sidebar_footer(page_name, icon_name):
    st.sidebar.markdown(f"""
    <button id="whatever" class="btn btn-large btn-secondary w-100" name="{page_name}" disabled>
    {insert_icon(icon_name)}
    <span>{page_name}</span>
    </button>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("***")
    st.sidebar.markdown("<br/><br/>", unsafe_allow_html=True)
    st.sidebar.markdown("""<i>Université Paris-Saclay - Master 2 Data Scale</i>""", unsafe_allow_html=True)
    st.sidebar.markdown("""<b>Année scolaire :</b> 2022-2023""", unsafe_allow_html=True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    paris_saclay = Image.open(os.path.join(current_dir, "assets", "uvsq.png"))
    st.sidebar.markdown("<br/><br/><br/><br/>", unsafe_allow_html=True)
    st.sidebar.image(paris_saclay, use_column_width=True)


def load_assets():
    remote_css("https://fonts.googleapis.com/icon?family=Material+Icons")
    remote_css("https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap")
    remote_css("https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,"
               "100..700,0..1,-50..200")
    remote_css("https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0")
    # bootstrap 5
    remote_css("https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/css/bootstrap.min.css")
    # font awesome
    remote_css("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css")

    # remote javascript
    remote_js("https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js")
    remote_js("https://cdn.jsdelivr.net/npm/@popperjs/core@2.18.0/dist/umd/popper.min.js")
    remote_js("https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js")


# Load the CSV file and convert it to a DataFrame
@st.cache
def load_data(file):
    return pd.read_csv(file)


def display_info(df):
    st.header("Information sur le dataframe")
    st.write(df.info())
    st.markdown("---")
    # Create a table with the DataFrame info
    info = [
        ("Nombre d'éléments", df.shape[0]),
        ("Nombre de colonnes", df.shape[1]),
        ("Nombre de valeurs nulles", df.isnull().sum().sum()),
    ]
    st.table(info)


# Display the first k rows of the DataFrame
def display_k_rows(df, k):
    st.dataframe(df.head(k))


# Display a bar chart of the distribution of an attribute
def display_bar_chart(df, attribute):
    st.bar_chart(df[attribute].value_counts())
