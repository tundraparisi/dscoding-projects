import pandas as pd
import numpy as np

class Strategy:
    """
    This is a data structure consisting in 4 strategies (functions) which allocate guests in hotels,
    calculates net earnings per each hotel, and finally the guests' level of satisfaction.
    
    Parameters:
        guests: DataFrame 
            Is the DataFrame imported by the Hotelsdata class, which contains the guests' information.
        hotels: DataFrame
            Is the DataFrame imported by the Hotelsdata class, which contains the hotels' information.
        pref: DataFrame
            Is the DataFrame imported by the Hotelsdata class, which contains the preference's information.
    """

    def __init__(self, guests, hotels, pref):
        self.guests = guests
        self.hotels = hotels
        self.pref = pref
    

    @property
    def random(self):

        """
        This is the random strategy, which randomly allocates guests to hotels.
        
        An allocation dictionary is created to store all the guests' allocations. 

        First, it randomly orders both guests list and hotels Series, so the allocation is completeley random. The hotel Series is
        transformed into a dictionary, so it is easier to use for calculations.

        Secondly, 2 for loops are runned:
            - guest: iterates the random guest list, and retrieves the discount from the guests DataFrame, and the preference list
            of the guest from the preference DataFrame.
            - hotel: iterates the random hotel list, and if the hotel is in the guest's preference list and there are available rooms,
            then the guest is allocated to the hotel, and a room is substracted from the hotel dictionary.

        Finally, when the loops are over, both hotels' net earnings (price - discount) and guests' satisfaction are calculated.

        The final results are append to the original dictionary (allocation).

        A Pandas DataFrame of the allocation dictionary is the final output. 
        """
        # Dictionary to store all the allocations.
        allocation = {'guest': [], 'hotel': [], 'net_earning': [], 'guest_satisfaction': []}
        
        # Random list of guests.
        random_guest = np.random.choice(self.guests['guest'],size = len(self.guests)).tolist()
        
        # Pandas Series containing hotels and number of rooms.
        hotel_list = pd.Series(self.hotels['rooms'].values, index = self.hotels['hotel'])
        
        # hotel_list is randomly ordered, and transformed into a dictionary, so manipulation and calculation of room availability
        # is easier. 
        random_hotel = hotel_list.sample(frac=1).to_dict() 

        # for loop to iterate over the guests' random list, retrieving the guest's discount (from the guests DataFrame) and the list
        # of preferences (from the preference DataFrame).
        for guest in random_guest:       
            guest_discount = self.guests[self.guests['guest'] == guest]['discount'].values[0]
            priority_hotels = self.pref[self.pref['guest'] == guest].sort_values(by='priority')['hotel'].tolist()

        # for loop after the guest loop, to iterate over the random_hotel dictionary, controlling that the hotel is available and it is
        # in the guest's preference list. If available, then it will substract one room to the hotel, in the dictionary.      
            for hotel in random_hotel:
                if hotel in priority_hotels and random_hotel[hotel]>0:
                    random_hotel[hotel] -=1
        
        # After the allocation is done, the net earning is calculated by substracting the guest discount to the hotel's price. 
                    gross_earning = self.hotels[self.hotels['hotel'] == hotel]['price'].values[0]
                    net_earning = gross_earning*(1-guest_discount)

        # Calculation of the guest's satisfaction (from 1 -satisfied- to 5 -not satisfied-), based on the hotel selected for him:
        #   - 1st hotel in preferences = 1 (completely satisfied).
        #   - Among the first 25% of the hotels in the list: 2 (slighlty satisfied).
        #   - Among the second 25% of the preference: 3 (neutral).
        #   - Among the third 25% of the preference: 4 (slighlty unsatisfied).
        #   - Among the last 25% of the hotels in the list: 5 (unsatisfied).    
                    satisfaction = 1 if priority_hotels.index(hotel)+1 == 1 else(
                        2 if priority_hotels.index(hotel)+1 <= (len(priority_hotels) * 0.25) else(
                        3 if priority_hotels.index(hotel)+1 <= (len(priority_hotels) * 0.5) else(
                        4 if priority_hotels.index(hotel)+1 < (len(priority_hotels) * 0.75) else 5)))

        # Appending results from each iteration to the allocation dictionary.  
                    allocation['guest'].append(guest)
                    allocation['hotel'].append(hotel)
                    allocation['net_earning'].append(net_earning)
                    allocation['guest_satisfaction'].append(satisfaction)
                    break
        
        # Transform the dictionary to a Pandas DataFrame to easily manipulate for calculations and graphs, and returns the DataFrame.
        random_allocation = pd.DataFrame(allocation)
        return random_allocation
    

    @property
    def preference(self):
        
        """
        This is the preference strategy, which allocates guests to hotels based on the guests' preferences.
        
        An allocation dictionary is created to store all the guests' allocations.

        First, it creates a guests list and a dictionary of hotels with their available rooms.

        Secondly, 2 for loops are runned:
            - guest: iterates the guest list, and retrieves the discount from the guests DataFrame, and the preference list
            of the guest from the preference DataFrame.
            - hotel: iterates the preference list, and if the hotel has available rooms, then the guest is allocated to the hotel,
            and a room is substracted from the hotel dictionary.

        Finally, when the loops are over, both hotels' net earnings (price - discount) and guests' satisfaction are calculated.

        The final results are append to the original dictionary (allocation).

        A Pandas DataFrame of the allocation dictionary is the final output. 
        """

        # Dictionary to store all the allocations.
        allocation = {'guest': [], 'hotel': [], 'net_earning': [], 'guest_satisfaction': []}

        # List of guests.
        guest_list = self.guests['guest'].tolist()

        # Pandas Series containing hotels and number of rooms is transformed into a dictionary, so manipulation and calculation of
        # room availability is easier. 
        hotel_list = pd.Series(self.hotels['rooms'].values, index = self.hotels.hotel).to_dict()

        # for loop to iterate over the guests' list, retrieving the guest's discount (from the guests DataFrame) and the list of
        # preferences (from the preference DataFrame).    
        for guest in guest_list:
                guest_discount = self.guests[self.guests['guest'] == guest]['discount'].values[0]
                priority_hotels = self.pref[self.pref['guest'] == guest].sort_values(by='priority')['hotel'].tolist()
                
        # for loop after the guest loop, to iterate over the guest's preference list. If available, then it will substract one room
        # to the hotel, in the dictionary.
                for hotel in priority_hotels:
                    if hotel_list[hotel]>0:
                        hotel_list[hotel] -=1

        # After the allocation is done, the net earning is calculated by substracting the guest discount to the hotel's price.    
                        gross_earning = self.hotels[self.hotels['hotel'] == hotel]['price'].values[0]
                        net_earning = gross_earning*(1-guest_discount)

        # Calculation of the guest's satisfaction (from 1 -satisfied- to 5 -not satisfied-), based on the hotel selected for him:
        #   - 1st hotel in preferences = 1 (completely satisfied).
        #   - Among the first 25% of the hotels in the list: 2 (slighlty satisfied).
        #   - Among the second 25% of the preference: 3 (neutral).
        #   - Among the third 25% of the preference: 4 (slighlty unsatisfied).
        #   - Among the last 25% of the hotels in the list: 5 (unsatisfied).        
                        satisfaction = 1 if priority_hotels.index(hotel)+1 == 1 else(
                        2 if priority_hotels.index(hotel)+1 <= (len(priority_hotels) * 0.25) else(
                        3 if priority_hotels.index(hotel)+1 <= (len(priority_hotels) * 0.5) else(
                        4 if priority_hotels.index(hotel)+1 < (len(priority_hotels) * 0.75) else 5)))

        # Appending results from each iteration to the allocation dictionary.        
                        allocation['guest'].append(guest)
                        allocation['hotel'].append(hotel)
                        allocation['net_earning'].append(net_earning)
                        allocation['guest_satisfaction'].append(satisfaction)
                        break

        # Transform the dictionary to a Pandas DataFrame to easily manipulate for calculations and graphs, and returns the DataFrame.             
        priority_allocation = pd.DataFrame(allocation)
        return priority_allocation
    

    @property
    def price(self):
    
        """
        This is the price strategy, which allocates guests to hotels based on the hotels' price (form the cheapest to the most expensive).
        
        An allocation dictionary is created to store all the guests' allocations.

        First, it creates a guests list, and a dictionary of hotels ordered by price (ascending) with their available rooms.

        Secondly, 2 for loops are runned:
            - guest: iterates the guest list, and retrieves the discount from the guests DataFrame, and the preference list
            of the guest from the preference DataFrame.
            - hotel: iterates the hotel list, and if the hotel is in the guest's preference list and has available rooms,
            then the guest is allocated to the hotel, and a room is substracted from the hotel dictionary.

        Finally, when the loops are over, both hotels' net earnings (price - discount) and guests' satisfaction are calculated.

        The final results are append to the original dictionary (allocation).

        A Pandas DataFrame of the allocation dictionary is the final output. 
        """
        
        # Dictionary to store all the allocations.
        allocation = {'guest': [], 'hotel': [], 'net_earning': [], 'guest_satisfaction': []}
        
        # List of guests.
        guest_list = self.guests['guest'].tolist()

        # Pandas Series, containing hotels ordered by price (ascending) and the number of rooms available, is transformed into a
        # dictionary, so manipulation and calculation of room availability is easier.
        hotel_ordered = self.hotels.sort_values(by='price') 
        hotel_list = pd.Series(hotel_ordered['rooms'].values, index = hotel_ordered.hotel).to_dict()


        # for loop to iterate over the guests' list, retrieving the guest's discount (from the guests DataFrame) and the list of
        # preferences (from the preference DataFrame).    
        for guest in guest_list:
            guest_discount = self.guests[self.guests['guest'] == guest]['discount'].values[0]
            priority_hotels = self.pref[self.pref['guest'] == guest].sort_values(by='priority')['hotel'].tolist()

        # for loop after the guest loop, to iterate over the hotels' list. If it is in the guest's preference list and has available
        # rooms, then it will substract one room to the hotel, in the dictionary.    
            for hotel in hotel_list:
                if hotel in priority_hotels and hotel_list[hotel]>0:
                    hotel_list[hotel] -=1
        
        # After the allocation is done, the net earning is calculated by substracting the guest discount to the hotel's price.
                    gross_earning = self.hotels[self.hotels['hotel'] == hotel]['price'].values[0]
                    net_earning = gross_earning*(1-guest_discount)

        # Calculation of the guest's satisfaction (from 1 -satisfied- to 5 -not satisfied-), based on the hotel selected for him:
        #   - 1st hotel in preferences = 1 (completely satisfied).
        #   - Among the first 25% of the hotels in the list: 2 (slighlty satisfied).
        #   - Among the second 25% of the preference: 3 (neutral).
        #   - Among the third 25% of the preference: 4 (slighlty unsatisfied).
        #   - Among the last 25% of the hotels in the list: 5 (unsatisfied).    
                    satisfaction = 1 if priority_hotels.index(hotel)+1 == 1 else(
                        2 if priority_hotels.index(hotel)+1 <= (len(priority_hotels) * 0.25) else(
                        3 if priority_hotels.index(hotel)+1 <= (len(priority_hotels) * 0.5) else(
                        4 if priority_hotels.index(hotel)+1 < (len(priority_hotels) * 0.75) else 5)))

        # Appending results from each iteration to the allocation dictionary.    
                    allocation['guest'].append(guest)
                    allocation['hotel'].append(hotel)
                    allocation['net_earning'].append(net_earning)
                    allocation['guest_satisfaction'].append(satisfaction)
                    break
        
        # Transform the dictionary to a Pandas DataFrame to easily manipulate for calculations and graphs, and returns the DataFrame.
        price_allocation = pd.DataFrame(allocation)
        return price_allocation
    

    @property
    def rooms(self):
        
        """
        This is the rooms strategy, which allocates guests to hotels based on the hotels' rooms availability (form the least roomy to the
        most roomy).
        
        An allocation dictionary is created to store all the guests' allocations.

        First, it creates a guests list, and a dictionary of hotels ordered by rooms availability (ascending) with their available rooms.

        Secondly, 2 for loops are runned:
            - guest: iterates the guest list, and retrieves the discount from the guests DataFrame, and the preference list
            of the guest from the preference DataFrame.
            - hotel: iterates the hotel list, and if the hotel is in the guest's preference list and has available rooms,
            then the guest is allocated to the hotel, and a room is substracted from the hotel dictionary.

        Finally, when the loops are over, both hotels' net earnings (price - discount) and guests' satisfaction are calculated.

        The final results are append to the original dictionary (allocation).

        A Pandas DataFrame of the allocation dictionary is the final output. 
        """

        # Dictionary to store all the allocations.
        allocation = {'guest': [], 'hotel': [], 'net_earning': [], 'guest_satisfaction': []}
        
        # List of guests.
        guest_list = self.guests['guest'].tolist()

        # Pandas Series, containing hotels ordered by rooms availability (ascending) and the number of rooms available, is transformed
        # into a dictionary, so manipulation and calculation of room availability is easier.
        hotel_ordered = self.hotels.sort_values(by='rooms') 
        hotel_list = pd.Series(hotel_ordered['rooms'].values, index = hotel_ordered.hotel).to_dict()

        # for loop to iterate over the guests' list, retrieving the guest's discount (from the guests DataFrame) and the list of
        # preferences (from the preference DataFrame).        
        for guest in guest_list:
            guest_discount = self.guests[self.guests['guest'] == guest]['discount'].values[0]
            priority_hotels = self.pref[self.pref['guest'] == guest].sort_values(by='priority')['hotel'].tolist()

        # for loop after the guest loop, to iterate over the hotels' list. If it is in the guest's preference list and has available
        # rooms, then it will substract one room to the hotel, in the dictionary.    
            for hotel in hotel_list:
                if hotel in priority_hotels and hotel_list[hotel]>0:
                    hotel_list[hotel] -=1
        
        # After the allocation is done, the net earning is calculated by substracting the guest discount to the hotel's price.
                    gross_earning = self.hotels[self.hotels['hotel'] == hotel]['price'].values[0]
                    net_earning = gross_earning*(1-guest_discount)

        # Calculation of the guest's satisfaction (from 1 -satisfied- to 5 -not satisfied-), based on the hotel selected for him:
        #   - 1st hotel in preferences = 1 (completely satisfied).
        #   - Among the first 25% of the hotels in the list: 2 (slighlty satisfied).
        #   - Among the second 25% of the preference: 3 (neutral).
        #   - Among the third 25% of the preference: 4 (slighlty unsatisfied).
        #   - Among the last 25% of the hotels in the list: 5 (unsatisfied).    
                    satisfaction = 1 if priority_hotels.index(hotel)+1 == 1 else(
                        2 if priority_hotels.index(hotel)+1 <= (len(priority_hotels) * 0.25) else(
                        3 if priority_hotels.index(hotel)+1 <= (len(priority_hotels) * 0.5) else(
                        4 if priority_hotels.index(hotel)+1 < (len(priority_hotels) * 0.75) else 5)))
        
        # Appending results from each iteration to the allocation dictionary.    
                    allocation['guest'].append(guest)
                    allocation['hotel'].append(hotel)
                    allocation['net_earning'].append(net_earning)
                    allocation['guest_satisfaction'].append(satisfaction)
                    break
        
        # Transform the dictionary to a Pandas DataFrame to easily manipulate for calculations and graphs, and returns the DataFrame.
        room_allocation = pd.DataFrame(allocation)
        return room_allocation