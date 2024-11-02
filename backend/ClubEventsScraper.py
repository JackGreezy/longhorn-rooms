import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class ClubEventsScraper:
    def __init__(self):
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("https://utexas.campuslabs.com/engage/events")
        self.wait = WebDriverWait(self.driver, 10)
    
    def load_all_events(self):
        while True:
            try:
                # Wait for the 'Load More' button to appear, then click it
                load_more_button = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//button//span[contains(text(), 'Load More')]"))
                )
                ActionChains(self.driver).move_to_element(load_more_button).perform()
                load_more_button.click()
                time.sleep(2)  # Wait a bit to let new content load
            except Exception as e:
                print("No more 'Load More' button found. Finished loading all events.")
                break
    
    def scrape_events(self):
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        events = []

        # Find all event cards by specific style attribute
        event_divs = soup.find_all("div", style=lambda value: value and "box-sizing: border-box; padding: 10px; width: 50%; height: auto;" in value)

        for event_div in event_divs:
            event = {}

            # Extract the event title
            title_tag = event_div.find("h3")
            event["title"] = title_tag.text.strip() if title_tag else "No Title Found"

            # Extract date/time and room info
            date_location_div = event_div.find("div", style=lambda value: value and "margin-right: 8px; padding: 0.5rem 0px 1rem 1rem; overflow: visible; color: rgb(68, 68, 68); font-size: 0.938rem;" in value)
            if date_location_div:
                date_time_div = date_location_div.find_all("div")[0]
                event["date_time"] = date_time_div.text.strip() if date_time_div else "No Date/Time Found"
                
                location_div = date_location_div.find_all("div")[1]
                event["room"] = location_div.text.strip() if location_div else "No Location Found"
            else:
                event["date_time"] = "No Date/Time Found"
                event["room"] = "No Location Found"

            # Extract organization name
            org_tag = event_div.find("span", style=lambda value: value and "width: 91%; display: inline-block;" in value)
            event["organization"] = org_tag.text.strip() if org_tag else "No Organization Found"

            # Extract event image URL from background-image style in the div with role="img"
            event_img_tag = event_div.find("div", role="img")
            if event_img_tag and "background-image" in event_img_tag["style"]:
                style = event_img_tag["style"]
                img_url_start = style.find("url(") + 4
                img_url_end = style.find(")", img_url_start)
                event["event_image"] = style[img_url_start:img_url_end]
            else:
                event["event_image"] = "No Event Image Found"

            # Extract organization image
            org_img_tag = event_div.find("img", alt=True)
            event["organization_image"] = org_img_tag["src"] if org_img_tag else "No Org Image Found"

            # Append the event to the list
            events.append(event)

        return events

    def save_events(self, events):
        # Save extracted data to a JSON file
        with open("ut_club_events.json", "w", encoding="utf-8") as f:
            json.dump(events, f, indent=4)
        print("Events data saved to ut_club_events.json")
    
    def run(self):
        try:
            # Load all events by clicking "Load More" repeatedly
            self.load_all_events()
            # Scrape event data
            events = self.scrape_events()
            # Save data to JSON
            self.save_events(events)
        finally:
            # Quit the WebDriver
            self.driver.quit()

if __name__ == "__main__":
    scraper = ClubEventsScraper()
    scraper.run()
