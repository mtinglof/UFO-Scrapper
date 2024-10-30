from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas
import os

class DataCollect:
    def __init__(self):
        self.driver = webdriver.Chrome()
        return
    
    def Collect(self, link, date):
        data_page = webdriver.Chrome()
        data_page.get(link)
        column_headers=['LINK','OCCURRED','CITY','STATE','COUNTRY','SHAPE','SUMMARY','REPORTED','MEDIA','EXPLANATION']
        row_path = '//table/tbody/tr'
        for row_number in range(len(data_page.find_elements(By.XPATH, row_path))):
            for element_number in range(len(column_headers)):
                element_path = row_path+f'[{row_number+1}]/td[{element_number+1}]'
                if element_number == 0: print(data_page.find_element(By.XPATH, element_path+'/a').get_attribute('href'))
                else: print(data_page.find_element(By.XPATH, element_path).text)
        return
    
    def CheckDate(self):
        dates_link = 'https://nuforc.org/ndx/?id=post'
        self.driver.get(dates_link)
        dates_path = "//body/div/div/main/div/div/table/tbody/tr"
        for index, link in enumerate(self.driver.find_elements(By.XPATH, dates_path)):
            if index > 0: 
                link_path = '//td/u/a'
                self.Collect(link.find_element(By.XPATH, link_path).get_attribute('href'), link.find_element(By.XPATH, link_path).text)

driver = DataCollect()
driver.CheckDate()