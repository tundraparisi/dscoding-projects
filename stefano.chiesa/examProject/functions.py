from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import math
"""
-- Documentation --

"""


def create_map(ds, dw, legend = False):
    # create a world map
    axis = dw.plot(color='grey', edgecolor='black')
    ds.plot(column='AverageTemperature', ax=axis, markersize=80, legend=legend, legend_kwds={'shrink': 0.3})
    plt.title('Average Temperatures in World Major Cities ', fontsize=15)
    fig = plt.gcf()
    fig.set_size_inches(20, 16)
    fig.savefig('matplotlib.png', dpi=500, bbox_inches='tight')
    return plt.show()


def create_map_date(ds, dw, date):
    filtered_ds = ds[ds['dt'] == date]
    if not filtered_ds.empty:
        create_map(filtered_ds, dw, True)
    else:
        print('Data not available for the given date.')


def create_map_gif(ds, dw, dates):

    fig, ax = plt.subplots(figsize=(20, 16))
    axis = dw.plot(ax=ax, color='grey', edgecolor='black')

    def update(frame):
        current_date = dates[frame]
        filtered_cities = ds[ds['dt'] == current_date]
        scatter = filtered_cities.plot(column='AverageTemperature', ax=axis, markersize=80)
        plt.title(f'Average Temperatures in World Major Cities ({current_date})', fontsize=25)
        return scatter

    def init():
        # Create an empty colorbar with the appropriate colormap and normalization
        sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=-40, vmax=40))
        sm.set_array([])  # empty array for the data range
        # Add the colorbar to the figure
        cbar = plt.colorbar(sm, ax=ax, fraction=0.02, pad=0.04)
        cbar.ax.tick_params(labelsize=14)
        return cbar

    animation = FuncAnimation(fig, update, frames=len(dates), interval=250, init_func=init)
    animation.save('temperature_animation.gif', fps=1)


def date_map_gif(ds, dw, min_date, max_date):
    fig, ax = plt.subplots(figsize=(20, 16))
    axis = dw.plot(ax=ax, color='grey', edgecolor='black')
    panda_dates = ds[(ds['dt'] >= min_date) & (ds['dt'] <= max_date)]
    dates = panda_dates['dt'].tolist()

    def update(frame):
        current_date = dates[frame]
        filtered_cities = ds[ds['dt'] == current_date]
        scatter = filtered_cities.plot(column='AverageTemperature', ax=axis, markersize=80)
        plt.title(f'Average Temperatures in World Major Cities ({current_date})', fontsize=25)
        return scatter

    def init():
        # Create an empty colorbar with the appropriate colormap and normalization
        sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=-80, vmax=60))
        sm.set_array([])  # empty array for the data range
        # Add the colorbar to the figure
        cbar = plt.colorbar(sm, ax=ax, fraction=0.02, pad=0.04)
        cbar.ax.tick_params(labelsize=14)
        return cbar

    animation = FuncAnimation(fig, update, frames=len(dates), interval=250, init_func=init)
    animation.save('temperature_animation.gif', fps=1)


def create_map_range(ds, dw, start_date, end_date):
    # Filter data within the specified date range
    filtered_data = ds[(ds['dt'] >= start_date) & (ds['dt'] <= end_date)]

    # Calculate temperature range for each city within the specified date range
    city_temperature_ranges = filtered_data.groupby('City')['AverageTemperature'].agg(['min', 'max']).apply(
        lambda x: (x['min'], x['max']), axis=1)

    # Get top 5 cities with the highest temperature difference within the specified date range
    top_cities = city_temperature_ranges.apply(lambda x: x[1] - x[0]).nlargest(5).index

    # Filter data for top 5 cities within the specified date range
    top_cities_data = filtered_data[filtered_data['City'].isin(top_cities)]

    # Create a world map
    axis = dw.plot(color='grey', edgecolor='black')

    # Plot top 5 cities with the highest temperature range within the specified date range
    top_cities_data.plot(column='AverageTemperature', ax=axis, markersize=80)

    # Annotate the map with city names and temperature ranges
    i = -80
    for idx, (city, (min_temp, max_temp)) in enumerate(city_temperature_ranges[top_cities].items()):
        plt.text(0, i, f'{city}: {round(min_temp, 1)}°C to {round(max_temp, 1)}°C: {round(max_temp - min_temp, 1)}C°',
                 fontsize=24, horizontalalignment='center')
        i = i - 9
    plt.title('Top 5 Cities with Highest Temperature Range\n{} to {}'.format(start_date, end_date), fontsize=15)
    fig = plt.gcf()
    fig.set_size_inches(20, 16)
    fig.savefig('matplotlib.png', dpi=500, bbox_inches='tight')

    plt.show()


def calculate_distance(city1, city2, route):
    # calculate the distance between two cities using their latitude and longitude coordinates
    lat1, lon1 = city1['Latitude'], city1['Longitude']
    lat2, lon2 = city2['Latitude'], city2['Longitude']

    # Haversine formula to compute distances on the Earth's surface in kms
    radius = 6371  # earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c

    if distance == 0 or city1['City'] in route:   # I set the cities where we already have been and the current city out of the planet to avoid loops :)
        return 1000000000
    else:
        return distance



def warmest_closest_city(current_city, ds, route):
    cities = []
    for idx, city in ds.iterrows():
        distance = calculate_distance(city, current_city, route)
        cities.append((distance, city))

    top5 = sorted(cities, key=lambda x: x[0])[:5]    # one line function to take the top 5 cities by distance (closest)
    warmest = max(top5, key=lambda x: x[1]['AverageTemperature'])   # same but by AverageTemperature

    return warmest[1].loc['City']        # we return the name of the warmest city


def best_route(ds, date, start_city, target_city):
    ds = ds[ds['dt'] == date]
    route = [start_city]
    current_city = start_city  # initialize current_city with the start city name

    while current_city != target_city:
        # find the GeoDataFrame row for the current city
        current_city_row = ds[ds['City'] == current_city].iloc[0]
        warmest = warmest_closest_city(current_city_row, ds, route)
        # extract the city name from the GeoDataFrame row
        current_city = warmest
        route.append(current_city)
    return route










