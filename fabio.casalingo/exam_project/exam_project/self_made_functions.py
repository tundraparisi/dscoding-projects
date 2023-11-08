import pandas as pd
from geopy.distance import great_circle as gc
import folium
import plotly.graph_objects as go
dataset = pd.read_excel('C:/Uni/Coding/python/worldcities.xlsx')

def three_close_city(input_city_id,n):
    city = dataset[dataset['id'] == input_city_id]  # seleziono il record relativo ad input_city
    id_city = int(city['id'].iloc[0])  # prendo l'id
    #     dataset.loc[dataset['id'] == id_city, 'lat'].values[0] estraggo la latitudine
    #     dataset.loc[dataset['id'] == id_city, 'lng'].values[0] estraggo la longitudine
    city_coords = (dataset.loc[dataset['id'] == id_city, 'lat'].values[0], dataset.loc[dataset['id'] == id_city, 'lng'].values[0])

    # Calculate distances from input_city to all cities in the dataset
    dataset['Distance from start'] = dataset.apply(lambda row: gc(city_coords, (row['lat'], row['lng'])).kilometers, axis=1)

    # Sort the dataset by distance
    sorted_dataset = dataset.sort_values(by='Distance from start')

    # Get the three closest cities
    closest_cities = sorted_dataset.iloc[1:n]  # Skip the first row (starting city)
    return closest_cities


def distance_between_two_cities(start_city,end_city):
        '''st = dataset[dataset['id'] == s]
        start_city = int(s['id'].iloc[0])
        ed = dataset[dataset['id'] == e]
        end_city = int(e['id'].iloc[0])'''

        start_coords = dataset[(dataset['id'] == start_city)][['lat', 'lng']].values[0]
        end_coords = dataset[(dataset['id'] == end_city)][['lat', 'lng']].values[0]

        visited_cities = []
        city = start_city
        visited_cities.append(city)
        while city != end_city:
            i = 35
            #j = 0
            while city in visited_cities:
                un_city = three_close_city(city,i)
                un_city['Distance to destination'] = un_city.apply(
                    lambda row: gc((row['lat'], row['lng']), end_coords).kilometers, axis=1)
                #j = i
                for x in range(i):
                    closest_city = un_city.sort_values(by='Distance to destination').iloc[x]
                    # print("CLOSEST: ",closest_city['city'])
                    if closest_city['id'] not in visited_cities:
                        city = closest_city['id']
                        name = closest_city['city']
                        #j = 0
                        break
                i += 1
            #print(name)
            visited_cities.append(city)
        #print('Sei arrivato!!')
        return visited_cities

def maps(visit):
    zoom = dataset[(dataset['id'] == visit[0])][['lat', 'lng']].values[0] #errore
    mappa = folium.Map(location = zoom,zoom_start = 2)
    #mappa = folium.Map(location=[45.5236, -122.6750], zoom_start=0)
    folium.TileLayer('cartodbdark_matter').add_to(mappa)
    for i in range(len(visit)):
        s = dataset[(dataset['id'] == visit[i])][['lat', 'lng']].values[0]
        #if i > 0 and i < (len (visit) - 1):
            #s2 = dataset[(dataset['id'] == visit[i + 1])][['lat', 'lng']].values[0]
        folium.Marker(s,popup = dataset[(dataset['id'] == visit[i])][['city']].values[0]).add_to(mappa)
    locations = [(dataset.loc[dataset['id'] == visit[j], ['lat', 'lng']].values[0]) for j in range(len(visit))]
    line = folium.PolyLine(locations=locations,
                           color='yellow',  # Colore della linea
                           weight=2,  # Spessore della linea
                           opacity=0.3  # Opacità della linea
                           )
    line.add_to(mappa)
    mappa.save('mappa.html')
    return mappa

def map2(visited):
    # Creare una figura Plotly
    fig = go.Figure()
    row = {'lat': visited[0], 'lon': visited[1]}
    path_df = pd.DataFrame(columns=['lat', 'lon'])
    path_df = pd.concat([path_df, pd.DataFrame([row])], ignore_index=True)
    # Aggiungere i marker per le città nel percorso
    for i in range(len(path_df)):
        row = path_df.iloc[i]
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[row['lon']],
            lat=[row['lat']],
            mode='markers+text',
            text=[f'Città {i + 1}'],
            marker=dict(size=10)
        ))

    # Creare le linee tra i marker per rappresentare il percorso
    for i in range(len(path_df) - 1):
        start_coord = path_df.iloc[i]
        end_coord = path_df.iloc[i + 1]
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[start_coord['lon'], end_coord['lon']],
            lat=[start_coord['lat'], end_coord['lat']],
            mode='lines',
            line=dict(width=2, color='blue')
        ))

    # Personalizzare la figura
    fig.update_geos(projection_scale=10)
    fig.update_layout(title='Percorso tra le città')
    fig.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="lightgray")
    return fig


