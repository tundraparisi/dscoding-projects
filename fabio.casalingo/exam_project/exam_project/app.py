import pandas as pd
from geopy.distance import great_circle as gc
import folium
import streamlit as st
import self_made_functions as func

st.title('Progetto Python')


@st.cache_data  # Utilizza la cache di Streamlit per memorizzare il dataframe
def load_dataset():
    return pd.read_excel('C:/Uni/Coding/python/worldcities.xlsx')


# Carica il dataframe utilizzando la funzione cache
dataset = load_dataset()

city_name_to_id_iso3 = {f"{city} ({iso3})": id for id, city, iso3 in
                        zip(dataset['id'], dataset['city'], dataset['iso3'])}
action = st.sidebar.selectbox('Seleziona un azione',
                              ['Trova n città più vicine', 'Calcola distanza tra due città',
                               'Trova città più ad est', 'Esegui percorso tra due città'])

if action == 'Trova n città più vicine':
    selected_city_name_iso3 = st.selectbox('Città', list(city_name_to_id_iso3.keys()))
    input_city_id = city_name_to_id_iso3[selected_city_name_iso3]
    n = st.number_input('Inserisci il numero di città vicine che desivìderi', min_value=1, value=1)
    n += 1
    if st.button('Trova città più n vicine'):
        closest_cities = func.three_close_city(input_city_id, n)
        st.write('Le tre città più vicine sono:')
        st.write(closest_cities)

if action == 'Calcola distanza tra due città':
    #path_df = pd.DataFrame(columns=['lat', 'lon'])
    selected_city1_name_iso3 = st.selectbox('Città1', list(city_name_to_id_iso3.keys()))
    selected_city2_name_iso3 = st.selectbox('Città2', list(city_name_to_id_iso3.keys()))
    input_city1_id = city_name_to_id_iso3[selected_city1_name_iso3]
    input_city2_id = city_name_to_id_iso3[selected_city2_name_iso3]
    if st.button('Mosta il percorso per andare da una città ad un altra'):
        path = func.distance_between_two_cities(input_city1_id, input_city2_id)
        st.write('Ecco la visualizzazione del percorso')
        mappa = func.maps(path)
        st.components.v1.html(mappa._repr_html_(), width=800, height=600)

if action == 'Trova città più ad est':
    func.prova()
if action == 'Esegui percorso tra due città':
    func.distance_between_two_cities()
