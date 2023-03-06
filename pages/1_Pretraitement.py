import streamlit as st
from gps_uvsq_utils.gps_helpers import creation_dataframe_fichier, calc_distance_parcouru_entre_2_coordonnees
from gps_uvsq_utils.st_helpers import load_assets, load_sidebar_footer, display_info, display_k_rows, display_bar_chart

st.set_page_config(
    page_title="Prétraitement des données",
    page_icon="🚞",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Main objective page
load_assets()
load_sidebar_footer("Prétraitements", "settings")
st.title("Les différents prétraitement")


def main():
    # Select the CSV file to load
    file = st.file_uploader("Choisir un fichier", type="plt")
    if file is not None:
        df = creation_dataframe_fichier(file)

        # Display information about the DataFrame
        if st.button("Afficher les informations sur le fichier", key="info"):
            display_info(df)

        # Display the first k rows of the DataFrame
        if st.checkbox("Afficher les premières lignes du fichier"):
            k = st.number_input("Nombre de lignes à afficher", min_value=5, max_value=25)
            display_k_rows(df, k)

        st.markdown("---")
        st.markdown("## Calcul de distance")
        # Select the coordinates
        start_idx, end_idx = st.slider('Depart:', 0, len(df) - 1, (0, len(df) - 1))
        start_latitude = df.iloc[start_idx]['latitude']
        start_longitude = df.iloc[start_idx]['longitude']
        end_latitude = df.iloc[end_idx]['latitude']
        end_longitude = df.iloc[end_idx]['longitude']

        # display coordinates in a map
        st.map(df.iloc[start_idx:end_idx][['latitude', 'longitude']])

        # text centered and bold
        st.markdown(f""" <p style="text-align: center; font-weight: bold;">DISTANCE ENTRE LES POINTS 
        <span style="border: solid 2px green; border-radius:10px; padding:5px; background-color: grey">{(start_latitude, start_longitude)}</span> ET 
        <span style="border: solid 2px red; border-radius:10px; padding:5px; background-color: grey">{(end_latitude, end_longitude)}</span></p> """, unsafe_allow_html=True)
        distance = calc_distance_parcouru_entre_2_coordonnees(df, start_idx, end_idx)
        st.markdown(f"""<span class="display-6">Distance:</span> <span class="display-5" style="border: solid 2px red; border-radius:10px; padding:5px; background-color: grey">{distance:.2f} km</span>""", unsafe_allow_html=True)


        # Display a bar chart of the distribution of an attribute
        if st.checkbox("Afficher la distribution d'un attribut"):
            attribute = st.selectbox("Choisir l'attribut", df.columns)
            display_bar_chart(df, attribute)


if __name__ == "__main__":
    main()
