from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os.path
from os import path
import time
import csv

# Connect to DB
import mongoDBConn

# Start
beginTimeFormatted = time.asctime(time.localtime(time.time()))
beginTime = time.time()
print(f'''WeatherScraper ☁☀⚡❄☂🌀
Started at: {beginTimeFormatted}''')

# Set path to web driver being used, in this case it's Chrome.
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# Data to be scraped: New Hampshire Top 5 Cities
citiesTop5NH = ["Manchester", "Nashua", "Concord", "Derry", "Dover"]
linkListNH = {
    "Manchester": "https://weather.com/weather/hourbyhour/l/a28b7610302e8eb27bef2d081530cbbe826326e94fa0216223d07246138cc364",
    "Nashua": "https://weather.com/weather/hourbyhour/l/5cfead018a9910a365636982fb15a23b509c2f3bf8e8730361cf76026eaf0341",
    "Concord": "https://weather.com/weather/hourbyhour/l/3b7ae74f5b0cd50daf16c234e487aa76668973a7f3bd06b5b5333d08ed378e39",
    "Derry": "https://weather.com/weather/hourbyhour/l/6bbf78aeb89e180d05b11e1da942cec98b3c192065e2100743274684a33649ed",
    "Dover": "https://weather.com/weather/hourbyhour/l/99a42d3e0de60295eaff862b481349e6967fbcbad720f5817dfb1ff1203f914b"
}

# This is the link type you need, an hour-by-hour for a city. Example link:
# driver.get("https://weather.com/weather/hourbyhour/l/ebf31a11cc5d14b2172aa73e8a7f7689733573afc580d8a4920edcf227b95a13")
for city in citiesTop5NH:
    print("Opening browser...")
    driver.get(f"{linkListNH[city]}")

    # Give 5 seconds to load the page and all elements needed.
    # If it can't find elements correctly, try increasing the range.
    for x in range(5):
        print(f'Page loading... {x+1}')
        time.sleep(1)

    # Makes sure elements to be scraped are found before scraping
    print("Locating elements...")
    hourlyList = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "HourlyForecast--DisclosureList--OznTI"))
        )
    print("1 of 4 done")

    locationOfScrape = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "LocationPageTitle--PresentationName--Injxu"))
    ).text
    # Define variables for city and state
    locationCity = locationOfScrape[0:-4]
    locationState = locationOfScrape[-2:]
    print("2 of 4 done")

    rawTimeOfScrape = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "HourlyForecast--timestamp--2Q9Cb"))
    ).text
    timeOfScrape = rawTimeOfScrape[6:]
    print("3 of 4 done")

    dayOfScrape = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "HourlyForecast--longDate--3khKr"))
    ).text
    print("4 of 4 done")

    # Define lists in order to hold 25 points of hourly data
    hourlyDetails = []
    detailsTime = []
    detailsTemp = []
    detailsPrecip = []
    # Create list for uploading 25 points of hourly data as documents
    # to a collection named CITY_STATE
    mongoDBPost = []
    collection = mongoDBConn.db[f"{locationCity}_{locationState}"]

    print("Elements located successfully.")
    print("Scraping...")
    time.sleep(1)

    print(f'''**********
Location: {locationOfScrape}
Time: {timeOfScrape}
Day: {dayOfScrape}
**********''')

    # Create a csv and write the title row in a tuple
    f = open(f"{locationCity}_{locationState}.csv", "a", newline="")
    tupTitle = ("Timestamp", "Website Time", "City", "State", "Time","Temperature", "Precipitation")
    writer = csv.writer(f)
    # Comment out "writer.writerow(tupTitle)" to append to
    # an already existing file without adding the title line.
    writer.writerow(tupTitle)

    # Scrape data for each hour up to 24 hours in the future
    # then store data in lists
    # then write rows of list data into csv
    for i in range(25):
        hourlyDetails.append(hourlyList.find_element_by_id(f'detailIndex{i}'))
        detailsTime.append(hourlyDetails[i].find_element_by_class_name("DetailsSummary--daypartName--1Mebr").text)
        detailsTemp.append(hourlyDetails[i].find_element_by_class_name("DetailsSummary--temperature--3FMlw").text)
        detailsPrecip.append(hourlyDetails[i].find_element_by_class_name("DetailsSummary--precip--2ARnx").text)

        # print(f'''Hours forward: {i}
        # Time: {detailsTime[i]}
        # Temp F°: {detailsTemp[i]}
        # Precip: {detailsPrecip[i]}''')

        time.sleep(0.1)
        # Create a row to be written into the csv file
        tup = (f"{beginTimeFormatted}", f"{timeOfScrape}", f"{locationCity}", f"{locationState}", f"{detailsTime[i]}",f"{detailsTemp[i]}", f"{detailsPrecip[i]}")
        writer.writerow(tup)
        print(f'''Row {i+1}/25 written to file''')

        # Create a dict to be uploaded to mongoDB
        mongoDBPost.append({
            "Timestamp": f"{beginTimeFormatted}",
            "Website_Time": f"{timeOfScrape}",
            "City": f"{locationCity}",
            "State": f"{locationState}",
            "Forecast_Time": f"{detailsTime}",
            "Forecast_Temp": f"{detailsTemp}",
            "Forecast_Precip": f"{detailsPrecip}"
        })
        print(mongoDBPost)
    # Close file
    print("Closing file...")
    f.close()
    print(f'{city}, {locationState} weather data written to {city}_{locationState}.csv.')
    collection.insert_one(mongoDBPost[24])
    print(f"Inserted data into mongoDB collection: {locationCity}_{locationState}")

# Close browser
driver.close()
endTime = time.time() - beginTime
endMinutes = endTime/60
print(f'Scrape completed in: {endTime} secs')


