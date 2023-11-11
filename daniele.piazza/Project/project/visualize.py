import pandas as pd
# install nbformat
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import plotly.graph_objects as go

class Visualize:
    def __init__(self, data):
        self.data = data
        self.data['dt'] = pd.to_datetime(self.data['dt'])
        self.data['Year'] = self.data['dt'].dt.year
        self.data.dropna(subset=['AverageTemperature'], inplace=True)
        self.data_year = self.data.groupby(['City_Country', 'Year', 'Latitude', 'Longitude']).agg(
            YearlyAverage=('AverageTemperature', 'mean'),
            AvailableMonths=('AverageTemperature', 'count'),
            MinTemp= ('AverageTemperature', 'min'),
            MaxTemp = ('AverageTemperature', 'max')).reset_index()
        self.data_year['YearlyAverage'] = self.data_year['YearlyAverage'].round(2)
        self.clean_data()
 
    def clean_data(self):
        self.data.sort_values(by='dt', inplace=True)
        complete_years = self.data_year[self.data_year['AvailableMonths'] == 12][['City_Country', 'Year']]
        self.data = pd.merge(self.data, complete_years, how='inner', on=['City_Country', 'Year'])
        self.data_year = self.data_year[self.data_year['AvailableMonths'] == 12]
        self.data_year.sort_values(by='Year', inplace=True)
        self.data_year.drop(columns=['AvailableMonths'], inplace=True)

    def fig_layout(self,fig):
        fig.update_layout(width=1200,height=600,margin={"r":0,"t":0,"l":0,"b":0})
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
        return self.fig_layout(fig,'General Map')
    
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
        return  self.fig_layout(fig)
    

    def heatmap(self):
        fig = px.density_mapbox(self.data_year, lat='Latitude', lon='Longitude', z='YearlyAverage', radius=5,
                                center=dict(lat=0, lon=0),range_color=[], zoom=0.4, animation_frame = 'Year',hover_name="City_Country",
                                mapbox_style="open-street-map", animation_group="City_Country",color_continuous_scale=px.colors.diverging.Portland,opacity=0.8,template='plotly_dark',
                                hover_data={
                                    "YearlyAverage": True,
                                    "City_Country": False,
                                    "Year": False,
                                    "Latitude": False,
                                    "Longitude": False,
                                })
        return self.fig_layout(fig)


    def line(self,city_country):
        city_data = self.data_year[(self.data_year['City_Country'] == city_country)]
        fig = px.line(city_data, x='Year', y='YearlyAverage', markers=True)
        return self.fig_layout(fig)

    def line_year(self,city_country,year):
        city_data = self.data[(self.data['City_Country'] == city_country) & (self.data['Year'] == year)]
        fig = px.line(city_data, x='dt', y='AverageTemperature', markers=True)
        return self.fig_layout(fig)
    
    def bubble_range(self):
        self.data_year["Range"] = self.data_year['MaxTemp'] - self.data_year['MinTemp']
        self.data_year["Size"] =  self.data_year['Range']/10
        min  = self.data_year['Range'].min()
        max = self.data_year['Range'].max()
        fig = px.scatter_mapbox(self.data_year, lat='Latitude', lon='Longitude', color="Range", size="Size",
                                color_continuous_scale=px.colors.diverging.Portland, zoom=1, animation_frame='Year',
                                hover_name="City_Country", mapbox_style="open-street-map", range_color=(min, max),template='plotly_dark',
                                hover_data={
                                    "Range": True,
                                    "City_Country": False,
                                    "Year": False,
                                    "Latitude": False,
                                    "Longitude": False,
                                    "YearlyAverage": False,
                                    "Size": False
                                })
        self.data_year.drop(columns=['Range', 'Size'], inplace=True)
        return self.fig_layout(fig)
    
    def bubble(self,size):
        min = self.data_year['MinTemp'].min()
        max = self.data_year['MinTemp'].max()
        self.data_year['Size'] = [size]*len(self.data_year)
        fig = px.scatter_mapbox(self.data_year,
                                lat='Latitude',
                                lon='Longitude',
                                color="YearlyAverage",
                                hover_name="City_Country",
                                size="Size",
                                size_max=size,
                                zoom=1,
                                animation_frame="Year",
                                mapbox_style="open-street-map",
                                range_color=(min,max),
                                color_continuous_scale=px.colors.diverging.Portland,template='plotly_dark',
                                hover_data={
                                    "YearlyAverage": True,
                                    "City_Country": False,
                                    "Year": False,
                                    "Latitude": False,
                                    "Longitude": False,
                                    "Size":False
                                })
        self.data_year.drop(columns=['Size'], inplace=True)
        return self.fig_layout(fig)
    
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

        fig = px.scatter(x=years.flatten(), y=temperatures, color_discrete_sequence=['green'], labels={'x': 'Year', 'y': 'Temperature'})
        fig.add_scatter(x=years.flatten(), y=predicted_temperatures, mode='lines', line=dict(color='blue'), name='Polynomial Regression')
        fig.add_scatter(x=np.arange(2012, 2100), y=future_predicted_temperatures, mode='lines', line=dict(color='red'), name='Future Prediction')
        fig.update_layout(xaxis_title='Year', yaxis_title='Temperature')
        return self.fig_layout(fig)
    
    def additional_statistics(self):
        city_stats = self.data_year.groupby('City_Country')['YearlyAverage'].agg(['mean', 'median', 'std']).reset_index()
        city_stats.columns = ['City', 'AverageTemperatureMean', 'AverageTemperatureMedian', 'AverageTemperatureStd']
        return city_stats
    
    def boxplot(self,city_country):
        df = self.data[self.data['City_Country'] == city_country]
        df['Month'] = df['dt'].dt.month
        df['Year'] = df['dt'].dt.year  
        df['Month_Name'] = df['dt'].dt.strftime('%B')  # Add a column for the month name
        colors = px.colors.qualitative.Dark24
        month_labels = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        fig = go.Figure()
        for month in range(1, 13):
            month_data = df[df['Month'] == month]
            month_temperatures = month_data['AverageTemperature']
            jittered_values = np.random.normal(month, 0.1, len(month_temperatures)) 
            fig.add_box(x=month_data['Month'], y=month_temperatures, name=month_labels[month], marker_color=colors[month-1], 
                        hovertemplate='Temperature: %{y}<br>Year: %{text}', text=month_data['Year'])
            fig.add_scatter(x=jittered_values, y=month_temperatures, mode='markers', name=month_labels[month], 
                            marker=dict(color=colors[month-1], size=5, opacity=0.1), showlegend=False,
                            hovertemplate='Temperature: %{y}<br>Year: %{text}', 
                            text=month_data['Year'])  
        fig.update_layout(xaxis={'tickmode': 'array', 'tickvals': list(month_labels.keys()), 'ticktext': list(month_labels.values())})
        fig.update_traces(line=dict(width=2))
        return self.fig_layout(fig)
    