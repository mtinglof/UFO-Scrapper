import pandas as pd
import os
from tqdm import tqdm

class CombineClean():
    def __init__(self):
        self.geo, self.found_geo = self.GetGeo()
        self.Combine()

    def GetGeo(self):
        column_names = ['geonameid','name','asiiname','alternatenames','latitude','longitude','feature class','feature code',
                        'country code','cc2','admin1 code','admin2 code','admin3 code','admin4 code','population','elevation','dem','timezone',
                        'modification date']
        geo = pd.read_csv('./collect_data/location data/US.txt', delimiter='\t', header=None, names=column_names)
        geo['city_lower'] = geo['name'].apply(lambda x: str(x).lower())
        geo['state_lower'] = geo['admin1 code'].apply(lambda x: str(x).lower())
        found_geo = pd.read_excel('./collect_data/location data/found_us.xlsx', index_col=0).to_dict('index')
        return(geo, found_geo)

    def Combine(self):
        listed_dates = os.listdir("./collect_data/saved_data")
        df_hold = []
        for data_file in listed_dates:
            file_path = "./collect_data/saved_data/" + data_file
            df_hold.append(pd.read_csv(file_path))
        hold = pd.concat(df_hold)
        hold.to_csv('combined.csv', index=False)
        self.Clean(hold)
    
    def Clean(self, data):   
        data.reset_index(inplace=True, drop=True) 
        data['OCCURRED'] = pd.to_datetime(data['OCCURRED'], format='%m/%d/%Y %H:%M', errors='coerce')        
        data['REPORTED'] = pd.to_datetime(data['REPORTED'], format='%m/%d/%Y', errors='coerce').dt.date
        self.FindGeo(data)            

    def FindGeo(self, data):
        lat_hold = []
        long_hold = []
        pop_hold = []
        found = []
        for index in tqdm(range(data.shape[0]), total=len(data), desc="Collectiong location data"):
            city = str(data.at[index, 'CITY']).lower()
            state = str(data.at[index, 'STATE']).lower()
            key = city+"_"+state
            if key in self.found_geo.keys():
                found.append(1)
                lat = self.found_geo[key]['lat']
                long = self.found_geo[key]['long']
                pop = self.found_geo[key]['pop']
            else:
                results = self.geo.loc[(self.geo['state_lower']==state) & (self.geo['city_lower']==city) & 
                                    (self.geo['population']>0)]
                if len(results) > 0:
                    results = results.sort_values(by=['population'])
                    found.append(1)
                    lat = list(results['latitude'])[-1]
                    long = list(results['longitude'])[-1]
                    pop = list(results['population'])[-1]
                    self.found_geo[key] = {
                        'city': city,
                        'state': state,
                        'lat': lat,
                        'long': long,
                        'pop': pop
                    }
                else:
                    lat, long, pop = '', '', ''
                    found.append(0)
            lat_hold.append(lat)
            long_hold.append(long)
            pop_hold.append(pop)
        self.Export(data)

    def Export(self, data):
        data.to_csv('cleaned_reports.csv', index=False)
        pd.DataFrame.from_dict(self.found_geo, orient='index').to_excel("found_us.xlsx", index_label='id')


control = CombineClean()