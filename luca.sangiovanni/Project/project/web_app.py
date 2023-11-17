import streamlit as st
import pandas as pd
from project.visualization import CityCountry, BigCities, Temperatures

path = "C:\\Users\sangi\Desktop\Info progetto python\Datasets"
cities = pd.read_csv(path + "\cities.csv", index_col=0)

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_title="Weather data project", layout="wide", initial_sidebar_state="expanded",)
st.sidebar.title("Pages' list")


def main_page():
    st.title("Weather data project")
    st.divider()
    st.write("""This project aims to analyze the change of temperatures from various cities around the world. Select 
            the page you wish to see from the menu on the left.""")
    st.write("For more info, check the readme file on GitHub or contact me at luca.sangiovanni1@studenti.unimi.it.")
    st.write("Have fun!")


def cities_overview():
    st.header("Cities overview")
    st.divider()
    st.write("""In this page you will be able to see an overview of the cities in the dataset. First of all,
             just by loking at the dataset, we can see that there are some countries that are represented by a lot
             of cities; as one would expect, the most represented countries are the most populated ones.""")
    st.write("In particular, here's a list of the top 15 most represented countries in the dataset:\n")
    st.dataframe(CityCountry.byCountry_List(any))
    st.text(" ")
    st.pyplot(CityCountry.byCountry_Plot(any))
    st.write("""\nThe data shown above is referring to the bigger dataset, which contains thousands of cities. I also 
            used a smaller dataset, which contains only 100 cities. Let's take a look at these major cities:\n""")
    if st.button("Show map", help="Click here to show the map of major cities", type="primary"):
        BigCities.majorCitiesMap(any)


def country_info():
    st.header("Country info")
    st.divider()
    st.write("""In this page you can see some informations about the countries present in the dataset. In addition,
            you will be able to see the map of the country, with its cities.\n""")
    selected_country = st.selectbox("Which country do you want to know about?", sorted(list(cities["Country"].unique())),
                                    placeholder="Click here to select a country...")
    if st.button("Confirm", help=("Click here to show info about " + selected_country), type="primary"):
        Temperatures.countryStats(any, nation=str(selected_country))
    if st.button(("Show me the map of " + selected_country), help=("Click here to show the map of " + selected_country),
                 type="primary"):
        CityCountry.byCountry_Map(any, nation=str(selected_country))


options = st.sidebar.radio(" ", options = ["Main menu", "Cities overview", "Country info", "Temperatures map",
                                           "Temperatures shock"])
if options == "Main menu":
    main_page()
elif options == "Cities overview":
    cities_overview()
elif options == "Country info":
    country_info()
elif options == "Temperatures map":
    temp_map()
elif options == "Temperatures shock":
    temp_shock()
