import pandas as pd
# install nbformat
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

class Visualize:
    def __init__(self, data):
        self.data = data
        self.data['dt'] = pd.to_datetime(self.data['dt'])
        self.data['Year'] = self.data['dt'].dt.year
        self.data_year = self.year_temp()
        self.min = self.data_year['MinTemp'].min()
        self.max = self.data_year['MinTemp'].max()

    def fig_layout(self,fig,title):
        fig.update_layout(width=1200,height=700,margin={"r":0,"t":0,"l":0,"b":0},title=title)
        return fig
    
    def show_locations(self):
        city = self.data.groupby("City").first().reset_index()
        fig = px.scatter_mapbox(city,
                    lat='Latitude',
                    lon='Longitude',
                    hover_name="City",mapbox_style="carto-positron",zoom=1)
        fig.update_geos(
            visible=True, resolution=50,
            showcountries=True, countrycolor="RebeccaPurple"
        )
        fig.update_layout(width=1200,height=700, margin={"r":0,"t":0,"l":0,"b":0})
        return fig
    
    def show_city(self, city_country):
        filtered_data = self.data[self.data['City_Country'] == city_country].groupby(['City', 'Country', 'Latitude', 'Longitude']).first().reset_index()
        fig = px.scatter_mapbox(filtered_data,
                                lat='Latitude',
                                lon='Longitude',
                                hover_name="City",
                                mapbox_style="carto-positron",
                                zoom=7,
                                center={"lat": filtered_data['Latitude'].iloc[0], "lon": filtered_data['Longitude'].iloc[0]},size=[10],size_max=10)
        fig.update_geos(
            visible=True,
            resolution=50,
            showcountries=True,
            countrycolor="RebeccaPurple"
        )
        fig.update_layout(width=1200,height=700,margin={"r":0,"t":0,"l":0,"b":0})

        return fig
    

    def heatmap(self):
        color = px.colors.cyclical.IceFire
        fig = px.density_mapbox(self.data_year, lat='Latitude', lon='Longitude', z='YearlyAverage', radius=5,
                                center=dict(lat=0, lon=0),range_color=[], zoom=0.4, animation_frame = 'Year',hover_name="City",
                                mapbox_style="open-street-map", animation_group="City_Country",color_continuous_scale=color,opacity=0.8,template='plotly_dark')
        fig.update_layout(width=1200,height=700,margin={"r":0,"t":0,"l":0,"b":0}, title='Heatmap')

        return fig

    def line(self,city_country):
        city_data = self.data_year[(self.data_year['City_Country'] == city_country)]
        fig = px.line(city_data, x='Year', y='YearlyAverage', title=f" {city_country}", markers=True,width=1200,height=700)
        return fig

    def line_year(self,city_country,year):
        city_data = self.data[(self.data['City_Country'] == city_country) & (self.data['Year'] == year)]
        fig = px.line(city_data, x='dt', y='AverageTemperature', title=f" {city_country} in {year}", markers=True,width=1200,height=700)
        return fig
    
    def bubble_range(self):
        range = self.data_year['MaxTemp'] - self.data_year['MinTemp']
        size =  range/10
        min  = range.min()
        max = range.max()
        fig = px.scatter_mapbox(self.data_year, lat='Latitude', lon='Longitude', color=range, size=size,
                                color_continuous_scale=px.colors.diverging.Portland, zoom=1, animation_frame='Year',
                                hover_name="City_Country", mapbox_style="open-street-map", range_color=(min, max),template='plotly_dark')

        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, title='Temperature Range Heatmap',
                          width=1300,height=700)
        return fig
    
    def bubble(self,size):
        x = [size]*len(self.data_year)
        fig = px.scatter_mapbox(self.data_year, lat='Latitude',lon='Longitude', color="YearlyAverage", hover_name="City_Country", size=x,size_max=size ,zoom=1 ,animation_frame="Year",
                                mapbox_style="open-street-map", title='Temperature Change',range_color=(self.min,self.max),color_continuous_scale=px.colors.diverging.Portland,template='plotly_dark')
        fig.update_layout(width=1300,height=700,margin={"r":0,"t":0,"l":0,"b":0}, title='Heatmap')
        return fig
    
    def year_temp(self):
        city_year = self.data.copy() 
        city_year.dropna(subset=['AverageTemperature'], inplace=True)
        city_year = city_year.groupby(['City_Country', 'Year', 'Latitude', 'Longitude']).agg(
        YearlyAverage=('AverageTemperature', 'mean'),
        AvailableMonths=('AverageTemperature', 'count'),
        MinTemp= ('AverageTemperature', 'min'),
        MaxTemp = ('AverageTemperature', 'max')).reset_index()
        city_year = city_year[city_year['AvailableMonths'] == 12]
        city_year.drop(columns=['AvailableMonths'], inplace=True)
        city_year.sort_values(by='Year', inplace=True)
        return city_year
    
    def predict_city_temperature(self,city_country):
        city_data = self.data_year[(self.data_year['City_Country'] == city_country)]
        years = city_data['Year'].values.reshape(-1, 1)
        temperatures = city_data['YearlyAverage'].values
        poly_reg = PolynomialFeatures(degree=4)
        years_poly = poly_reg.fit_transform(years)
        lin_reg_poly = LinearRegression()
        lin_reg_poly.fit(years_poly, temperatures)
        future_years = np.arange(2012, 2100).reshape(-1, 1)
        future_years_poly = poly_reg.transform(future_years)
        predicted_temperatures = lin_reg_poly.predict(poly_reg.transform(years))
        future_predicted_temperatures = lin_reg_poly.predict(future_years_poly)

        fig = px.scatter(x=years.flatten(), y=temperatures, color_discrete_sequence=['green'], labels={'x': 'Year', 'y': 'Temperature'}, title=f'Temperature Prediction for {city_country}',width=1200,height=700)
        fig.add_scatter(x=years.flatten(), y=predicted_temperatures, mode='lines', line=dict(color='blue'), name='Polynomial Regression')
        fig.add_scatter(x=np.arange(2012, 2100), y=future_predicted_temperatures, mode='lines', line=dict(color='red'), name='Future Prediction')
        fig.update_layout(xaxis_title='Year', yaxis_title='Temperature')
        return fig