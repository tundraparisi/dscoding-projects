import functions as fun
import geopandas.io.file
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

tem_dataframe = pd.read_csv('venv/data/data_cities.csv', sep=',')  # import the data
print(tem_dataframe.head())

gtfp_dataframe = geopandas.GeoDataFrame(
    tem_dataframe, geometry=geopandas.points_from_xy(tem_dataframe.Longitude, tem_dataframe.Latitude)
)
print(gtfp_dataframe.head())
