import pandas as pd
from geopy.geocoders import Nominatim
import plotly.express as px

def coords(x):
    if(x[len(x)-1]=='N'|x[len(x)-1]=='E'):
        i = float(x[:len(x)-1])
    else:
        i = -float(x[:len(x)-1])
    return i

def coordinates(city):
    return [coords(city['Latitude']), coords(city['Longitude'])]


def update_file(path):
    geolocator = Nominatim(user_agent='danipiazza')
    cities = pd.read_csv(path)
    cities_coord = {}
    for i in range(len(cities)):
        try:
            if cities['City'][i] in cities_coord:
                continue
            info = geolocator.geocode(cities['City'][i] + " " + cities['Country'][i])
            cities_coord[cities['City'][i]] = [info.latitude, info.longitude] 
        except:
            pass
    for i in range(len(cities)):
        if not cities['City'][i] in cities_coord:
            cities_coord[cities['City'][i]] = coordinates(cities.iloc[i])
    del cities['Latitude']
    del cities['Longitude']
    cities['Latitude'] = cities['City'].apply(lambda x: cities_coord[x][0])
    cities['Longitude'] = cities['City'].apply(lambda x: cities_coord[x][1])
    cities.to_csv(path, index=False)
