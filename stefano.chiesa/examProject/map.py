from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import math


class Map:
    def __init__(self, ds, dw):
        self.ds = ds  # geopandas dataframe with city data
        self.dw = dw  # geopandas dataframe with world map data

    def create_map(self, legend=False, date =""):
        # create a world map
        axis = self.dw.plot(color='grey', edgecolor='black')
        self.ds.plot(column='AverageTemperature', ax=axis, markersize=80, legend=legend, legend_kwds={'shrink': 0.3})
        plt.title('Average Temperatures in World Major Cities C°', fontsize=15)
        fig = plt.gcf()
        fig.set_size_inches(20, 16)
        plt.show()

    def create_map_date(self, date):
        filtered_ds = self.ds[self.ds['dt'] == date]

        if not filtered_ds.empty:
            self.ds = filtered_ds
            self.create_map(True)
            print("Map of " + date)
        else:
            print('Data not available for the given date.')

    def create_map_gif(self, dates):
        fig, ax = plt.subplots(figsize=(20, 16))
        axis = self.dw.plot(ax=ax, color='grey', edgecolor='black')
        dates.sort()

        def update(frame):
            current_date = dates[frame]
            filtered_cities = self.ds[self.ds['dt'] == current_date]
            scatter = filtered_cities.plot(column='AverageTemperature', ax=axis, markersize=80)
            plt.title(f'Average Temperatures in World Major Cities C° ({current_date})', fontsize=25)
            return scatter

        def init():
            # create an empty colorbar with the appropriate colormap and normalization
            sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=-40, vmax=40))
            sm.set_array([])    # empty array for the data range
            # add the colorbar to the figure
            cbar = plt.colorbar(sm, ax=ax, fraction=0.02, pad=0.04)
            cbar.ax.tick_params(labelsize=14)
            return cbar

        animation = FuncAnimation(fig, update, frames=len(dates), interval=250, init_func=init)
        animation.save('temperature_animation_dates.gif', fps=1)

    def date_map_gif(self, min_date, max_date):
        panda_dates = self.ds[(self.ds['dt'] >= min_date) & (self.ds['dt'] <= max_date)]
        dates = panda_dates['dt'].unique().tolist()
        self.create_map_gif(dates)

    def create_map_range(self, start_date, end_date):
        filtered_data = self.ds[(self.ds['dt'] >= start_date) & (self.ds['dt'] <= end_date)]
        city_temperature_ranges = filtered_data.groupby('City')['AverageTemperature'].agg(['min', 'max']).apply(
            lambda x: (x['min'], x['max']), axis=1)
        top_cities = city_temperature_ranges.apply(lambda x: x[1] - x[0]).nlargest(5).index
        top_cities_data = filtered_data[filtered_data['City'].isin(top_cities)]

        axis = self.dw.plot(color='grey', edgecolor='black')
        top_cities_data.plot(column='AverageTemperature', ax=axis, markersize=80)

        i = -80
        for idx, (city, (min_temp, max_temp)) in enumerate(city_temperature_ranges[top_cities].items()):
            plt.text(0, i, f'{city}: {round(min_temp, 1)}°C to {round(max_temp, 1)}°C: {round(max_temp - min_temp, 1)}C°',
                     fontsize=24, horizontalalignment='center')
            i = i - 9
        plt.title('Top 5 Cities with Highest Temperature Range\n{} to {}'.format(start_date, end_date), fontsize=15)
        fig = plt.gcf()
        fig.set_size_inches(20, 16)
        plt.show()

    def calculate_distance(self, city1, city2, route):
        lat1, lon1 = city1['Latitude'], city1['Longitude']
        lat2, lon2 = city2['Latitude'], city2['Longitude']

        radius = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = radius * c

        if distance == 0 or city1['City'] in route:
            return 1000000000
        else:
            return distance

    def warmest_closest_city(self, current_city, route):
        cities = []
        for idx, city in self.ds.iterrows():
            distance = self.calculate_distance(city, current_city, route)
            cities.append((distance, city))

        top5 = sorted(cities, key=lambda x: x[0])[:5]
        warmest = max(top5, key=lambda x: x[1]['AverageTemperature'])

        return warmest[1].loc['City']

    def best_route(self, date, start_city, target_city):
        ds = self.ds[self.ds['dt'] == date]
        route = [start_city]
        current_city = start_city

        while current_city != target_city:
            current_city_row = ds[ds['City'] == current_city].iloc[0]
            warmest = self.warmest_closest_city(current_city_row, route)
            current_city = warmest
            route.append(current_city)
        return route