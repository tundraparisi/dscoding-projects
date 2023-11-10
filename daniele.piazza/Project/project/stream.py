import streamlit as st
from location import Location
from visualize import Visualize
import pandas as pd

api_key = pd.read_csv("/Users/dani/Desktop/api_key.txt",header=None)[0][0]
all_path = "Data/GlobalLandTemperaturesByCity.csv"
major_path = "Data/GlobalLandTemperaturesByMajorCity.csv"

st.set_page_config(layout="wide")

update = False # Set to True if you want to update the coordinates of the cities in the file
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

@st.cache_data()
def load_bubble(_vis, size:None):
    if size is None:
        return _vis.bubble_range()
    return _vis.bubble(size)

location_major = load_location(major_path, api_key)
location_all = load_location(all_path, api_key)
major_map = load_map_data(location_major.data)
all_map = load_map_data(location_all.data)
major_bubble = load_bubble(major_map, 10)
all_bubble = load_bubble(all_map, 4)
major_range = major_map.bubble_range()
all_range = all_map.bubble_range()

def main():
    page = st.selectbox("", ("General Data", "City Information"))
    st.title("Climate Data Analysis")
    dataset = st.selectbox("Select a dataset", ("Major", "All"))
    if dataset == "Major":
        location = location_major
        st.write("This dataset contains data about the major cities of the world")
        vis = major_map
        bubble = major_bubble
        range = major_range
    else:
        location = location_all
        st.write("This dataset contains data about all the cities of the world")
        vis = all_map
        bubble = all_bubble
        range = all_range
    if page == "General Data":
        st.header("General Data")
        st.header("Statistics about the dataset")
        city_stats = location.additional_statistics()
        st.write("", city_stats)
        #st.subheader("General Map")
        #st.plotly_chart(vis.show_locations())
        st.subheader("Heatmap")
        #st.plotly_chart(vis.heatmap())
        st.plotly_chart(bubble)
        st.subheader("Range Heatmap")
        st.plotly_chart(range)
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
        st.header(f"Data for city: {selected_city}")

        city_map = Visualize(location.data)
        st.plotly_chart(city_map.show_city(selected_city))

        fig_city = vis.line(selected_city)
        st.plotly_chart(fig_city)
        st.write("Predicted Temperatures for the next 100 years")
        predicted_temperatures = vis.predict_city_temperature(selected_city)
        st.plotly_chart(predicted_temperatures)
        selected_year = st.selectbox("Select a year", vis.data_year[vis.data_year['City_Country']==selected_city]['Year'].unique())
        st.header(f"Data for the city: {selected_city} and year: {selected_year}")
        fig_city_year = vis.line_year(selected_city,selected_year)
        st.plotly_chart(fig_city_year)

if __name__ == "__main__":
    main()
