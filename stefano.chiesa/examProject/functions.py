from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


def convert(db, column):
    if column == 'Latitude':
        for x in range(len(db[column].index)):
            if db.at[x, column][-1] == 'N':
                db.at[x, column] = '+' + db.at[x, column][0:len(db.at[x, column]) - 1]
            elif db.at[x, column][-1] == 'S':
                db.at[x, column] = '-' + db.at[x, column][0:len(db.at[x, column]) - 1]

    elif column == 'Longitude':
        for x in range(len(db[column].index)):
            if db.at[x, column][-1] == 'E':
                db.at[x, column] = '+' + db.at[x, column][0:len(db.at[x, column]) - 1]
            elif db.at[x, column][-1] == 'W':
                db.at[x, column] = '-' + db.at[x, column][0:len(db.at[x, column]) - 1]

    return db


def create_map(ds, dw):
    # create a world map
    axis = dw.plot(color='lightblue', edgecolor='black')
    ds.plot(column='AverageTemperature', ax=axis, markersize=80, legend=True, legend_kwds={'shrink': 0.3})
    plt.title('Average Temperatures in World Major Cities ', fontsize=15)
    fig = plt.gcf()
    fig.set_size_inches(20, 16)
    fig.savefig('matplotlib.png', dpi=500, bbox_inches='tight')
    return plt.show()


def create_map_date(ds, dw, date):
    filtered_ds = ds[ds['dt'] == date]
    if not filtered_ds.empty:
        create_map(filtered_ds, dw)
    else:
        print('Data not available for the given date.')


def create_map_gif(ds, dw, dates):
    fig, ax = plt.subplots(figsize=(20, 16))
    axis = dw.plot(ax=ax, color='lightblue', edgecolor='black')

    def update(frame):
        current_date = dates[frame]
        filtered_cities = ds[ds['dt'] == current_date]
        scatter = filtered_cities.plot(column='AverageTemperature', ax=axis, markersize=80, legend=True, legend_kwds={'shrink': 0.3})
        plt.title(f'Average Temperatures in World Major Cities ({current_date})', fontsize=15)
        return scatter

    animation = FuncAnimation(fig, update, frames=len(dates), interval=250)
    animation.save('temperature_animation.gif', fps=1)
