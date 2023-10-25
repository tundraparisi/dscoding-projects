import functions as fun
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

tem_dataframe = pd.read_csv('venv/data/data_cities.csv', sep=',')  # import the data
gpd_cities = gpd.GeoDataFrame(
    tem_dataframe, geometry=gpd.points_from_xy(tem_dataframe.Longitude, tem_dataframe.Latitude)
)
# 'dt', 'AverageTemperature', 'City', 'Latitude', 'Longitude', 'geometry'


# import a built-in dataset (deprecate from 2024)
gpd_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# removing antarctica
gpd_world = gpd_world[gpd_world.continent != "Antarctica"]  # removing antartica

fun.create_map_date(gpd_cities, gpd_world, '1990-01-01')

# dates = gpd_cities['dt'].unique()
dates = ['1990-01-01', '1990-06-01', '1910-01-01', '1998-04-01']
fun.create_map_gif(gpd_cities, gpd_world, dates)
