import functions as fun
import pandas as pd
import geopandas as gpd
from map import Map

path = 'venv/data/data_cities.csv'
tem_dataframe = pd.read_csv(path, sep=',')  # import the data
gpd_cities = gpd.GeoDataFrame(
    tem_dataframe, geometry=gpd.points_from_xy(tem_dataframe.Longitude, tem_dataframe.Latitude)
)
# # 'dt', 'AverageTemperature', 'City', 'Latitude', 'Longitude', 'geometry'
#
# #print(gpd_cities)
#
# # import a built-in dataset (deprecate from 2024)
gpd_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# # removing antarctica
gpd_world = gpd_world[gpd_world.continent != "Antarctica"]  # removing antartica
#
# fun.create_map(gpd_cities, gpd_world)
#
# fun.create_map_date(gpd_cities, gpd_world, '1990-01-01')
# # dates = gpd_cities['dt'].unique()
dates = ['2001-04-01', '2001-03-01']
fun.date_map_gif(gpd_cities, gpd_world, '2001-04-01', '2001-12-01')
# fun.create_map_gif(gpd_cities, gpd_world, dates)
# fun.create_map_range(gpd_cities, gpd_world, '1910-08-01', '2005-12-01')
#
# print(fun.best_route(gpd_cities, '2001-04-01', 'Peking', 'Los Angeles'))

#my_map = Map(gpd_cities, gpd_world)
# my_map.create_map()
#my_map.create_map_date('2001-04-01')
