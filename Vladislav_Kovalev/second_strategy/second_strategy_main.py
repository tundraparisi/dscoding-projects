import pandas as pd
from first_strategy.tools.decrement.decrement_dictionary_with_deletion import (
    decrement_dictionary_with_deletion,
)
from first_strategy.tools.creation.create_available_rooms import create_available_rooms
from second_strategy.tools.choice.preference_choice_key_dict import (
    preference_choice_key_dict,
)
from second_strategy.tools.creation.create_guests_query import create_guests_query


def second_strategy_main(
    *,
    dataHotels,
    dataPreferences,
    dataGuests,
) -> pd.DataFrame:
    """
    Calculation of main locations frame for second strategy

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

    # preferences transform into lists
    dataPreferences = dataPreferences.sort_values(["guest", "priority"])
    dataPreferences = dataPreferences.groupby(["guest"], as_index=False)["hotel"].agg(
        ", ".join
    )
    dataPreferences["hotel"] = dataPreferences["hotel"].str.split(", ")
    dataPreferences = create_guests_query(dataPreferences=dataPreferences)
    dataPreferences = dataPreferences.sort_values("order")

    # main strategy loop
    for indexGuest, infoGuest in dataPreferences.iterrows():
        guest, hotelPreferences, order = (
            infoGuest["guest"],
            infoGuest["hotel"],
            infoGuest["order"],
        )

        # select hotel
        hotelForGuest = preference_choice_key_dict(
            preferenceList=hotelPreferences,
            dictionaryForChoice=availableRoomsDict,
        )
        resultDict.update({guest: hotelForGuest})

        # reserve hotel
        if hotelForGuest is not None:
            availableRoomsDict = decrement_dictionary_with_deletion(
                dictionaryForUpdate=availableRoomsDict,
                keyDecrement=hotelForGuest,
            )

    resultFrame = pd.DataFrame.from_dict(
        {"guest": list(resultDict.keys()), "hotel": list(resultDict.values())}
    )

    return resultFrame
