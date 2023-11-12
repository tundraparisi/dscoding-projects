import pandas as pd


def average_elo(dataframe: pd.DataFrame):
    """_summary_

    Argumens:
        dataframe (pd.DataFrame): a pandas dataframe that contains information about the ELO rating of players

    Returns:
        pd.DataFrame: returns a pandas dataframe that has a "average_elo" column, represening the average rating of a rated game among two chess players

    ---

    Examples:
        dataframe["average_elo"] = (dataframe["average_elo"]+dataframe["black_rating"])
    """
    
    dataframe["average_elo"] = (
        dataframe["white_rating"] + dataframe["black_rating"]
    ) / 2
    return dataframe
