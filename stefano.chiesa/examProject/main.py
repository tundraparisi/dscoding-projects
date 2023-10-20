import functions as fun
import geopandas.io.file
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

tem_dataframe = pd.read_csv('data/mc.csv', sep=',')  # import the data

# cleaning the data
tfp_dataframe = tem_dataframe.drop(['AverageTemperatureUncertainty', 'Country'], axis=1)

print(tfp_dataframe)
print(tfp_dataframe[['Latitude', 'Longitude']])

#   table columns: | dt | AverageTemperature | City | Latitude | Longitude |

#gtfp_dataframe = geopandas.GeoDataFrame(
 #   tem_dataframe, geometry=geopandas.points_from_xy(tem_dataframe.Longitude, tem_dataframe.Latitude)
#)
#print(gtfp_dataframe.head())

a = np.array([1, 2, 3, 4, 5, 6, 7, 8])
print(a.shape)
m = np.array([
[2, 3, 4],
[5, 6, 7]
])
print(m.shape)


