import pandas as pd

class CISIData:

    #initialize dataset as an attribute
    def __init__(self):
        self.dataset = None
    
    #load dataset from csv file
    def load_data_from_csv(self, file_path):
        import pandas as pd
        self.dataset = pd.read_csv(file_path) 

    #show dataset
    def retrieve_data(self):
            return self.dataset
        
    #show how much rows loadd dataset contains
    def data_info(self):
        if self.dataset is not None:
            return f"Dataset information: {len(self.dataset)} rows loaded"
        else:
            return "No dataset loaded yet"
    
    #panda's head method to show first 5 rows
    def get_head(self, rows = 5):
            return self.dataset.head(rows)
    
    #panda's tail method to show last 5 rows
    def get_tail(self, rows = 5):
         return self.dataset.tail(rows)