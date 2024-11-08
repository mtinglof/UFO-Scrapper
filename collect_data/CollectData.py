from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import os
import re

class DataCollect:
    def __init__(self):
        self.driver = webdriver.Chrome()
        return
    
    # Function to click through each page of data tables. There is a chance that the table page does not change. 
    # Be aware, since this is a while loop, that the code (in theory) could get stuck if the change page action chain fails to change the page. 
    # Export data table with the report date as name to the saved_data folder. 
    def PageInfo(self, link, date):
        data_page = webdriver.Chrome()
        data_page.get(link)
        column_headers=['LINK','OCCURRED','CITY','STATE','COUNTRY','SHAPE','SUMMARY','REPORTED','MEDIA','EXPLANATION']
        list_holder = [[] for x in range(len(column_headers))]
        list_holder = self.CollectPage(data_page, list_holder, column_headers)
        while True:
            try:
                next_button = data_page.find_element(By.XPATH, '//a[@class="paginate_button next"]')
                ActionChains(data_page).scroll_to_element(next_button).scroll_by_amount(delta_x=0, delta_y=100).click(next_button).perform()
                list_holder = self.CollectPage(data_page, list_holder, column_headers)
            except: 
                break
        dict_data = {column: list_data for (column, list_data) in zip(column_headers, list_holder)}
        pd.DataFrame.from_dict(dict_data).to_csv(f"./saved_data/{date}.csv", index=False)
        return

    # Collecting data from table function. Sleep call to let page load. 
    # Sometimes, when moving pages, the page will not move, so check if link already exists in collected data. 
    def CollectPage(self, data_page, list_holder, column_headers):
        row_path = '//table/tbody/tr'
        time.sleep(2)
        for row_number in range(len(data_page.find_elements(By.XPATH, row_path))):
            link = data_page.find_element(By.XPATH, '//table/tbody/tr'+f'[{row_number+1}]/td/a').get_attribute('href')
            if link not in list_holder[0]:
                for element_number in range(len(column_headers)):
                    element_path = row_path+f'[{row_number+1}]/td[{element_number+1}]'
                    if element_number == 0: list_holder[element_number].append(link)
                    else: list_holder[element_number].append(data_page.find_element(By.XPATH, element_path).text)
        return(list_holder)
    
    # Function that will derive a list of reported dates from the NUFORC posted reports page. 
    # Skip the first row of table because of column headers and skip the last date because NUFORC has an empty date value with the current date.
    # Allow data to be collect if date is not in saved_data folder. 
    def GetDates(self):
        dates_link = 'https://nuforc.org/ndx/?id=post'
        self.driver.get(dates_link)
        dates_path = "//body/div/div/main/div/div/table/tbody/tr"
        files = [re.sub('.csv', "", file) for file in os.listdir('./saved_data')]
        date_len = len(self.driver.find_elements(By.XPATH, dates_path))
        for index in range(date_len):
            if index > 0 and index != date_len-1: 
                link_path = dates_path+f'[{index+1}]/td/u/a'
                date = self.driver.find_element(By.XPATH, link_path).text
                if date not in files: self.PageInfo(self.driver.find_element(By.XPATH, link_path).get_attribute('href'), date)

driver = DataCollect()
driver.GetDates()