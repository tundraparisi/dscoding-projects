import pandas as pd

file=open('/Users/tesi/Downloads/hotels/hotels.xlsx','r')
def import_data(path):
	with open ("/Users/tesi/Downloads/hotels/hotels.xlsx","r") as file:
		data=file.readlines()
	return data



