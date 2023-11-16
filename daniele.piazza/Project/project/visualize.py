"""
This class is used to visualize the data. It contains methods to create the following visualizations:
- General Map (show_location): a map with all the cities in the dataset
- Specific City Information (show_city): a map with the city of choice
- Heatmap (heatmap): a heatmap with the average temperature of each city for each year
- Line Chart Year (line_year): a line chart with the average temperature of a selected city in each month
- Line Chart (line): a line chart with the average temperature of a selected city in each year
- Temperature Range Heatmap (bubble_range): a heatmap with the range of temperatures for each city
- Average Temperature Heatmap (bubble): a heatmap with the average temperature for each city
- Predicted Temperatures (predict_city_temperature): a line chart with the predicted temperatures for the next 50 years
- Additional Statistics (additional_statistics): a dataframe with additional statistics about the dataset
- Temperature Boxplot (boxplot): a boxplot and scatterplot with the distribution of temperatures for a selected city during each mont
"""
import pandas as pd
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
import toml 
import pycountry_convert as pc


class Visualize:
    """
    Initialize the class with the data and calculate the yearly average temperature for each city.

    Parameters
    ----------
    data : pandas.DataFrame
        The dataframe containing the climate data

    Attributes
    ----------
    data : pandas.DataFrame
        The original input data
    data_year : pandas.DataFrame
        Processed data with yearly averages and other statistics
    primaryColor : str
        Primary color for visualization theme
    backgroundColor : str
        Background color for visualization theme
    secondaryBackgroundColor : str
        Secondary background color for visualization theme
    textColor : str
        Text color for visualization theme
    """
    def __init__(self,label,group):
        self.label = label
        self.data.dropna(subset=[label], inplace=True)
        self.data.dropna(subset=['AverageTemperature'], inplace=True)
        self.data['Year'] = self.data['dt'].dt.year
        self.data = self.data.sort_values(by='dt')
        self.data_year = self.data.groupby(group).agg(
            YearlyAverage=('AverageTemperature', 'mean'),
            AvailableMonths=('AverageTemperature', 'count'),
            MinTemp=('AverageTemperature', 'min'),
            MaxTemp=('AverageTemperature', 'max'),
            Std=('AverageTemperature','std')).reset_index()
        self.data_year['YearlyAverage'] = self.data_year['YearlyAverage'].round(2)
        self.clean_data()
        self.calculate_annual_uncertainty()
        self.get_theme() 

    """
    Calculate the annual uncertainty for each city.
    """
    def calculate_annual_uncertainty(self):
        annual_uncertainty = self.data.groupby(['Year', self.label])['AverageTemperatureUncertainty'].apply(lambda x: (x ** 2).sum() ** 0.5)
        self.data_year = pd.merge(self.data_year, annual_uncertainty.reset_index(name='AverageTemperatureUncertainty'), on=['Year', self.label])

    """
    Clean the data by removing incomplete years.
    """
    def clean_data(self):
        self.data.sort_values(by='dt', inplace=True)
        complete_years = self.data_year[self.data_year['AvailableMonths'] == 12][[self.label, 'Year']]
        self.data = pd.merge(self.data, complete_years, how='inner', on=[self.label, 'Year'])
        self.data_year = self.data_year[self.data_year['AvailableMonths'] == 12]
        self.data_year.sort_values(by='Year', inplace=True)
        self.data_year.drop(columns=['AvailableMonths'], inplace=True)

    """
    Get the theme from the streamlit config file.
    """
    def get_theme(self):
        config = toml.load('.streamlit/config.toml')
        self.primaryColor = config['theme']['primaryColor']
        self.backgroundColor = config['theme']['backgroundColor']
        self.secondaryBackgroundColor = config['theme']['secondaryBackgroundColor']
        self.textColor = config['theme']['textColor']

    """
    Set the layout for the figure.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The figure to be updated

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The updated figure
    """
    def fig_layout(self,fig):
        fig.update_layout({'paper_bgcolor': self.backgroundColor},
                          width=1300,
                          height=700,
                          margin={'r':0,'t':0,'l':0,'b':0},
                          font=dict(color=self.primaryColor),
                          updatemenus=[dict(bgcolor=self.secondaryBackgroundColor)]
                          )
        fig.update_mapboxes(bounds_east=180, bounds_west=-180, bounds_north=90, bounds_south=-70)
        fig.update_geos(
            resolution=110,
            showcountries=True, countrycolor="Black",
            lataxis = dict(range = [-90, 90]),
            lonaxis = dict(range = [-180, 180]),
            showocean=True, oceancolor=self.backgroundColor,
            showframe=False,
            showcoastlines=False,
        )
        return fig
    

    """
    Show a line chart with the average temperature of a selected city in each month.

    Parameters
    ----------
    city_country : str
        The name of the city to be shown
    year : int
        The year to be shown

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the line chart
    """
    def line_year(self,selected,year):
        city_data = self.data[(self.data[self.label] == selected) & (self.data['Year'] == year)]
        month = city_data['dt'].dt.month
        fig = px.line(city_data, x=month, y='AverageTemperature', markers=True, color_discrete_sequence=[self.primaryColor])
        fig.update_xaxes(title_text='Month')
        fig.update_layout(xaxis={'tickmode': 'array',
                                 'tickvals':month.unique(),
                                 'ticktext': city_data['dt'].dt.strftime('%B').unique()})
        return self.fig_layout(fig)

    """
    Show a line chart with the average temperature of a selected city in each year and it's uncertainty.

    Parameters
    ----------
    city_country : str
        The name of the city to be shown

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the line chart
    """
    def line(self, selected):
        city_data = self.data_year[(self.data_year[self.label] == selected)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=city_data['Year'],
            y=city_data['YearlyAverage'] - city_data['AverageTemperatureUncertainty'],
            marker=dict(color=self.primaryColor),
            line=dict(width=0),
            mode='lines',
            showlegend=False,
            name='Lower bound'
        ))
        fig.add_trace(go.Scatter(
            x=city_data['Year'],
            y=city_data['YearlyAverage'] + city_data['AverageTemperatureUncertainty'],
            mode='lines',
            marker=dict(color=self.primaryColor),
            line=dict(width=0),
            fill='tonexty',
            fillcolor=self.secondaryBackgroundColor,
            showlegend=False,
            name='Upper bound'
        ))
        fig.add_trace(go.Scatter(
            x=city_data['Year'],
            y=city_data['YearlyAverage'],
            mode='lines',
            name='Average Temperature',
            line=dict(color=self.primaryColor)
        ))
        return self.fig_layout(fig)
        
    """
    Show a bubble map with the range of temperatures for each city for each year.

    Parameters
    ----------
    n : int
        The number of cities to be shown

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the bubble map
    """
    def range(self, n=None):
        df = self.data_year.copy()
        scaler = MinMaxScaler()
        df['Range'] = (df['MaxTemp'] - df['MinTemp']).round(2)
        df['Size'] =  scaler.fit_transform(df[['Range']])
        if n is not None:
            df = df.groupby('Year').apply(lambda x: x.nlargest(n, 'Range')).reset_index(drop=True)
        min = df['Range'].min()
        max = df['Range'].max()
        return self.range_figure(df,min,max)

    """
    Show a bubble map with the average temperature for each city for each year.

    Parameters
    ----------
    n : int
        The number of cities to be shown

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the bubble map
    """
    def temperature(self,n=None):
        df = self.data_year.copy()
        min = df['YearlyAverage'].min()
        max = df['YearlyAverage'].max()
        if n is not None:
            df = df.groupby('Year').apply(lambda x: x.nlargest(n, 'YearlyAverage')).reset_index(drop=True)
        bubble_counts = df['Year'].value_counts()
        df['Size'] = df['Year'].apply(lambda x: 1000 / np.log((bubble_counts[x]) + 1))
        return self.temperature_figure(df,min,max)


    """
    Predict the temperatures for the next 50 years using polynomial regression and show them in a line chart.

    Parameters
    ----------
    selected : str
        The name of the city/country to be shown

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the line chart
    """
    def predict_temperature(self,selected):
        city_data = self.data_year[(self.data_year[self.label] == selected)]
        years = city_data['Year'].values.reshape(-1, 1)
        temperatures = city_data['YearlyAverage'].values
        poly_reg = PolynomialFeatures(degree=4)
        years_poly = poly_reg.fit_transform(years)
        lin_reg_poly = LinearRegression()
        lin_reg_poly.fit(years_poly, temperatures)
        range = np.arange(years.max(), years.max()+50)
        future_years = range.reshape(-1, 1)
        future_years_poly = poly_reg.transform(future_years)
        predicted_temperatures = lin_reg_poly.predict(poly_reg.transform(years))
        future_predicted_temperatures = lin_reg_poly.predict(future_years_poly)
        fig = px.scatter(x=years.flatten(),
                         y=temperatures,
                         color_discrete_sequence=[self.secondaryBackgroundColor],
                         labels={'x': 'Year', 'y': 'Temperature'}
                         )
        fig.add_scatter(x=years.flatten(),
                        y=predicted_temperatures,
                        mode='lines',
                        line=dict(color=self.primaryColor),
                        name='Polynomial Regression'
                        )
        fig.add_scatter(x=range,
                        y=future_predicted_temperatures,
                        mode='lines', 
                        line=dict(color='red'),
                        name='Future Prediction'
                        )
        fig.update_layout(xaxis_title='Year', yaxis_title='Temperature')
        return self.fig_layout(fig)
    

    """
    Calculate additional statistics about the dataset: average, minimum, maximum and standard deviation of the temperatures for each city.

    Returns
    -------
    city_stats : pandas.DataFrame
        The dataframe with the statistics
    """
    def additional_statistics(self):
        city_stats = self.data.groupby(self.label).agg(
            AverageTemperature=('AverageTemperature', 'mean'),
            MinTemperature=('AverageTemperature', 'min'),
            MaxTemperature=('AverageTemperature', 'max'),
            Std=('AverageTemperature','std')).round(2)
        return city_stats
    
    """
    Show a boxplot and scatterplot with the distribution of temperatures for a selected city during each month.

    Parameters
    ----------
    city_country : str
        The name of the city to be shown

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the boxplot and scatterplot
    """
    def boxplot(self,selected):
        df = self.data[self.data[self.label] == selected].copy()
        df['Month'] = df['dt'].dt.month
        df['Year'] = df['dt'].dt.year  
        df['Month_Name'] = df['dt'].dt.strftime('%B')  
        colors = px.colors.qualitative.Dark24
        fig = go.Figure()
        df.sort_values(by='Month', inplace=True)
        for month in range(1, 13):
            month_data = df[df['Month'] == month]
            month_temperatures = month_data['AverageTemperature']
            position = np.random.normal(month, 0.1, len(month_temperatures)) 
            month_name = month_data['Month_Name'].iloc[0]
            fig.add_box(x=month_data['Month'], 
                        y=month_temperatures, 
                        name=month_name, 
                        marker_color=colors[month-1], 
                        hovertemplate='Temperature: %{y}<br>Year: %{text}', 
                        text=month_data['Year']
                        )
            fig.add_scatter(x=position, 
                            y=month_temperatures, 
                            mode='markers', 
                            name=month_name, 
                            marker=dict(color=colors[month-1], size=5, opacity=0.3),
                            showlegend=False,
                            hovertemplate='Temperature: %{y}<br>Year: %{text}', 
                            text=month_data['Year']
                            )  
        fig.update_layout(xaxis={'tickmode': 'array',
                                 'tickvals':df['Month'].unique(),
                                 'ticktext': df['Month_Name'].unique()})
        fig.update_traces(line=dict(width=2))
        return self.fig_layout(fig)



