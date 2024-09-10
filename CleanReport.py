import pandas
import re

report_data = pandas.read_csv('combined_reports.csv')
location10_20_data = pandas.read_csv('SUB-EST2020_ALL_clean_1.csv')
location00_09_data = pandas.read_csv('SUB-EST2009_ALL_clean_1.csv')


def full_city_check(segment):
    additional_parts = []
    segments = segment.split(" ")
    segments = [value for value in segments if value != ""]
    start_range = list(range(len(segments)))
    end_range = start_range[::-1]
    first_flag = True
    for start_index in start_range:
        for end_index in end_range:
            if first_flag:
                first_flag = False
            else:
                if (start_index != end_index+1) and (end_index+1 > start_index):
                    additional_parts.append(" ".join(segments[start_index:end_index+1]))
    return(additional_parts)


def city_clean(city, state):
    if type(city) == str:
        city_parts = re.split('[(|)|-|\|,|/]', city)
        city_parts = [value for value in city_parts if value != ""]
        for phrase in city_parts:
            result = city_search(phrase, state)
            if len(result) > 0:
                return(result)
        for phrase in city_parts:
            segment_parts = full_city_check(phrase)
            for segment in segment_parts:
                result = city_search(segment, state)
                if len(result) > 0:
                    return(result)
        return("")
    else: 
        return("")


def city_search(city_part, state):
    if city_part[-1] == " ":
        city_part = city_part[:-1]
    location_search = location_data.loc[(location_data['STATEABB']==state) & (location_data['NAMECLEAN']==city_part) & (location_data['IGNOREFLAG']==0)]
    if len(location_search) > 0:
        return(location_search)
    alt_locations = list(set(location_data.loc[(location_data['STATEABB']==state) & (location_data['IGNOREFLAG']==0)]['ALTNAME']))
    for index, alt_location in enumerate(alt_locations):
        if type(alt_location) == str:
            if city_part == alt_location or city_part in alt_location.split(" "):
                location_search = location_data.loc[(location_data['STATEABB']==state) & (location_data['ALTNAME']==alt_locations[index]) & (location_data['IGNOREFLAG']==0)]
    if len(location_search) > 0:
        return(location_search)
    return("")
    


results = []

year_hold = []
name_hold = []
pop_hold = []
not_local = []
no_city = []
bad_location = []
collision = []
bad_year = []
bad_time = []

states = list(set(location10_20_data['STATEABB']))

for report_index in range(report_data.shape[0]):
    state = report_data['State'][report_index]
    city = report_data['City'][report_index]
    if pandas.isna(report_data['Time'][report_index]):
        bad_time_flag = True
    else: 
        bad_time_flag = False
    if pandas.isna(report_data['Date'][report_index]): 
        results = [-1, -1, -1, -1, -1, -1, -1, 1]
    else:
        year = int(report_data['Date'][report_index].split("/")[-1])
        if year >= 2010:
            location_data = location10_20_data
            if year > 2020:
                location_column_name = 'POPESTIMATE' + str(2020)
            else: 
                location_column_name = 'POPESTIMATE' + str(year)
        else: 
            location_data = location00_09_data
            location_column_name = 'POP_' + str(year)
        if year >= 2000: 
            if type(city) != str or type(state) != str:
                results = [year, -1, -1, -1, -1, 1, -1, -1]
            elif state not in states:
                results = [year, -1, -1, 1, -1, -1, -1, -1]
            else:
                city = city.lower()
                location_search = city_clean(city, state)
                if len(location_search)==0:
                    results = [year, -1, -1, -1, 1, -1, -1, -1]
                else:
                    if len(location_search)==1:
                        results = [year, list(location_search['NAMECLEAN'])[0], list(location_search[location_column_name])[0], -1, -1, -1, -1, -1]
                    else:
                        if len(set(list(location_search[location_column_name]))) > 1:
                            results = [year, list(location_search['NAMECLEAN'])[0], max(list(location_search[location_column_name])), -1, -1, -1, 1, -1]
                        else:
                            results = [year, list(location_search['NAMECLEAN'])[0], list(location_search[location_column_name])[0], -1, -1, -1, -1, -1]
        else: 
            results = [year, -1, -1, -1, -1, -1, -1, -1]
    
    if bad_time_flag:
        results.append(1)
    else:
        results.append(-1)
            
    print("{}/{}".format(report_index, report_data.shape[0]), end="\r")
    year_hold.append(results[0])
    name_hold.append(results[1])
    pop_hold.append(results[2])
    not_local.append(results[3])
    no_city.append(results[4])
    bad_location.append(results[5])
    collision.append(results[6])
    bad_year.append(results[7])
    bad_time.append(results[8])

report_data['Year'] = year_hold
report_data['Clean_Name'] = name_hold
report_data['Pop'] = pop_hold
report_data['Not_Local'] = not_local
report_data['No_City'] = no_city
report_data['Bad_Location'] = bad_location
report_data['Collision'] = collision
report_data['Bad_Year'] = bad_year
report_data['Bad_Time'] = bad_time
report_data.to_csv("combined_reports_clean.csv", index=False)