# WeatherScraper
___
## About
WeatherScraper is a chunk of python that scrapes hour-by-hour weather data from various cities on https://weather.com. You can feed it a link with "driver.get(*link*)" and it will pull 24 hrs of the forecast for that city.

My main goal is to scrape weather data at hourly intervals in order to assess accuracy of weather forecasts in many cities throughout multiple states in the US.

***This uses Selenium and requires ChromeDriver at "C:\Program Files (x86)\chromedriver.exe". You can download ChromeDriver at https://chromedriver.chromium.org/downloads.***

Scraped data is appended to a CSV file titled: "CITY_STATE.csv" such as "Boston_MA.csv."
