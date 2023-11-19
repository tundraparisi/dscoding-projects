import numpy as np


class City:
    def __init__(self, name, latitude, longitude, country, population, city_id):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.country = country
        self.population = population
        self.id = city_id
        self.neighbors = []

    def add_neighbor(self, neighbor, distance):
        self.neighbors.append({'city': neighbor, 'distance': distance})

    def calculate_distance(self, destination_city):
        '''
        :param destination_city: City, destination point
        :return: Euclidian distance between two cities
        '''
        # TODO think about distance between [-150, 150] by longitude
        return np.sqrt((destination_city.latitude - self.latitude) ** 2 +
                       (destination_city.longitude - self.longitude) ** 2)
