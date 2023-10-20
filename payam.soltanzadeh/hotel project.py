import pandas as pd

# Load the datasets
hotels = pd.read_excel('/.')
guests = pd.read_excel('/')
preferences = pd.read_excel('/mnt/data/preferences.xlsx')

# Explore the first few rows of each dataset
(hotels.head(), guests.head(), preferences.head())
