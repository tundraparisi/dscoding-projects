import streamlit as st
import pandas as pd
import numpy as np
from data import Hotelsdata
from methods import Strategy
import altair as alt

# Setting page configuration
st.set_page_config(layout='wide')

# General title
st.title('Allocation strategies of guests into hotels')

# 1st subheader: introduction of the project
st.subheader('_Introduction to the project_')
st.write('**Based on 3 datasets imported (guests, hotels and guests´ preferences), this program outputs 4 different allocation strategies:**')
st.caption(':small_blue_diamond: :blue[**Random strategy:**] guests are allocated randomly into hotels.')
st.caption(':small_blue_diamond: :blue[**Preference strategy:**] guests are allocated into hotels based on their list of preference and room availability.')
st.caption(':small_blue_diamond: :blue[**Price strategy:**] guests are allocated into hotels based on price (from cheapest to most expensive), guests´s preferences and room availiability.')
st.caption(':small_blue_diamond: :blue[**Rooms strategy:**] guests are allocated into hotels based on number of rooms per hotel (from most rommy to least roomy), guests´s preferences and room availiability.')
st.write('---')  

# Datasets:
path = 'Datasets'
data = Hotelsdata(path)
df_guests = data.guests
df_hotels = data.hotels
df_preference = data.preference

# Strategies
strategy = Strategy(df_guests, df_hotels, df_preference)
#preference = strategy.preference
#price = strategy.price
#rooms = strategy.rooms

# 2nd subheader: select strategy to see data visualization
st.subheader('_Strategy results_')

# Select box: for selecting a strategy from the list of strategies.
select_strategy = st.selectbox(
    label='_Select a strategy to see detailed results of the allocation:_',
    options=["Random strategy", "Preference strategy", "Price strategy", "Rooms strategy"], 
    index=None, 
    placeholder="Select strategy...")

if select_strategy == 'Random strategy':
    # Summary table
    random = strategy.random
    Results = pd.DataFrame(['Random'])
    Results.columns = ['Strategy'] + list(Results.columns[1:])
    Results['Guests allocated'] = [f"{(random['guest'].count()):,}"]
    Results['vs_total guests'] = [f"{round((random['guest'].count()/data.guests['guest'].count())*100,2)}%"]
    Results['Average satisfaction'] = [int(round((random['guest_satisfaction'].mean()),0))]
    Results['Hotels occupied'] = [random['hotel'].nunique()]
    Results['vs total hotels'] = [f"{round((random['hotel'].nunique()/data.hotels['hotel'].count())*100,2)}%"]
    Results['Average earnings per hotel'] = [f"€{round((random['net_earning'].sum())/random['hotel'].nunique(),2):,}"]
    Results['Strategy´s total earnings'] = [f"€{round(random['net_earning'].sum(),2):,}"]
    st.write('_Satisfaction is measured from 1 (completely satisfied) to 5 (very dissatisfied)_')
    st.table(Results.set_index('Strategy'))

    # Chart
    hotels_occupied = random['hotel'].nunique()
    total_hotels = data.hotels['hotel'].count()

    # Create Altair charts
    hotels = pd.DataFrame({'Metric': ['Hotels Occupied', 'Total Hotels'], 'Count': [hotels_occupied, total_hotels]})
    chart = alt.chart(hotels, title='Hotels occupied').mark_bar(opacity=1).encode(
        column=alt.Column('hotel:O', spacing=5, header=alt.Header(labelOrient="bottom")),
        x=alt.X('variable', sort=['Actual_FAO', 'Predicted', 'Simulated'], axis=None),
        y=alt.Y('value:Q'),
        color=alt.Color('variable:N')).configure_view(stroke='transparent')
    
    st.altair_chart(chart_hotels, use_container_width=True)

    # Chart
