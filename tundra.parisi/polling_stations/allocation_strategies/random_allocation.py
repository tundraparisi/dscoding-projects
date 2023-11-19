import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import data

voters = pd.read_excel('data/voters.xlsx')
voters.head()
polling_stations = pd.read_excel('data/polling_stations.xlsx')
polling_stations.head()

# class Hello:
#     def __init__(self):
#         print('Hello')

class RandomVoterAllocator:
    def __init__(self, voters, polling_stations):
        self.voters = voters
        self.polling_stations = polling_stations
# I define this function with the two arguments
    def random_allocation(self):
    # I use numpy library to mix the order of the voters
        np.random.shuffle(self.voters)
    # create an empty dictionary
        allocation = {}

        for voter in voters:
        #every voter get assigned a polling_station
            station = np.random.choice(self.polling_stations)
        # if the station is already in the dictionary, the voter get appended as a new element
            if station in allocation:
                allocation[station].append(voter)
        #otherwise the program creates a new key and the voter is the associated value
            else:
                allocation[station] = [voter]
        return allocation
    
voters = voters['voter'].values
polling_stations = polling_stations['polling_station'].values

# I create an istance of RandomVoterAllocator
allocator = RandomVoterAllocator(voters, polling_stations)

# call the random allocation method on the allocator instance
allocation_result = allocator.random_allocation()

plt.bar(allocation_result.keys(), [len(voters) for voters in allocation_result.values()])
plt.xlabel('Polling Stations')
plt.ylabel('Number of voters allocated')
plt.title('Random allocation')
plt.xticks(rotation=45)
plt.show()