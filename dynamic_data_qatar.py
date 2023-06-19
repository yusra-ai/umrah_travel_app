import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

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
    'bookingClass': 'B',
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
    'currency':'USD'
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
for flight_element in elements:

    # get html for each flight element
    html_content = flight_element.get_attribute("innerHTML")
    soup = BeautifulSoup(html_content, "html.parser")
    flight_card = soup.find('booking-flight-card')

    flight_info = {
        'tag': flight_card.find('span', class_='flight-card__tag').text.strip(),
        'departure_time': flight_card.find('h3', class_='at-flight-card-depart-time').text.strip(),
        'origin_code': flight_card.find('p', class_='at-flight-card-origin-code').text.strip(),
        'stop_info': flight_card.find('p', class_='flight-card__stop-info').text.strip(),
        'arrival_time': flight_card.find('span', class_='at-flight-card-arrival-time').text.strip(),
        'destination_code': flight_card.find('p', class_='at-flight-card-destination-code').text.strip(),
        'flight_details_link': flight_card.find('a', class_='flight-card__link')['href']
    }

    flight_name = flight_element.text
    print("-----------------------")
    print(flight_name)
    print("-----------------------")

# Close the browser
browser.quit()
