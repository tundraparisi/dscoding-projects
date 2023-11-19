import pandas as pd

def combined(random, preference, price, rooms):
    random['strategy'] = 'Random'
    preference['strategy'] = 'Preference'
    price['strategy'] = 'Price'
    rooms['strategy'] = 'Room'

    combined_df = pd.concat([random, preference, price, rooms])
    return combined_df
