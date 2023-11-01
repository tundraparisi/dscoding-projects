import pandas as pd
import numpy as np
import scipy.spatial
import haversine

def calculate_3_closest_cities(data):
    # Calculate the distance matrix
    mat = scipy.spatial.distance.cdist(data[['lat', 'lng']], data[['lat', 'lng']], metric='euclidean')
    new_df = pd.DataFrame(mat, index=data['id'], columns=data['id'])

    # Store the array values in a variable
    arr = new_df.values

    # We don't want to find the minimum to be the same point, so replace diagonal by nan
    arr[np.diag_indices_from(new_df)] = np.nan

    # Find the indices of the 3 minimum values in each row
    closest_indices = np.argsort(arr, axis=1)[:, :3]

    # Get the names of the 3 closest cities for each city
    closest_cities = np.array(data['id'].iloc[closest_indices])

    # Add the 'close' column to the DataFrame
    data['closest_cities'] = list(closest_cities)

    return data

def sort_row(row):
    return row.sort_values(ascending=True)


def find_nearest_cities(df, k=3):
    # Crea un albero k-d con le coordinate delle città per migliorare l'efficienza
    city_coords = df[['lat', 'lng']].to_numpy()
    city_tree = scipy.spatial.KDTree(city_coords)

    city_coords = (df['lat'], df['lng'])
    # Trova gli indici delle k città più vicine
    nearest_indices = city_tree.query(city_coords, k=k+1)[1][1:]

    # Estrai i nomi delle k città più vicine
    nearest_cities = df.loc[nearest_indices, 'city_ascii'].tolist()

    # Aggiungi NaN se ci sono meno di k città vicine
    nearest_cities += [np.nan] * (k - len(nearest_cities))

    # Applica la funzione alle righe del DataFrame
    df['nearest_cities'] = df.apply(nearest_cities, axis=1)

    # Espandi la colonna 'nearest_cities' in tre colonne separate
    df[['nearest_city_1', 'nearest_city_2', 'nearest_city_3']] = pd.DataFrame(df['nearest_cities'].tolist(), index=df.index)

    return df


import scipy
import numpy as np
import pandas as pd


def closest_cities(df):
    mat = scipy.spatial.distance.cdist(df[['lat', 'lng']],
                                       df[['lat', 'lng']], metric='euclidean')
    new_df = pd.DataFrame(mat, index=df['id'], columns=df['id'])

    # Store the array values in a variable
    arr = new_df.values
    # We dont want to find mimimum to be same point, so replace diagonal by nan
    arr[np.diag_indices_from(new_df)] = np.nan

    # Replace the non nan min with column name and otherwise with false
    new_close = np.where(arr == np.nanmin(arr, axis=1)[:, None], new_df.columns, False)

    # Get column names ignoring false.
    df['close'] = [i[i.astype(bool)].tolist() for i in new_close]

    # we want to eliminate the brackets from the column 'close'
    df['close'] = df['close'].str.get(0)

    return df

def process_world_cities_data(data):
    # Calculate the distance matrix
    mat = scipy.spatial.distance.cdist(data[['lat', 'lng']], data[['lat', 'lng']], metric='euclidean')
    new_df = pd.DataFrame(mat, index=data['id'], columns=data['id'])

    # Store the array values in a variable
    arr = new_df.values

    # We don't want to find the minimum to be the same point, so replace diagonal by nan
    arr[np.diag_indices_from(new_df)] = np.nan

    # Replace the non-nan min with column name and otherwise with False
    new_close = np.where(arr == np.nanmin(arr, axis=1)[:, None], new_df.columns, False)

    # Get column names ignoring False
    data['close'] = [i[i.astype(bool)].tolist() for i in new_close]

    # Eliminate the brackets from the 'close' column
    data['close'] = data['close'].str.get(0)

    return data

def calculate_closest_cities(data, num_closest=3):
    # Calculate the distance matrix
    mat = scipy.spatial.distance.cdist(data[['lat', 'lng']], data[['lat', 'lng']], metric='euclidean')
    new_df = pd.DataFrame(mat, index=data['id'], columns=data['id'])

    # Store the array values in a variable
    arr = new_df.values

    # We don't want to find the minimum to be the same point, so replace diagonal by nan
    arr[np.diag_indices_from(new_df)] = np.nan

    # Find the indices of the num_closest minimum values in each row
    closest_indices = np.argsort(arr, axis=1)[:, :num_closest]

    # Get the names of the closest cities for each city
    closest_cities = data['id'].iloc[closest_indices].apply(lambda x: x.tolist()).reset_index(drop=True)

    # Add the 'close' column to the DataFrame
    data['close'] = closest_cities

    return data

