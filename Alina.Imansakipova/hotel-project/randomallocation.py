import pandas as pd
import random

import openpyxl
hotelsdata = pd.read_excel(r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/hotels.xlsx").set_index('hotel')
guestdata = pd.read_excel(r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/guests.xlsx").set_index('guest')
preferencesdata=pd.read_excel(r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/preferences.xlsx").set_index(['guest','hotel'])
from satisfactionpercentage import calculate_satisfaction_percentage

def allocate_random_hotel(guest_id, guest_row, hotelsdata, preferences):
    available_hotels = hotelsdata[hotelsdata['rooms'] > 0]
    if available_hotels.empty:
        return None

    # randomly picking the hotel
    random_available_hotel_id = random.choice(available_hotels.index)
    # returning the row (aka the room)
    random_available_hotel_row = available_hotels.loc[random_available_hotel_id]
    # excluding the room from table of available rooms
    random_available_hotel_row['rooms'] -= 1

    paid_price_coefficient = 1 - guest_row['discount']
    paid_price = random_available_hotel_row['price'] * paid_price_coefficient

    satisfaction = calculate_satisfaction_percentage(guest_id, random_available_hotel_id, preferences)

    return [guest_id, random_available_hotel_id, satisfaction, paid_price]

def get_random_allocation(hotelsdata, guestsdata, preferencesdata):
    allocation = pd.DataFrame(columns=['guest_id', 'hotel_id', 'satisfaction_percentage', 'paid_price'])

    # randomizing guests
    shuffled_guests = guestsdata.sample(frac=1, random_state=42)
    # we're taking every guest_id AND every pair guest_id|discount
    for guest_id, guest_row in shuffled_guests.iterrows():
        allocation_entry = allocate_random_hotel(guest_id, guest_row, hotelsdata, preferencesdata)
        if allocation_entry is not None:
            allocation.loc[len(allocation)] = allocation_entry

    return allocation