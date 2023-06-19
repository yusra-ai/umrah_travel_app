import requests
from bs4 import BeautifulSoup
import logging



# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FlightSearch")

url = "https://www.qatarairways.com/app/booking/flight-selection"
params = {
    "upsellCallId": "123",
    "bookingClass": "B",
    "tripType": "O",
    "selLang": "en",
    "fromStation": "ISB",
    "from": "Islamabad",
    "toStation": "ORD",
    "to": "Chicago",
    "departing": "2023-07-20",
    "adults": "1",
    "children": "0",
    "infants": "0",
    "teenager": "0",
    "ofw": "0",
    "promoCode": "",
    "flexibleDate": "off",
    "cid": "SXIN23456993M"
}



headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:

    logger.info("Request successful!")
    page_content = response.content
    soup = BeautifulSoup(page_content, "html.parser")

    # Find all flight containers
    flight_containers = soup.find_all("booking-flight-card")
    print("Wait")
    #
    # # Iterate over each flight container
    # for container in flight_containers:
    #     # Extract flight details from the container
    #     flight_number = container.find("div", class_="flight-selection-flight-number").text.strip()
    #     departure_time = container.find("div", class_="flight-selection-time-departure").text.strip()
    #     arrival_time = container.find("div", class_="flight-selection-time-arrival").text.strip()
    #     price = container.find("span", class_="flight-selection-total-amount").text.strip()
    #
    #     # Print the flight details
    #     print(f"Flight: {flight_number}")
    #     print(f"Departure Time: {departure_time}")
    #     print(f"Arrival Time: {arrival_time}")
    #     print(f"Price: {price}")
    #     print("----------------------")

else:
    logger.error(f"Request failed with status code: {response.status_code}")
