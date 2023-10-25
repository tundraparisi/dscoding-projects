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
    ds = ds[ds['dt'] == date]
    # getting days
    days = ds['dt'].unique()
    if date in days:
        create_map(ds, dw)
    else:
        return print('Unavailable date')


def create_map_gif(ds, dw, dates):
        fig, ax = plt.subplots(figsize=(20, 16))

        def update(frame):
            ax.clear()  # Clear the previous plot
            if ax.legend_:
                ax.legend_.remove()  # Remove the legend from the previous frame

            current_date = dates[frame]
            axis = dw.plot(ax=ax, color='lightblue', edgecolor='black')
            filtered_cities = ds[ds['dt'] == current_date]
            scatter = filtered_cities.plot(column='AverageTemperature', ax=axis, markersize=80, legend=True,
                                           legend_kwds={'shrink': 0.3})
            plt.title(f'Average Temperatures in World Major Cities ({current_date})', fontsize=15)
            return scatter

        animation = FuncAnimation(fig, update, frames=len(dates), interval=250)

        # Save the animation as a GIF file
        animation.save('temperature_animation.gif', fps=1)  # 1 frame per second
