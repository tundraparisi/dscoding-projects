import pandas as pd
from geopy.distance import great_circle as gc
import folium

dataset = pd.read_excel('C:/Uni/Coding/python/worldcities.xlsx')

def three_close_city(input_city_id):
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
    closest_cities = sorted_dataset.iloc[1:]  # Skip the first row (starting city)
    return closest_cities


def distance_between_two_cities():
        s = dataset[dataset['id'] == 1826645935]
        start_city = int(s['id'].iloc[0])
        e = dataset[dataset['id'] == 1392685764]
        end_city = int(e['id'].iloc[0])

        start_coords = dataset[(dataset['id'] == start_city)][['lat', 'lng']].values[0]
        end_coords = dataset[(dataset['id'] == end_city)][['lat', 'lng']].values[0]

        visited_cities = []
        city = start_city
        visited_cities.append(city)
        while city != end_city:
            i = 35
            #j = 0
            while city in visited_cities:
                un_city = three_close_city(city)[: i]
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
        print('Sei arrivato!!')
        return visited_cities

def maps(visit):
    zoom = dataset[(dataset['id'] == visit[0])][['lat', 'lng']].values[0] #errore
    mappa = folium.Map(location = zoom, zoom_start = 2)
    #mappa = folium.Map(location=[45.5236, -122.6750], zoom_start=0)
    for i in range(len(visit)):
        s = dataset[(dataset['id'] == visit[i])][['lat', 'lng']].values[0]
        #if i > 0 and i < (len (visit) - 1):
            #s2 = dataset[(dataset['id'] == visit[i + 1])][['lat', 'lng']].values[0]
        folium.Marker(s,popup = dataset[(dataset['id'] == visit[i])][['city']].values[0] ).add_to(mappa)
    locations = [(dataset.loc[dataset['id'] == visit[j], ['lat', 'lng']].values[0]) for j in range(len(visit))]
    line = folium.PolyLine(locations=locations,
                           color='green',  # Colore della linea
                           weight=5,  # Spessore della linea
                           opacity=0.7  # Opacità della linea
                           )
    line.add_to(mappa)
    mappa.save('mappa.html')


def east(input_city_id):
    visited_cities = [input_city_id]  # Initialize a list to track visited cities
    starting_city = input_city_id
    city_coords = (dataset.loc[dataset['id'] == input_city_id, 'lat'].values[0],
                   dataset.loc[dataset['id'] == input_city_id, 'lng'].values[0])
    next_city_id= 0
    while next_city_id != starting_city:
        # Calculate distances from the current city to all cities in the dataset
        dataset['Distance from start'] = dataset.apply(lambda row: gc(city_coords, (row['lat'], row['lng'])).kilometers,
                                                       axis=1)
        east_cities = dataset[(dataset['lng'] > city_coords[1]) & (dataset['id'] != input_city_id)]
        if east_cities.empty:
            # far partire una divesa logica
            westernmost_city = dataset[dataset['lng'] == dataset['lng'].min()]
            closest_city = westernmost_city.iloc[0]
        else:
            # Sort the east cities by distance
            east_cities = east_cities.sort_values(by='Distance from start')
            # Get the closest city to the east
            closest_city = east_cities.iloc[0]

        next_city_id = closest_city['id']

        print(next_city_id)
        print(closest_city['city'])
        visited_cities.append(next_city_id)
        city_coords = (closest_city['lat'], closest_city['lng'])

    return visited_cities

#funziona non cancellare
def prova(input_city_id):
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
        if city_coords[1] > 0:
            east_cities = dataset[(dataset['lng'] > city_coords[1])][:100] #20
            #east_cities = dataset.iloc[abs(dataset['lat'] - city_coords[0]).argsort()][:50]  #NEW
            east_cities =  east_cities.sort_values(by='Distance from start')[:20] #NEW
            if east_cities.empty:
                # far partire una divesa logica
                westernmost_city = dataset[dataset['lng'] == dataset['lng'].min()]
                closest_city = westernmost_city.iloc[0]
            else:
                # Sort the east cities by distance
                if (east_cities['lat'].iloc[0], east_cities['lng'].iloc[0]) != start_coords:
                    east_cities = east_cities.sort_values(by='Distance from prev')
                # Get the closest city to the east
                closest_city = east_cities.iloc[0]
        else:
            east_cities = dataset[(dataset['lng'] > city_coords[1]) & (dataset['lng'] < 0)][:100]
            #east_cities = dataset.iloc[abs(dataset['lat'] - city_coords[0]).argsort()][:50] #NEW
            east_cities = east_cities.sort_values(by='Distance from start')[:20] #NEW

            if east_cities.empty:
                east_cities = dataset[(dataset['lng'] > city_coords[1])][:100]  # 20
                east_cities = east_cities.sort_values(by='Distance from start')[:20]  # NEW
                # Sort the east cities by distance
            if(east_cities['lat'].iloc[0], east_cities['lng'].iloc[0]) != start_coords:
                east_cities = east_cities.sort_values(by='Distance from prev')
                # Get the closest city to the east
            closest_city = east_cities.iloc[0]


        next_city_id = closest_city['id']
        if(closest_city['city']=='Labasa'):
            x+=1
        if x == 2:
            break
        #print(closest_city['city'],closest_city['lng'])
        visited_cities.append(next_city_id)
        city_coords = (closest_city['lat'], closest_city['lng'])

    return visited_cities