class City(Visualize):
    def __init__(self,data):
        self.data = data.copy()
        group = ["City_Country", 'Year', 'Latitude', 'Longitude']
        super().__init__('City_Country',group)

    def range_figure(self,df,min,max):
        fig = px.scatter_mapbox(df,
                                lat='Latitude',
                                lon='Longitude',
                                color='Range',
                                size='Size',
                                color_continuous_scale=px.colors.diverging.Portland,
                                zoom=1,
                                animation_frame='Year',
                                hover_name='City_Country',
                                mapbox_style='open-street-map', 
                                range_color=(min, max),
                                template='plotly_dark',
                                hover_data={
                                    'Range': True,
                                    'City_Country': False,
                                    'Year': False,
                                    'Latitude': False,
                                    'Longitude': False,
                                    'YearlyAverage': False,
                                    'Size': False
                                })
        return self.fig_layout(fig)
    
    
    def temperature_figure(self,df,min,max):
        fig = px.scatter_mapbox(df,
                        lat='Latitude',
                        lon='Longitude',
                        color='YearlyAverage',
                        hover_name='City_Country',
                        size='Size',
                        zoom=1,
                        animation_frame='Year',
                        mapbox_style='open-street-map',
                        template='plotly_dark',
                        range_color=(min,max),
                        color_continuous_scale=px.colors.diverging.Portland,
                        hover_data={
                            'YearlyAverage': True,
                            'City_Country': False,
                            'Year': False,
                            'Latitude': False,
                            'Longitude': False,
                            'Size':False
                        })
        return self.fig_layout(fig)
    
    """
    Show a heatmap with the average temperature of each city for each year.

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the heatmap
    """
    def heatmap(self):
        fig = px.density_mapbox(self.data_year,
                                lat='Latitude',
                                lon='Longitude',
                                z='YearlyAverage',
                                radius=15,
                                center=dict(lat=0, lon=0),
                                range_color=[],
                                zoom=0.4,
                                animation_frame = 'Year',
                                hover_name='City_Country',
                                mapbox_style='open-street-map', 
                                animation_group='City_Country',
                                color_continuous_scale=px.colors.diverging.Portland,opacity=0.8,template='plotly_dark',
                                hover_data={
                                    'YearlyAverage': True,
                                    'City_Country': False,
                                    'Year': False,
                                    'Latitude': False,
                                    'Longitude': False,
                                })
        return self.fig_layout(fig)
    """
    Show a map with all the cities in the dataset.

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the map
    """
    def show_locations(self):
        city = self.data.groupby('City').first().reset_index()
        fig = px.scatter_mapbox(city,
                    lat='Latitude',
                    lon='Longitude',
                    hover_name='City',mapbox_style='open-street-map',zoom=1)
        fig.update_geos(
            visible=True, resolution=50,
            showcountries=True, countrycolor='RebeccaPurple'
        )
        return self.fig_layout(fig)
    
    """
    Show a map with the city of choice.

    Parameters
    ----------
    city_country : str
        The name of the city to be shown

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the map
    """
    def show_city(self, city_country):
        filtered_data = self.data[self.data['City_Country'] == city_country].groupby(['City_Country', 'Latitude', 'Longitude']).first().reset_index()
        filtered_data['Size'] = [20]
        fig = px.scatter_mapbox(filtered_data,
                                lat='Latitude',
                                lon='Longitude',
                                hover_name='City_Country',
                                mapbox_style='open-street-map',
                                zoom=7,
                                center={'lat': filtered_data['Latitude'].iloc[0], 'lon': filtered_data['Longitude'].iloc[0]},
                                size='Size',
                                hover_data={
                                    'City_Country': False,
                                    'Latitude': False,
                                    'Longitude': False,
                                    'Size': False
                                })
        fig.update_geos(
            visible=True,
            resolution=50,
            showcountries=True,
            countrycolor='RebeccaPurple'
        )
        return  self.fig_layout(fig)
    


