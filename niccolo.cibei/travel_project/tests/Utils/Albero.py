import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
from haversine import haversine

def find_nearest_cities(df):
    # Crea un albero k-d con le coordinate delle città per migliorare l'efficienza
    city_coords = df[['lat', 'lng']].to_numpy()
    city_tree = cKDTree(city_coords)

    # Definisci una funzione per trovare le 3 città più vicine per ogni città
    def nearest_cities(city, k=3):
        city_coords = (city['lat'], city['lng'])
        # Trova gli indici delle k città più vicine
        nearest_indices = city_tree.query(city_coords, k=k+1)[1][1:]

        # Estrai i nomi delle k città più vicine
        nearest_cities = df.loc[nearest_indices, 'id'].tolist()

        # Aggiungi NaN se ci sono meno di k città vicine
        nearest_cities += [np.nan] * (k - len(nearest_cities))

        return nearest_cities

    # Applica la funzione alle righe del DataFrame
    df['nearest_cities'] = df.apply(nearest_cities, axis=1)

    # Espandi la colonna 'nearest_cities' in tre colonne separate
    df[['nearest_city_1', 'nearest_city_2', 'nearest_city_3']] = pd.DataFrame(df['nearest_cities'].tolist(), index=df.index)

    return df


def find_nearest_cities_try(df):
    # Crea un albero k-d con le coordinate delle città per migliorare l'efficienza
    city_coords = df[['lat', 'lng']].to_numpy()
    city_tree = cKDTree(city_coords)
# Definisci una funzione per trovare le 3 città più vicine per ogni città
    def nearest_cities(city, k=3):

        city_coords = (city['lat'], city['lng'])
        other_cities = df[df['city_ascii'] != city['city_ascii']]

        # Calcola le distanze haversine e crea un DataFrame temporaneo con le distanze
        temp_df = other_cities.apply(lambda row: haversine(city_coords, (row['lat'], row['lng']), unit='km'), axis=1)
        temp_df = temp_df.rename('distance').reset_index()

        # Trova le k città più vicine
        nearest_cities = temp_df.nsmallest(k, 'distance')

        # Restituisci solo i nomi delle città più vicine
        return nearest_cities['city_ascii'].to_list()


    # Applica la funzione alle righe del DataFrame
    df['nearest_cities'] = df.apply(nearest_cities, axis=1)

    # Espandi la colonna 'nearest_cities' in tre colonne separate
    df[['nearest_city_1', 'nearest_city_2', 'nearest_city_3']] = pd.DataFrame(df['nearest_cities'].tolist(), index=df.index)

    return df

