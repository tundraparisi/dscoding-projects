import pandas as pd
df = pd.read_csv('GLT_ByMajorCity.csv')

unique_cities = df['City'].nunique()
unique_countries = df['Country'].nunique()

print(unique_cities)
print(unique_countries)

missing_values = df.isnull().sum()
