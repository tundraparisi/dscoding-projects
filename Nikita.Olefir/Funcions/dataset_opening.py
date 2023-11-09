import pandas as pd

def open_csv_as_dataframe(file_path:str):
    """ This function opens a csv file as pandas dataframe

    Args:
        file_path (str): the path to the csv file downloaded on a computer

    Returns:
       pd.DataFrame: returns a pandas dataframe
    """    
    try:
        dataframe = pd.read_csv(file_path)
        return dataframe
    except Exception as e:
        print(f"Error reading csv file: {e}")
