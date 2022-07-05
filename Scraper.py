from datetime import date, datetime
import time
from urllib.parse import urlencode
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import date
import re
import json


class Website:
    def __init__(self, base_url: str, hotels_per_page: int, page_token: str):
        self.base_url = base_url
        self.hotels_per_page = hotels_per_page
        self.page_token = page_token
    
    def generage_url(self, dest: str, checkin: date, checkout: date):
        pass

    def change_page(self, url: str, page: int):
        return re.sub(f'{self.page_token}=\d+', f'{self.page_token}={page}', url)


class TravelYandex(Website):
    def __init__(self):
      super().__init__('https://travel.yandex.ru/hotels/', 25, 'navigationToken')

    def numToMonth(num):
        return {
                1: 'Январь',
                2: 'Февраль',
                3: 'Март',
                4: 'Апрель',
                5: 'Май',
                6: 'Июнь',
                7: 'Июль',
                8: 'Август',
                9: 'Сентябрь', 
                10: 'Октябрь',
                11: 'Ноябрь',
                12: 'Декабрь'
        }[num]

    def generage_url(self, dest: str, checkin: date, checkout: date):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        driver = webdriver.Chrome(options=option)
        driver.get(base_url)
        driver.maximize_window()

        city_input = driver.find_element(By.XPATH, "//input[@class='w_eHd input_center']")
        city_input.clear()
        city_input.send_keys(dest)
        time.sleep(1)
        elem = driver.find_element(By.XPATH, "//div[@class='rC02U _PIrG sfzRD w5F6Y P0ZeS']")
        elem.click()
        time.sleep(1)

        #load calendar
        months_list = driver.find_elements(By.XPATH, "//div[@class='monthsList']//div")
        months_list[-1].click()
        #looking for correct month index
        checkin_month_index = 0 #февраль - 7
        for i in range(0, 12):
            if(months_list[i].text.__contains__(self.numToMonth(checkin.month))):
                checkin_month_index = i
                break
        checkout_month_index = checkin_month_index + checkout.month - checkin.month
        time.sleep(1)

        month_counter = -1

        for day in driver.find_elements(By.XPATH, "//div[@class='mYiO8']/div/span"):
            if(day.text == "1"):
                month_counter = month_counter + 1
            if(month_counter == checkin_month_index and day.text == checkin.day.__str__()):
                day.click()
            if(month_counter == checkout_month_index and day.text == checkout.day.__str__()):
                day.click()
                break


        submit_button = driver.find_element(By.XPATH, "//button[@class='vHqxX z8gtM']")
        submit_button.click()

        time.sleep(2)
        base_url = driver.current_url
        driver.quit()

        return base_url



class Booking(Website):
    def __init__(self):
      super().__init__('https://www.booking.com/searchresults.ru.html', 25, 'offset')

    def generate_url(self, dest: str, checkin: date, checkout: date):
        new_url = self.base_url + "?" + urlencode(
            {
                "ss": dest,
                "checkin_year": checkin.year,
                "checkin_month": checkin.month,
                "checkin_monthday": checkin.day,
                "checkout_year": checkout.year,
                "checkout_month": checkout.month,
                "checkout_monthday": checkout.day,
                "no_rooms": 1,
                "offset": 0
            }
        )
        return new_url



class Parser:
    def get_hotel_urls(website: Booking, dest: str, checkin: date, checkout: date):
        print(website.base_url)
    
    def get_hotel_urls(website: TravelYandex, dest: str, checkin: date, checkout: date):
        print(website.base_url)gjhg


sites = [Booking(), TravelYandex()]


for i in sites:
    Parser.get_hotel_urls(i, 'asd', date(2022,1,1), date(2022,1,1))
