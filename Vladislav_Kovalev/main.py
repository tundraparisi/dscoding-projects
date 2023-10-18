import pandas as pd
from strategies.first_strategy.first_strategy_main import first_strategy_main
from strategies.second_strategy.second_strategy_main import second_strategy_main
from strategies.third_strategy.third_strategy_main import third_strategy_main
from strategies.fourth_strategy.fourth_strategy_main import fourth_strategy_main
from results_tools.construct_result.construct_result import construct_result
from utils import (
    dataHotelsPath,
    dataGuestsPath,
    dataPreferencesPath,
    firstStrategyPath,
    secondStrategyPath,
    thirdStrategyPath,
    fourthStrategyPath,
)

if __name__ == "__main__":
    # read the data
    dataHotels = pd.read_excel(dataHotelsPath)
    dataGuests = pd.read_excel(dataGuestsPath)
    dataPreferences = pd.read_excel(dataPreferencesPath)

    # random: customers are randomly distributed to the rooms until the seats or customers are exhausted;
    resultFrameFirstStrategy = first_strategy_main(
        dataHotels=dataHotels,
        dataGuests=dataGuests,
    )

    # customer preference: customers are served in order of reservation (the customer number indicates the order)
    # and are allocated to the hotel based on their preference, until the seats or customers are exhausted;
    resultFrameSecondStrategy = second_strategy_main(
        dataHotels=dataHotels,
        dataPreferences=dataPreferences,
    )

    # price: the places in the hotel are distributed in order of price, starting with the cheapest hotel
    # and following in order of reservation and preference until the places or customers are exhausted;
    resultFrameThirdStrategy = third_strategy_main(
        dataHotels=dataHotels,
        dataPreferences=dataPreferences,
    )

    # vailability: places in hotels are distributed in order of room availability, starting with
    # the most roomy hotel and subordinately in order of reservation and preference
    # until places or clients are exhausted.
    resultFrameFourthStrategy = fourth_strategy_main(
        dataHotels=dataHotels,
        dataPreferences=dataPreferences,
    )

    for resultFrame, resultPath in zip(
        [
            resultFrameFirstStrategy,
            resultFrameSecondStrategy,
            resultFrameThirdStrategy,
            resultFrameFourthStrategy,
        ],
        [
            firstStrategyPath,
            secondStrategyPath,
            thirdStrategyPath,
            fourthStrategyPath,
        ],
    ):
        resultFrameSave = construct_result(
            dataHotels=dataHotels,
            dataGuests=dataGuests,
            dataPreferences=dataPreferences,
            resultFrame=resultFrame,
        )

        resultFrameSave.to_excel(
            resultPath,
            index=False,
        )