#funziona non cancellare
def east(input_city_id):
    visited_cities = [input_city_id]  # Initialize a list to track visited cities
    starting_city = input_city_id
    city_coords = (dataset.loc[dataset['id'] == input_city_id, 'lat'].values[0],
                   dataset.loc[dataset['id'] == input_city_id, 'lng'].values[0])
    start_coords = city_coords
    next_city_id= 0
    x = 0
    while next_city_id != starting_city:
        # Calculate distances from the current city to all cities in the dataset
        dataset['Distance from prev'] = dataset.apply(lambda row: gc(city_coords, (row['lat'], row['lng'])).kilometers,
                                                       axis=1)
        dataset['Distance from start'] = dataset.apply(lambda row: gc(start_coords, (row['lat'], row['lng'])).kilometers,
                                                     axis=1)
        dataset['Diff_lat'] = abs(dataset['lat'] - dataset.loc[dataset['id'] == input_city_id, 'lat'].values[0])

        if city_coords[1] > 0:
            if gc(city_coords, start_coords).kilometers < 150 and len(visited_cities) > 60 :
                visited_cities.append(starting_city)
                break
            east_cities = dataset[(dataset['lng'] > city_coords[1])]#[:2000] #20

            east_cities =  east_cities.sort_values(by='Distance from prev')[:5] #NEW
            if east_cities.empty:
                # far partire una divesa logica
                westernmost_city = dataset[dataset['lng'] == dataset['lng'].min()]
                closest_city = westernmost_city.iloc[0]
            else:
                # Sort the east cities by distance
                if (east_cities['lat'].iloc[0], east_cities['lng'].iloc[0]) != start_coords:
                    east_cities = east_cities.sort_values(by='Diff_lat')
                # Get the closest city to the east
                closest_city = east_cities.iloc[0]
        else:
            east_cities = dataset[(dataset['lng'] > city_coords[1]) & (dataset['lng'] < 0)]#[:2000]
            #east_cities = dataset.iloc[abs(dataset['lat'] - city_coords[0]).argsort()][:50] #NEW

            east_cities = east_cities.sort_values(by='Distance from prev')[:5] #NEW

            if east_cities.empty:
                east_cities = dataset[(dataset['lng'] > city_coords[1])]  # 20
                east_cities = east_cities.sort_values(by='Distance from prev')[:5]  # NEW
                # Sort the east cities by distance
            if(east_cities['lat'].iloc[0], east_cities['lng'].iloc[0]) != start_coords:
                east_cities = east_cities.sort_values(by='Distance from start')[:5]
                # Get the closest city to the east
            closest_city = east_cities.iloc[0]

        next_city_id = closest_city['id']
        print(closest_city['city'])
        '''if(closest_city['city']=='Labasa'):
            x+=1
        if x == 2:
            print('Male male')
            break'''
        visited_cities.append(next_city_id)
        if -17.4572 <= start_coords[1] <= 1.484 and start_coords[0] < 49.6504 and -60.4467 <= closest_city['lng'] <= -52.7333:
            city_coords = (dataset.loc[dataset['id'] == 1620177495, 'lat'].values[0],
                           dataset.loc[dataset['id'] == 1620177495, 'lng'].values[0])
        elif -9.6962 <= start_coords[1] <= -1.9025 and start_coords[0] > 49.6504 and -60.4467 <= closest_city['lng'] <= -52.7333:
            city_coords = (dataset.loc[dataset['id'] == 1372403494, 'lat'].values[0],
                           dataset.loc[dataset['id'] == 1372403494, 'lng'].values[0])
        elif 16.5033 <= start_coords[1] <= 49.18 and start_coords[0] < 12.0 and -60.4467 <= closest_city['lng'] <= -52.7333:
            visited_cities.append(1076697777)
            city_coords = (dataset.loc[dataset['id'] == 1024669127, 'lat'].values[0],
                           dataset.loc[dataset['id'] == 1024669127, 'lng'].values[0])
        elif 92.75 <= start_coords[1] <= 133.6667 and -12.6167 < start_coords[0] < 9.2833 and 79.826 <= closest_city['lng'] <= 81.7:
            city_coords = (dataset.loc[dataset['id'] == 1360353144, 'lat'].values[0],
                           dataset.loc[dataset['id'] == 1360353144, 'lng'].values[0])
        elif 92.75 <= start_coords[1] <= 133.6667 and start_coords[0] < -12.6167 and 79.826 <= closest_city['lng'] <= 81.7:
            city_coords = (dataset.loc[dataset['id'] == 1036561011, 'lat'].values[0],
                           dataset.loc[dataset['id'] == 1036561011, 'lng'].values[0])
        else:
            city_coords = (closest_city['lat'], closest_city['lng'])

    maps(visited_cities)
    return visited_cities
