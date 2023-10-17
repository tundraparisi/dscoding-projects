import pandas as pd
from first_strategy.first_strategy_main import first_strategy_main
from second_strategy.second_strategy_main import second_strategy_main
from construct_result.construct_result import construct_result

dataHotels = pd.read_excel("./Vladislav_Kovalev/hotels/hotels.xlsx")
dataGuests = pd.read_excel("./Vladislav_Kovalev/hotels/guests.xlsx")
dataPreferences = pd.read_excel("./Vladislav_Kovalev/hotels/preferences.xlsx")

resultFrame = first_strategy_main(
    dataHotels=dataHotels,
    dataGuests=dataGuests,
)

result_first_strategy = construct_result(
    dataGuests=dataGuests, dataHotels=dataHotels, resultFrame=resultFrame
)

resultFrame = second_strategy_main(
    dataHotels=dataHotels,
    dataGuests=dataGuests,
    dataPreferences=dataPreferences,
)

result_second_strategy = construct_result(
    dataGuests=dataGuests, dataHotels=dataHotels, resultFrame=resultFrame
)

print(result_first_strategy)
