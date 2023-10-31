from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1 import make_axes_locatable


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

    animation = FuncAnimation(fig, update, frames=len(dates), interval=250, init_func= init)
    animation.save('temperature_animation.gif', fps=1)


def date_map_gif(ds, dw, min_date, max_date):
    fig, ax = plt.subplots(figsize=(20, 16))
    axis = dw.plot(ax=ax, color='lightblue', edgecolor='black')
    dates = ds[(ds['dt'] >= min_date) & (ds['dt'] <= max_date)]

    def update(frame):
        try:
            current_date = dates.iloc[frame]['dt']
            filtered_cities = ds[ds['dt'] == current_date]
            scatter = filtered_cities.plot(column='AverageTemperature', ax=axis, markersize=80)
            plt.title(f'Average Temperatures in World Major Cities ({current_date})', fontsize=25)
            return scatter

        except IndexError:
            print("Date format not correct or Date non in the dataset")
            return None  # Return None for frames that caused an index out of range error

    try:
        # Create frames using FuncAnimation
        animation = FuncAnimation(fig, update, frames=len(dates), interval=250)

        # Add frames to the frames list
        animation.save('temperature_animation.gif', fps=1)

    except Exception as e:
        print(f"An error occurred: {e}")
        # Handle other exceptions if needed
