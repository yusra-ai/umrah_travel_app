from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt


def setup_selenium_crawler(webdriver_path='/Users/hassanpasha/github/chromedriver', headless = False):

    """
      Set up and configure a Selenium browser instance for web scraping.

      Args:
          webdriver_path (str, optional): The path to the ChromeDriver executable. Defaults to '/Users/hassanpasha/github/chromedriver'.
          headless (bool, optional): Flag indicating whether to run the browser in headless mode. Defaults to False.

      Returns:
          selenium.webdriver.Chrome: The initialized Selenium browser instance.

    """

    # Set up browser options
    options = Options()
    if headless is True:

        # Run the browser in headless mode (without UI)
        options.add_argument('--headless')

    # Bypass OS security model
    options.add_argument('--no-sandbox')

    # Disable /dev/shm usage to prevent running out of memory in Linux containers
    options.add_argument('--disable-dev-shm-usage')

    # Specify the path to the ChromeDriver executable
    webdriver_path = webdriver_path

    # Set up the service
    service = Service(webdriver_path)

    # Set the headers
    browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                         'Chrome/91.0.4472.124 Safari/537.36',
    headers = {
        'User-Agent': browser_user_agent,
        'Accept-Language': 'en-US,en;q=0.9',
    }

    options.add_argument(f'user-agent={headers["User-Agent"]}')


    # Launch the browser
    browser = webdriver.Chrome(service=service, options=options)



    return browser


def get_flight_data_qatar(booking_class: str, from_airport_code: str, to_airport_code: str,
                          departing_date_year_month_day: str, adults_count: str, child_count: str,
                          infant_count: str, currency='usd', sell_language='en', browser=setup_selenium_crawler()) -> pd.DataFrame:
    """
      Retrieves flight data from Qatar Airways website using the specified parameters.

      Args:
          booking_class (str): The booking class for the flight.
          from_airport_code (str): The IATA code of the departure airport.
          to_airport_code (str): The IATA code of the arrival airport.
          departing_date_year_month_day (str): The date of departure in the format 'YYYY-MM-DD'.
          adults_count (str): The number of adult passengers.
          child_count (str): The number of child passengers.
          infant_count (str): The number of infant passengers.
          currency (str, optional): The currency code for prices. Defaults to 'usd'.
          sell_language (str, optional): The language for displaying the website. Defaults to 'en'.
          browser (selenium.webdriver.Chrome, optional): The initialized Selenium browser instance. Defaults to setup_selenium_crawler().

      Returns:
          pd.DataFrame: Flight data as a pandas DataFrame.


       Example :

            booking_class = 'Business'  # Booking class, e.g., 'Business', 'Economy', etc.
            from_airport_code = 'ISB'  # Departure airport code, e.g., 'ISB' for Islamabad
            to_airport_code = 'ORD'  # Destination airport code, e.g., 'ORD' for Chicago O'Hare
            departing_date_year_month_day = '2023-06-20'  # Departure date in the format 'YYYY-MM-DD'
            adults_count = '1'  # Number of adult passengers
            child_count = '0'  # Number of child passengers
            infant_count = '0'  # Number of infant passengers
            currency = 'usd'  # Currency for prices, e.g., 'usd', 'eur', etc.
            sell_language = 'en'  # Language for the booking process, e.g., 'en' for English



      """

    # Set the URL and parameters

    url = 'https://www.qatarairways.com/app/booking/flight-selection'

    params = {
        'bookingClass': booking_class,
        'tripType': 'O',
        'selLang': sell_language,
        'fromStation': from_airport_code,
        'toStation': to_airport_code,
        'departing': departing_date_year_month_day,
        'adults': adults_count,
        'children': child_count,
        'infants': infant_count,
        'ofw': '0',
        'flexibleDate': 'off',
        'currency': currency
    }


    # Construct the URL with parameters
    url_with_params = f'{url}?{"&".join(f"{key}={value}" for key, value in params.items())}'

    # Navigate to the URL
    browser.get(url_with_params)

    # Wait for the dynamic content to load
    wait = WebDriverWait(browser, 10)

    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[id^="at-flight-search-result-"]')))

    flights = []

    for flight_element in elements:

        # get html for each flight element
        html_content = flight_element.get_attribute("innerHTML")
        soup = BeautifulSoup(html_content, "html.parser")
        flight_card = soup.find('booking-flight-card')
        date_crawled = dt.datetime.today().strftime('%Y-%m-%d')

        flight_info = {}

        flight_info['date_crawled'] = date_crawled

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

        for cabin_card in cabin_cards:

            cabin_class_element = cabin_card.find('h5', class_='cabin-class')
            cabin_price_element = cabin_card.find('span', class_='fit-child')

            cabin_class = cabin_class_element.text.strip() if cabin_class_element else ''
            cabin_price = cabin_price_element.text.strip() if cabin_price_element else ''

            flight_info[cabin_class] = cabin_price

        flights.append(flight_info)

    # Close the browser
    # browser.quit()

    return pd.DataFrame(flights)


booking_class = 'E'  # Booking class, e.g., 'Business', 'Economy', etc.
from_airport_code = 'ISB'  # Departure airport code, e.g., 'ISB' for Islamabad
to_airport_code = 'ORD'  # Destination airport code, e.g., 'ORD' for Chicago O'Hare
departing_date_year_month_day = '2023-06-20'  # Departure date in the format 'YYYY-MM-DD'
adults_count = '1'  # Number of adult passengers
child_count = '0'  # Number of child passengers
infant_count = '0'  # Number of infant passengers
currency = 'usd'  # Currency for prices, e.g., 'usd', 'eur', etc.
sell_language = 'en'  # Language for the booking process, e.g., 'en' for English


df = get_flight_data_qatar(booking_class, from_airport_code, to_airport_code, departing_date_year_month_day,
                           adults_count, child_count, infant_count, currency, sell_language)

# Plot the line graph
plt.plot(df['departure_time'], df['Economy'])
plt.plot(df['departure_time'], df['Business'])

plt.xlabel('Time')
plt.ylabel('Price')
plt.title('Flight Prices Over Time')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()
x = 1


