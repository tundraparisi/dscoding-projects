import numpy as np
import pandas as pd
from haversine import haversine
import networkx as nx

class TravelGraph:
    def __init__(self, df):
        self.df = df
        self.G = nx.Graph()

    def haversine_matrix(self):
        # Convert latitude and longitude from degrees to radians
        coordinates = self.df[['lat', 'lng']].to_numpy()

        # Calculate Haversine distances
        hav_distances = np.zeros((len(coordinates), len(coordinates)))
        for i in range(len(coordinates)):
            for j in range(len(coordinates)):
                if i != j:
                    coords1 = coordinates[i]
                    coords2 = coordinates[j]
                    hav_distance = haversine(coords1,
                                             coords2,
                                             normalize=False,
                                             check=False)  # we don't want to check the coords
                    hav_distances[i, j] = hav_distance

        hav_matrix = pd.DataFrame(hav_distances, index=self.df['id'], columns=self.df['id'])
        return hav_matrix

    def graph_creation(self, k=30):
        hav_matrix = self.haversine_matrix()
        for city_id in self.df['id']:
            self.G.add_node(city_id)

        for i in range(len(hav_matrix)):
            close_city = pd.DataFrame(hav_matrix.iloc[i].sort_values())
            for j in range(1, k):
                self.G.add_edge(self.df.iloc[i]['id'], close_city.index[j], weight=close_city.iloc[j].values[0])

    def shortest_path(self, source_city_name, target_city_name):

        # Find the corresponding IDs for the source and target cities
        source_id = self.df.loc[self.df['city_ascii'] == source_city_name, 'id'].values[0]
        target_id = self.df.loc[self.df['city_ascii'] == target_city_name, 'id'].values[0]

        # Find the shortest path between the source and target city IDs
        short_path = nx.shortest_path(self.G, source=source_id, target=target_id, weight='weight')

        return short_path

    def cycle_tour(self, start_city_name):

        tour_cities = []
        # Find the corresponding ID for the starting city
        start_id = self.df.loc[self.df['city_ascii'] == start_city_name, 'id'].values[0]

        # Utilizza l'algoritmo di Dijkstra per trovare il percorso più breve che forma un ciclo
        cycle_path = nx.approximation.traveling_salesman_problem(self.G, cycle=True)

        # Trova l'indice della città di partenza nel percorso
        start_index = cycle_path.index(start_id)

        # Ruota la lista del percorso in modo che inizi dalla città di partenza
        tour_path = cycle_path[start_index:] + cycle_path[:start_index]
        for i in tour_path:
            tour_cities.append(self.df.loc[self.df['id'] == i, 'city_ascii'].values[0])
        return tour_cities



