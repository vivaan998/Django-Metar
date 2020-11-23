import requests, os
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

def get_station_info(sCode):

    err_msg = ''
    message = ''
    message_class = ''

    text = sCode + ".TXT"         
    base_url = 'https://tgftp.nws.noaa.gov/data/observations/metar/stations/' + text

    if requests.get(base_url).status_code == 200:
        driver.get(base_url)

        metar_soup = BeautifulSoup(driver.page_source, 'html.parser')
        meta_info = [i.getText() for i in metar_soup]

        message = "Metar Code Found!"
        message_class = 'is-success'

    else:
        message = "Metar Code Doesn't Exsits!"
        message_class = 'is-danger' 
        meta_info = None

    context = {
        "message" : message,
        "message_class" : message_class,
        "data" : meta_info[0] if meta_info is not None else meta_info
    }
    return context


def get_time(time):

    date = time.strftime("%m/%d/%Y")
    obj_time = time.strftime("%H:%M")
    
    obv_time = date + " at " + obj_time + " GMT"
    return obv_time

def get_temp(temp):

    f_temp = str(temp).replace(" C", "")
    farenhite = round((float(f_temp)*(9/5)) + 32)

    obv_temp = str(temp) + " (" + str(farenhite) + " F)"
    return obv_temp

def get_speed(speed):

    mph = speed.replace(' knots','')
    mph_speed = round(float(mph) * 1.151)

    obv_speed = str(mph_speed) +" mph " + "(" + speed + ")"
    return obv_speed