import functions as fun
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt


tem_dataframe = pd.read_csv('venv/data/data_cities.csv', sep=',')  # import the data
gpd_cities = gpd.GeoDataFrame(
    tem_dataframe, geometry = gpd.points_from_xy(tem_dataframe.Longitude, tem_dataframe.Latitude)
)

# import a built-in dataset (deprecate from 2024)
gpd_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# removing antartica
gpd_world = gpd_world[gpd_world.name != "Antarctica"]

# create a world map
axis = gpd_world.plot(color = 'lightblue', edgecolor = 'black')
gpd_cities.plot(ax = axis, color = 'black', markersize = 5)
plt.title('World Major Cities', fontsize = 40)
fig = plt.gcf()
fig.set_size_inches(19.2,18.2)
fig.savefig('matplotlib.png', dpi = 500, bbox_inches='tight')
plt.show()












