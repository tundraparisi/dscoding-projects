import streamlit as st
from location import Location
from visualize import Visualize
import pandas as pd

update = False # Set to True if you want to update the coordinates of the cities in the file
html = False  # Set to True if you want to create the html files for the bubble and range heatmaps

api_key = pd.read_csv("/Users/dani/Desktop/api_key.txt",header=None)[0][0]
all_path = "Data/GlobalLandTemperaturesByCity.csv"
major_path = "Data/GlobalLandTemperaturesByMajorCity.csv"

st.set_page_config(layout="wide")


@st.cache_data
def load_location(path, api_key):
    location = Location(path, api_key)
    if update:
        location.update_file()
    return location

@st.cache_data
def load_map_data(location_data):
    vis = Visualize(location_data)
    return vis

def create_html(major,all):
    major.bubble(10).write_html("bubble_major.html")
    major.bubble_range().write_html("range_major.html")
    all.bubble(2).write_html("bubble_all.html")
    all.bubble_range().write_html("range_all.html")

location_major = load_location(major_path, api_key)
location_all = load_location(all_path, api_key)
major_map = load_map_data(location_major.data)
all_map = load_map_data(location_all.data)

if html:
    create_html(major_map,all_map)

def load_html(path):
    with open(path, 'r') as f:
        return f.read()


def main():
    page = st.selectbox("", ("General Data", "City Information"))
    st.title("Climate Data Analysis")
    dataset = st.selectbox("Select a dataset", ("Top cities", "All cities"))
    if dataset == "Top cities":
        location = location_major
        st.write("This dataset contains data about the major cities of the world")
        vis = major_map
        bubble = load_html("bubble_major.html")
        range = load_html("range_major.html")
    else:
        location = location_all
        st.write("This dataset contains data about all the cities of the world")
        vis = all_map
        bubble = load_html("bubble_all.html")
        range = load_html("range_all.html")
    if page == "General Data":
        st.header("General Data")
        st.header("Statistics about the dataset")
        city_stats = vis.additional_statistics()
        st.write("", city_stats)
        #st.subheader("General Map")
        #st.plotly_chart(vis.show_locations())
        st.subheader("Range Heatmap")
        st.text("The heatmap shows the range (max-min) of temperatures for each city in the dataset")
        st.components.v1.html(range, width=1400, height=800, scrolling=True)
        st.subheader("Heatmap")
        st.text("The heatmap shows the average temperature for each city in the dataset")
        st.components.v1.html(bubble, width=1400, height=800, scrolling=True)
    elif page == "City Information":
        country = location.data['Country'].unique()
        country.sort()
        selected_country = st.selectbox("Select a country", ("All", *country))
        if selected_country != "All":
            city_list = location.data[location.data['Country'] == selected_country]['City_Country'].unique()
        else:
            city_list = location.data['City_Country'].unique()
        st.header("City Information")
        city_list.sort()
        selected_city = st.selectbox("Select a City", city_list)
        st.subheader(f"Data for city: {selected_city}")
        st.plotly_chart(vis.show_city(selected_city))
        st.subheader("Boxplot of the temperatures for the city")
        st.text("The boxplot shows the distribution of the temperatures for the city")
        boxplot = vis.boxplot(selected_city)
        st.plotly_chart(boxplot)
        st.subheader("Line chart of the temperatures for the city")
        st.text("The line chart shows the temperatures for the city during the years")
        fig_city = vis.line(selected_city)
        st.plotly_chart(fig_city)
        st.subheader("Predicted Temperatures")
        st.text("The line chart shows the predicted temperatures for the next 100 years")
        predicted_temperatures = vis.predict_city_temperature(selected_city)
        st.plotly_chart(predicted_temperatures)
        selected_year = st.selectbox("Select a year", vis.data_year[vis.data_year['City_Country']==selected_city]['Year'].unique())
        st.subheader(f"Data for the city: {selected_city} and year: {selected_year}")
        st.text("The line chart shows the temperatures for the city during the months of the year")
        fig_city_year = vis.line_year(selected_city,selected_year)
        st.plotly_chart(fig_city_year)

if __name__ == "__main__":
    main()
