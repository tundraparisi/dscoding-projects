import pandas as pd
from first_strategy.tools.decrement.decrement_dictionary_with_deletion import (
    decrement_dictionary_with_deletion,
)
from first_strategy.tools.random.random_choice_key_dict import random_choice_key_dict
from first_strategy.tools.creation.create_available_rooms import create_available_rooms


def first_strategy_main(
    *,
    dataHotels,
    dataPreferences,
    dataGuests,
) -> pd.DataFrame:
    """
    Calculation of main locations frame for first strategy

    Parameters
    ----------
    dataHotels: pd.DataFrame
        dataframe of hotels and rooms
    dataPreferences: str
        dataframe of preferences
    dataGuests: pd.DataFrame
        dataframe of guests

    Returns
    -------
    pd.DataFrame
        DataFrame with guests and locations
    """
    resultDict = {}

    availableRoomsDict = create_available_rooms(
        dataHotels=dataHotels,
    )
    random_choice_key_dict(dictionaryForChoice=availableRoomsDict)

    guests = dataGuests["guest"].drop_duplicates()
    for guest in guests:
        hotelForGuest = random_choice_key_dict(dictionaryForChoice=availableRoomsDict)
        resultDict.update({guest: hotelForGuest})
        availableRoomsDict = decrement_dictionary_with_deletion(
            dictionaryForUpdate=availableRoomsDict,
            keyDecrement=hotelForGuest,
        )
    resultFrame = pd.DataFrame.from_dict(
        {"guest": list(resultDict.keys()), "hotel": list(resultDict.values())}
    )
    return resultFrame
