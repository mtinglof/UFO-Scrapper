import pandas as pd

column_names = ['geonameid','name','asiiname','alternatenames','latitude','longitude','feature class','feature code',
                'country code','cc2','admin1 code','admin2 code','admin3 code','admin4 code','population','elevation','dem','timezone',
                'modification date']
df = pd.read_csv('./collect_data/location data/US.txt', delimiter='\t', header=None, names=column_names)  
print(df)
