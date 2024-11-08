import pandas as pd
import os

class CombineClean():
    def __init__(self):
        self.Combine()

    def Combine(self):
        listed_dates = os.listdir("./saved_data")
        df_hold = []
        for data_file in listed_dates:
            file_path = "./saved_data/" + data_file
            df_hold.append(pd.read_csv(file_path))
        hold = pd.concat(df_hold)
        hold.to_csv('combined.csv', index=False)
        self.Clean(hold)
    
    def Clean(self, data):    
        data['OCCURRED'] = pd.to_datetime(data['OCCURRED'], format='%m/%d/%Y %H:%M', errors='coerce')        
        data['REPORTED'] = pd.to_datetime(data['REPORTED'], format='%m/%d/%Y', errors='coerce').dt.date             
        data.to_csv('cleaned_reports.csv', index=False)

control = CombineClean()