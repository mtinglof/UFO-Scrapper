from selenium import webdriver
import pandas
import os

class DataCollect:
    def __init__(self):
        self.driver = webdriver.Chrome(r".\chromedriver_win32\chromedriver.exe")
        return

    def Collect(self):
        column_headers = ['Datetime', 'City', 'State', 'Shape', 'Duration', 'Summary', 'Posted']
        dates_hold = self.PreparedDates()
        for date_link in dates_hold:
            link = "http://www.nuforc.org/webreports/ndxp" + date_link + ".html"
            self.driver.get(link)
            row_path = "//table/tbody/tr"
            data_hold = {}
            for row_index in range(len(self.driver.find_elements_by_xpath(row_path))):
                data_path = "//table/tbody/tr[{}]/td".format(row_index)
                if row_index != 0:
                    data_hold[row_index] = {}
                    for column_index, row_item in enumerate(self.driver.find_elements_by_xpath(data_path)):
                        data_hold[row_index][column_headers[column_index]] = row_item.text
            data_hold = pandas.DataFrame.from_dict(data_hold, orient='index', columns=column_headers)
            save_path = "./saved_data/" + date_link + ".csv"
            data_hold.to_csv(save_path, index= False)  

    def PreparedDates(self):
        dates_hold = []
        file_dates = []
        self.driver.get("http://www.nuforc.org/webreports/ndxpost.html")
        date_path = "//table/tbody/tr"
        listed_dates = os.listdir("./saved_data")
        for found_date in listed_dates:
            file_dates.append(found_date.split(".")[0])
        dates = self.driver.find_elements_by_xpath(date_path)
        for date_item in dates:
            date = date_item.text.split(" ")
            if len(date) > 1:
                date = date[0]
                date_link = date.split("/")
                date_link = date_link[2][-2:] + date_link[0] + date_link[1]
                if date_link not in file_dates:
                    dates_hold.append(date_link)
        return(dates_hold)

data_collect = DataCollect()
data_collect.Collect()