#versione senza modifiche
'''def prova(input_city_id):
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
        if city_coords[1] > 0:
            east_cities = dataset[(dataset['lng'] > city_coords[1])][:100] #20
            #east_cities = dataset.iloc[abs(dataset['lat'] - city_coords[0]).argsort()][:50]  #NEW
            east_cities =  east_cities.sort_values(by='Distance from start')[:20] #NEW
            if east_cities.empty:
                # far partire una divesa logica
                westernmost_city = dataset[dataset['lng'] == dataset['lng'].min()]
                closest_city = westernmost_city.iloc[0]
            else:
                # Sort the east cities by distance
                east_cities = east_cities.sort_values(by='Distance from prev')
                # Get the closest city to the east
                closest_city = east_cities.iloc[0]
        else:
            east_cities = dataset[(dataset['lng'] > city_coords[1]) & (dataset['lng'] < 0)][:100]
            #east_cities = dataset.iloc[abs(dataset['lat'] - city_coords[0]).argsort()][:50] #NEW
            east_cities = east_cities.sort_values(by='Distance from start')[:20] #NEW

            if east_cities.empty:
                east_cities = dataset[(dataset['lng'] > city_coords[1])]
                # Sort the east cities by distance
            east_cities = east_cities.sort_values(by='Distance from prev')
                # Get the closest city to the east
            closest_city = east_cities.iloc[0]


        next_city_id = closest_city['id']
        if(closest_city['city']=='Labasa'):
            x+=1
        if x == 2:
            break
        #print(closest_city['city'],closest_city['lng'])
        visited_cities.append(next_city_id)
        city_coords = (closest_city['lat'], closest_city['lng'])

    return visited_cities'''
#test fallimentare ma forse ha potenzialità
'''def prova(input_city_id):
    visited_cities = [input_city_id]  # Initialize a list to track visited cities
    starting_city = input_city_id

    # Get coordinates of the starting city
    city_coords = (dataset.loc[dataset['id'] == input_city_id, 'lat'].values[0],
                   dataset.loc[dataset['id'] == input_city_id, 'lng'].values[0])
    start_coords = city_coords
    next_city_id = 0
    x = 0

    while next_city_id != starting_city:
        # Calculate distances from the current city to all cities in the dataset
        dataset['Distance from prev'] = dataset.apply(lambda row: gc(city_coords, (row['lat'], row['lng'])).kilometers,
                                                       axis=1)
        dataset['Distance from start'] = dataset.apply(lambda row: gc(start_coords, (row['lat'], row['lng'])).kilometers,
                                                      axis=1)

        if city_coords[0] > 0:
            # If latitude is positive, prioritize moving east
            east_cities = dataset[(dataset['lng'] > city_coords[1])][:200]
        else:
            east_cities = dataset[(dataset['lng'] > city_coords[1]) & (dataset['lng'] < 0)][:200]

        east_cities = east_cities.sort_values(by='Distance from start')

        if east_cities.empty:
            # Handle the case when there are no more cities to the east
            westernmost_city = dataset[dataset['lng'] == dataset['lng'].min()]
            closest_city = westernmost_city.iloc[0]
        else:
            # Sort the east cities by distance from the previous city
            east_cities = east_cities.sort_values(by='Distance from prev')

            # Choose the closest city with the latitude closest to the starting city
            closest_city = east_cities.iloc[0]

        next_city_id = closest_city['id']

        if closest_city['city'] == 'Labasa':
            x += 1

        if x == 2:
            break

        print(closest_city['city'], closest_city['lng'])
        visited_cities.append(next_city_id)
        city_coords = (closest_city['lat'], closest_city['lng'])

    return visited_cities
'''

