import pandas as pd
import numpy as np
import scipy
import json

#url = 'http://island.ricerca.di.unimi.it/~alfio/shared/worldcities.xlsx'
df= pd.read_excel(r"C:\Users\cibei\OneDrive\Desktop\Coding_for_data_science\Python\dscoding-projects\niccolo.cibei\project\dataset\worldcities.xlsx")


def closest_cities(df):
    dict = {}

    mat = scipy.spatial.distance.cdist(df[['lat', 'lng']],
                                       df[['lat', 'lng']], metric='euclidean')
    new_df = pd.DataFrame(mat, index=df['id'], columns=df['id'])

    for i in range(len(new_df)):
        dict[new_df.index[i]] = new_df[new_df.index[i]].sort_values()[1:4]
    return dict


dictionary = closest_cities(df)

def closest_cities_json(data = dictionary):
    with open('closest_cities.json', 'w') as fp:
        json.dump(data, fp)

closest_cities_json(dictionary)


