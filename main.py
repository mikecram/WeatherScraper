from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

beginTimeFormatted = time.asctime(time.localtime(time.time()))
beginTime = time.time()
print(f'''WeatherScraper ☁☀⚡❄☂🌀
Started at: {beginTimeFormatted}''')

# Set path to web driver being used, in this case it's Chrome.
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# This is the link type you need, an hour-by-hour for a city. Example link:
# driver.get("https://weather.com/weather/hourbyhour/l/ebf31a11cc5d14b2172aa73e8a7f7689733573afc580d8a4920edcf227b95a13")
print("Opening browser...")
driver.get("https://weather.com/weather/hourbyhour/l/a28b7610302e8eb27bef2d081530cbbe826326e94fa0216223d07246138cc364")

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
# This is for use when naming the csv file
locationCity = locationOfScrape[0:-4]
locationState = locationOfScrape[-2:]
print("2 of 4 done")

timeOfScrape = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "HourlyForecast--timestamp--2Q9Cb"))
).text
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
# Comment out "writer.writerow(tupTitle)" to append to an already existing file without adding the title line.
writer.writerow(tupTitle)

# Scrape data for each hour up to 24 hours in the future
# then store data in lists
# then write rows of list data into csv
for i in range(25):
    hourlyDetails.append(hourlyList.find_element_by_id(f'detailIndex{i}'))
    detailsTime.append(hourlyDetails[i].find_element_by_class_name("DetailsSummary--daypartName--1Mebr").text)
    detailsTemp.append(hourlyDetails[i].find_element_by_class_name("DetailsSummary--temperature--3FMlw").text)
    detailsPrecip.append(hourlyDetails[i].find_element_by_class_name("DetailsSummary--precip--2ARnx").text)

    print(f'''Hours forward: {i}
    Time: {detailsTime[i]}
    Temp F°: {detailsTemp[i]}
    Precip: {detailsPrecip[i]}''')

    time.sleep(0.2)
# Create a row to be written into the csv file
    tup = (f"{beginTimeFormatted}", f"{timeOfScrape}", f"{locationCity}", f"{locationState}", f"{detailsTime[i]}",f"{detailsTemp[i]}", f"{detailsPrecip[i]}")
    writer.writerow(tup)
    print(f'''Row {i+1} written to file
    ____________________''')

# Close file, close web driver
print("Closing browser...")
f.close()
driver.quit()
print("Browser closed.")
endTime = time.time() - beginTime
print(f'Scrape completed in: {endTime} secs')


