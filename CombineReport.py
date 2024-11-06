import pandas
import os

listed_dates = os.listdir("./saved_data")
df_hold = []
for data_file in listed_dates:
    file_path = "./saved_data/" + data_file
    df_hold.append(pandas.read_csv(file_path))
df_main = pandas.concat(df_hold)
df_main.to_csv("combined_reports.csv", index=False)