import streamlit as st
import pandas as pd
import numpy as np
from data import Hotelsdata
from methods import Strategy

# Setting page configuration
st.set_page_config(layout='wide')

# General title
st.title('Allocation strategies of guests into hotels')

# 1st subheader: introduction of the project
st.subheader('_Introduction to the project_')
st.caption('**Based on 3 datasets imported (guests, hotels and guests´ preferences), this program outputs 4 different allocation strategies:**')
st.caption(':small_blue_diamond: :blue[**Random strategy:**] guests are allocated randomly into hotels.')
st.caption(':small_blue_diamond: :blue[**Preference strategy:**] guests are allocated into hotels based on their list of preference and room availability.')
st.caption(':small_blue_diamond: :blue[**Price strategy:**] guests are allocated into hotels based on price (from cheapest to most expensive), guests´s preferences and room availiability.')
st.caption(':small_blue_diamond: :blue[**Rooms strategy:**] guests are allocated into hotels based on number of rooms per hotel (from most rommy to least roomy), guests´s preferences and room availiability.')
st.write('---')  


# 2nd subheader: summary of each strategy
st.subheader('_Strategies´ summary_')

# Datasets:
path = 'Datasets'
data = Hotelsdata(path)
df_guests = data.guests
df_hotels = data.hotels
df_preference = data.preference

# Strategies
strategy = Strategy(df_guests, df_hotels, df_preference)
random = strategy.random
preference = strategy.preference
price = strategy.price
rooms = strategy.rooms

# Summary DataFrame of each strategy
Results = pd.DataFrame(['Random', 'Preference', 'Price', 'Rooms'])
Results.columns = ['Strategy'] + list(Results.columns[1:])
Results['Guests allocated'] = [f"{(random['guest'].count()):,}", f"{(preference['guest'].count()):,}", f"{(price['guest'].count()):,}", f"{(rooms['guest'].count()):,}"]
Results['vs_total guests'] = [f"{round((random['guest'].count()/data.guests['guest'].count())*100,2)}%", f"{round((preference['guest'].count()/data.guests['guest'].count())*100,2)}%", f"{round((price['guest'].count()/data.guests['guest'].count())*100,2)}%", f"{round((rooms['guest'].count()/data.guests['guest'].count())*100,2)}%"]
Results['Average satisfaction'] = [random['guest_satisfaction'].mean(), round((preference['guest_satisfaction'].mean()),0), round((price['guest_satisfaction'].mean()),0), round((rooms['guest_satisfaction'].mean()),0)]
Results['Hotels occupied'] = [random['hotel'].nunique(), preference['hotel'].nunique(), price['hotel'].nunique(), rooms['hotel'].nunique()]
Results['vs total hotels'] = [f"{round((random['hotel'].nunique()/data.hotels['hotel'].count())*100,2)}%", f"{round((preference['hotel'].nunique()/data.hotels['hotel'].count())*100,2)}%", f"{round((price['hotel'].nunique()/data.hotels['hotel'].count())*100,2)}%", f"{round((rooms['hotel'].nunique()/data.hotels['hotel'].count())*100,2)}%"]

hotel_list = pd.Series(data.hotels.rooms.values, index=data.hotels.hotel)
random_remaining_rooms = hotel_list.subtract(random.groupby('hotel')['guest'].count())
priority_remaining_rooms = hotel_list.subtract(preference.groupby('hotel')['guest'].count())
price_remaining_rooms = hotel_list.subtract(price.groupby('hotel')['guest'].count())
room_remaining_rooms = hotel_list.subtract(rooms.groupby('hotel')['guest'].count())

Results['Hotels fully occupied'] = [len(random_remaining_rooms[random_remaining_rooms == 0]), len(priority_remaining_rooms[priority_remaining_rooms == 0]), len(price_remaining_rooms[price_remaining_rooms == 0]), len(room_remaining_rooms[room_remaining_rooms == 0])]
Results['vs hotels occupied'] = [f"{round((len(random_remaining_rooms[random_remaining_rooms == 0])/random['hotel'].nunique())*100,2)}%", f"{round((len(priority_remaining_rooms[priority_remaining_rooms == 0])/preference['hotel'].nunique())*100,2)}%", f"{round((len(price_remaining_rooms[price_remaining_rooms == 0])/price['hotel'].nunique())*100,2)}%", f"{round((len(room_remaining_rooms[room_remaining_rooms == 0])/rooms['hotel'].nunique())*100,2)}%"]
Results['Average earnings per hotel'] = [f"€{round((random['net_earning'].sum())/random['hotel'].nunique(),2):,}", f"€{round((preference['net_earning'].sum())/preference['hotel'].nunique(),2):,}", f"€{round((price['net_earning'].sum())/price['hotel'].nunique(),2):,}", f"€{round((rooms['net_earning'].sum())/rooms['hotel'].nunique(),2):,}"]
Results['Strategy´s total earnings'] = [f"€{round(random['net_earning'].sum(),2):,}", f"€{round(preference['net_earning'].sum(),2):,}", f"€{round(price['net_earning'].sum(),2):,}", f"€{round(rooms['net_earning'].sum(),2):,}"]
# end of Results DataFrame

# Show Results DataFrame
st.write('**Satisfaction is measured from 1 (completely satisfied) to 5 (very dissatisfied)**')
st.table(Results.set_index('Strategy'))
st.write('---')


