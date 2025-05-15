import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome()

class InstagramAutomation:
    def __init__(self, username, password):
        """Initialize the Instagram automation with user credentials."""
        self.username = username
        self.password = password

        
        # Set up the Chrome driver with options
        self.options = webdriver.ChromeOptions()
        # Uncomment the line below if you want the browser to run in headless mode (no UI)
        # self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def login(self):
        try:
            print("Navigating to Instagram...")
            self.driver.get("https://www.instagram.com/")
            
            # Wait for the page to load and accept cookies if prompted
            try:
                cookie_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Allow')]"))
                )
                cookie_button.click()
                #print("Accepted cookies.")
            except TimeoutException:
                #print("No cookie banner found or it already has been accepted.")
                pass
            
            # Find the username and password input fields
            # print("Logging in...")
            username_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            
            # Input credentials
            username_input.send_keys(self.username)
            password_input.send_keys(self.password)
            
            # Click the login button
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            login_button.click()

            time.sleep(2)
            
            # Handle "Save Login Info" popup if it appears
            try:
                not_now_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not now')]"))
                )
                not_now_button.click()
                #print("Declined saving login info.")
            except TimeoutException:
                #print("No 'Save Login Info' prompt found.")
                pass

            # Handle notifications popup if it appears
            try:
                notifications_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not now')]"))
                )
                notifications_button.click()
                #print("Declined notifications.")
            except TimeoutException:
                #print("No notifications prompt found.")
                pass
                
            #print("Successfully logged in.")
            return True
            
        except Exception as e:
            print(f"Error during login: {e}")
            return False


    def dont_save_login(self):
        try:
            not_now_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Not now' or text()='Not Now']"))
            )
            not_now_button.click()
            print("Clicked 'Not now' on save login info prompt.")
        except TimeoutException as e:
            print("error : {e}")
    
    
    def close(self):
        """Close the browser."""
        print("Closing browser...")
        self.driver.quit()


def main():
    # Replace with your Instagram credentials
    username = "sheffskatesoc"
    password = "j£h38qH/65f"
    
    # Replace with the account you want to check
    account_to_check = "sluggerskatestore"
    
    # Number of posts to view
    num_posts = 3
    
    # Initialize the automation
    instagram_bot = InstagramAutomation(username, password)
    
    try:
        # Perform the actions
        if instagram_bot.login():
            time.sleep(1)  # Wait a moment after login

            instagram_bot.dont_save_login()
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Wait for a moment before closing
        time.sleep(5)
        instagram_bot.close()


if __name__ == "__main__":
    main()