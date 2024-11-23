from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize the WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.redbus.in/")
time.sleep(1)

# Input Source and Destination
source_input = driver.find_element(By.XPATH, '//*[@id="src"]')  # From
source_input.send_keys("Karur")
source_input.send_keys(Keys.RETURN)
time.sleep(1)

destination_input = driver.find_element(By.XPATH, '//*[@id="dest"]')  # To
destination_input.send_keys("Trichy")
destination_input.send_keys(Keys.RETURN)
time.sleep(1)

# Select Date of Travel
date_input = driver.find_element(By.XPATH, "//div[@class='labelCalendarContainer']").click()
driver.find_element(By.XPATH, "//span[normalize-space()='23']").click()
driver.find_element(By.XPATH, '//*[@id="search_button"]').click()
time.sleep(5)

# Initialize Data List
bus_data = []

# Infinite Scrolling Implementation
scrolling = True
while scrolling:
    old_page_source = driver.page_source

    # Scroll the Page
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)

    new_page_source = driver.page_source

    if old_page_source == new_page_source:
        scrolling = False

# Extract Bus Data
bus_names = driver.find_elements(By.CSS_SELECTOR, "div[class='travels lh-24 f-bold d-color']")
bus_types = driver.find_elements(By.CSS_SELECTOR, "div[class='bus-type f-12 m-top-16 l-color evBus']")
departure_times = driver.find_elements(By.CSS_SELECTOR, "div[class='dp-time f-19 d-color f-bold']")
duration_times = driver.find_elements(By.CSS_SELECTOR, "div[class='dur l-color lh-24']")
star_ratings = driver.find_elements(By.CSS_SELECTOR, "div[class='rating-sec lh-24']")
prices = driver.find_elements(By.CSS_SELECTOR, "div[class='fare d-block']")
seat_availabilities = driver.find_elements(By.CSS_SELECTOR, "div[class='seat-left m-top-16']")

# Combine Data into List
for i in range(len(bus_names)):
    try:
        bus_data.append({
            "Bus Name": bus_names[i].text if i < len(bus_names) else "N/A",
            "Bus Type": bus_types[i].text if i < len(bus_types) else "N/A",
            "Departure Time": departure_times[i].text if i < len(departure_times) else "N/A",
            "Duration": duration_times[i].text if i < len(duration_times) else "N/A",
            "Star Rating": star_ratings[i].text if i < len(star_ratings) else "N/A",
            "Price": prices[i].text if i < len(prices) else "N/A",
            "Seat Availability": seat_availabilities[i].text if i < len(seat_availabilities) else "N/A",
        })
    except Exception as e:
        print(f"Error while appending data for bus {i}: {e}")

# Convert Data to DataFrame
bus_route_details = pd.DataFrame(bus_data)

# Display or Save the Data
print(bus_route_details)
bus_route_details.to_csv("bus_route_details.csv", index=False)

# Close Driver
driver.quit()
