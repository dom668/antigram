import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class InstagramAutomation:
    def __init__(self, username, password):
        """Initialize the Instagram automation with user credentials."""
        self.username = username
        self.password = password

        self.base_url = "https://www.instagram.com/"

        
        # Set up the Chrome driver with options
        self.options = webdriver.ChromeOptions()
        # Uncomment the line below if you want the browser to run in headless mode (no UI)
        # self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def login(self):
        
        self.driver.maximize_window() # in fullscreen mode the buttons have text as well

        try:
            print("Navigating to Instagram...")
            self.driver.get(self.base_url)
            
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

            time.sleep(1)
            
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

    def open_inbox(self):
        try:
            url = self.driver.current_url
            inbox_url = f"{url}/direct/inbox"
            self.driver.get(inbox_url)
            #print("got url")
        except:
            print("dint work bro")

    def go_to_account(self, account):
        try:
            url = self.driver.current_url
            account_url = f"{url}{account}"
            self.driver.get(account_url)
            time.sleep(2)
        except:
            print("didnt work bro")

    def message_viewed_account(self):
        try:
            message_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Message' or text()='Message']"))
            )
            message_button.click()
            time.sleep(3)
            self.driver.refresh()
            time.sleep(2)
            print("clicked on message")
        except TimeoutException as e:
            print(f"dint work bro {e}")

    def send_message(self, meassage="hello"):
        try:
            
            actions = ActionChains(self.driver)
            actions.send_keys(meassage)  # Send keys to the active element (usually the body)
            actions.perform()
            print("sent keys")
            actions.send_keys(Keys.ENTER) # Send Tab key
            actions.perform()
            print("sent enter")
        except:
            print("dint work bro")


    def send_100_message(self, message="hello"):
        actions = ActionChains(self.driver)
        try:
            x = 0
            while (x < 100):
                print("in the while")
                actions.send_keys(message)  # Send keys to the active element (usually the body)
                actions.perform()
                actions.send_keys(Keys.ENTER) # Send Tab key
                actions.perform()
                x = x + 1
                time.sleep(0.5)
        except:
            print("dint work")

    def click_middle_of_screen(self):
        print("trying to click middle")
        actions = ActionChains(self.driver)
        try:
            window_width = self.driver.execute_script("return window.innerWidth")
            window_height = self.driver.execute_script("return window.innerHeight")

            center_x = window_width // 2
            center_y = window_height // 2

            actions = ActionChains(self.driver)
            actions.move_by_offset(center_x, center_y).perform()

            actions.click().perform()
            
        except:
            print("brok it")

    def click_most_recent_post(self):
        print("trying to click middle")
        actions = ActionChains(self.driver)
        try:
            window_width = self.driver.execute_script("return window.innerWidth")
            window_height = self.driver.execute_script("return window.innerHeight")

            center_x = window_width // 2
            center_y = window_height // 2

            print(center_x)
            print(center_y)

            actions = ActionChains(self.driver)
            actions.move_by_offset(center_x, center_y-250).perform()

            actions.click().perform()
            
        except:
            print("brok it")


    # try search for kier and send him a myself, use a combination of url, like https://www.instagram.com/kier.struthers/
    # then use the button "meassage"        
    
    
    def close(self):
        print("Closing browser...")
        self.driver.quit()


def main():


    # Replace with your Instagram credentials
    username = "back180stylin"
    password = "hardskat3SC3n3"
    
    # Initialize the automation
    instagram_bot = InstagramAutomation(username, password)
    
    try:
        
        # Perform the actions
        if instagram_bot.login():
            time.sleep(1)  # Wait a moment after login
            instagram_bot.dont_save_login()
            instagram_bot.go_to_account("freeskatemag")
            time.sleep(1)
            instagram_bot.click_most_recent_post()

        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Wait for a moment before closing
        time.sleep(50)
        instagram_bot.close()


if __name__ == "__main__":
    main()