class Country(Visualize):
    def __init__(self,path):
        self.data = pd.read_csv(path,index_col=False)
        self.data.loc[:,'Continent'] = self.data['Country'].apply(self.country_to_continent)
        self.data.loc[(self.data['Country'] == 'Congo (Democratic Republic Of The)') | (self.data['Country'] == "Côte D'Ivoire"), 'Continent'] = 'Africa'
        self.data.loc[self.data['Country'] == 'Bosnia And Herzegovina', 'Continent'] = 'Europe'
        self.data.dropna(subset=['Continent'], inplace=True)
        self.data['dt'] = pd.to_datetime(self.data['dt'])
        self.data['Year'] = self.data['dt'].dt.year
        group = ['Country', 'Year', 'Continent']
        super().__init__('Country',group)

    def country_to_continent(self,country_name):
        try:
            country_alpha2 = pc.country_name_to_country_alpha2(country_name)
            country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
            country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
        except:
            country_continent_name = None
        return country_continent_name

    def temperature_figure(self,df,min,max):
        fig = px.choropleth(df,
                            locations="Country",
                            locationmode = "country names", 
                            color="YearlyAverage", 
                            hover_name="Country",
                            animation_frame="Year",
                            range_color=[min,max],
                            color_continuous_scale=px.colors.diverging.Portland,
                            hover_data={
                                'YearlyAverage': True,
                                'Country': False,
                                'Year': False
                                })
        fig.update_layout(dragmode=False)
        return self.fig_layout(fig)
    
    def range_figure(self,df,min,max):
        fig = px.choropleth(df,
                        locations='Country',
                        locationmode='country names',
                        color='Range',
                        color_continuous_scale=px.colors.diverging.Portland,
                        animation_frame='Year',
                        hover_name='Country',
                        range_color=(min, max),
                        hover_data={
                            'Country': False,
                            'Year': False,
                            'YearlyAverage': False
                        })
        fig.update_layout(dragmode=False)
        return self.fig_layout(fig)
    
