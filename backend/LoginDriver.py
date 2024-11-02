import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginDriver:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv("UT_USERNAME")
        self.password = os.getenv("UT_PASSWORD")
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 60)

    def login(self):
        # Open the main page and navigate to login
        self.driver.get("https://registrar.utexas.edu/schedules/249")
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Find courses now"))).click()

        # Enter login details
        self.wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(self.username)
        self.wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(self.password)
        self.wait.until(EC.element_to_be_clickable((By.NAME, "_eventId_proceed"))).click()

        # Duo 2FA - Wait for Duo prompt and click "Yes, this is my device"
        print("Please complete Duo 2FA on your phone...")
        time.sleep(10)  # Adjust based on Duo timing

        try:
            # Check if "Yes, this is my device" button appears and click it
            trust_button = self.wait.until(EC.element_to_be_clickable((By.ID, "trust-browser-button")))
            trust_button.click()
            print("Clicked 'Yes, this is my device'")
        except:
            print("Trust this browser prompt did not appear.")

        # Confirm login success by checking the URL or page content
        self.wait.until(lambda driver: "registrar" in self.driver.current_url)
        print("Login successful.")
        
        # Capture cookies for session transfer
        cookies = self.driver.get_cookies()
        self.driver.quit()  # Close the Selenium session
        return cookies
