import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import pprint

# Set up browser options
options = Options()
# options.add_argument('--headless')  # Run the browser in headless mode (without UI)
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument('--disable-dev-shm-usage')  # Disable /dev/shm usage to prevent running out of memory in Linux containers

# Specify the path to the ChromeDriver executable
webdriver_path = '/Users/hassanpasha/github/chromedriver'

# Set up the service
service = Service(webdriver_path)

# Launch the browser
browser = webdriver.Chrome(service=service, options=options)

# Set the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Set the URL and parameters
url = 'https://www.qatarairways.com/app/booking/flight-selection'
params = {
    'upsellCallId': '123',
    'bookingClass': 'E',
    'tripType': 'O',
    'selLang': 'en',
    'fromStation': 'ISB',
    'from': 'Islamabad',
    'toStation': 'ORD',
    'to': 'Chicago',
    'departing': '2023-07-20',
    'adults': '1',
    'children': '0',
    'infants': '0',
    'teenager': '0',
    'ofw': '0',
    'promoCode': '',
    'flexibleDate': 'off',
    'cid': 'SXIN23456993M',
    'currency': 'USD'
}

# Construct the URL with parameters
url_with_params = f'{url}?{"&".join(f"{key}={value}" for key, value in params.items())}'

# Navigate to the URL
browser.get(url_with_params)

# Wait for the dynamic content to load
wait = WebDriverWait(browser, 10)

elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[id^="at-flight-search-result-"]')))


# Extract the flight details
# flight_elements = browser.find_elements(By.CSS_SELECTOR, '[id^="at-flight-search-result-"]')

flights = []
for flight_element in elements:

    # get html for each flight element
    html_content = flight_element.get_attribute("innerHTML")
    soup = BeautifulSoup(html_content, "html.parser")
    flight_card = soup.find('booking-flight-card')

    flight_info = {}

    tag_element = flight_card.find('span', class_='flight-card__tag')
    flight_info['tag'] = tag_element.text.strip() if tag_element else ''

    departure_time_element = flight_card.find('h3', class_='at-flight-card-depart-time')
    flight_info['departure_time'] = departure_time_element.text.strip() if departure_time_element else ''

    origin_code_element = flight_card.find('p', class_='at-flight-card-origin-code')
    flight_info['origin_code'] = origin_code_element.text.strip() if origin_code_element else ''

    stop_info_element = flight_card.find('p', class_='flight-card__stop-info')
    flight_info['stop_info'] = stop_info_element.text.strip() if stop_info_element else ''

    arrival_time_element = flight_card.find('span', class_='at-flight-card-arrival-time')
    flight_info['arrival_time'] = arrival_time_element.text.strip() if arrival_time_element else ''

    destination_code_element = flight_card.find('p', class_='at-flight-card-destination-code')
    flight_info['destination_code'] = destination_code_element.text.strip() if destination_code_element else ''

    cabin_cards = soup.find_all('a', class_='cabin-card')
    cabin_info = []


    for cabin_card in cabin_cards:
        cabin = {}

        cabin_class_element = cabin_card.find('span', class_='ng-tns-c88-1')

        cabin['cabin_class'] = cabin_class_element.text.strip() if cabin_class_element else ''

        price_element = cabin_card.find('span', class_='fit-child ng-tns-c88-1')
        cabin['price'] = price_element.text.strip() if price_element else ''

        cabin_info.append(cabin)


    flight_info['cabin_info'] = cabin_info

    flights.append(flight_info)



# Close the browser

df = pd.DataFrame(flights)
x = 1
browser.quit()


