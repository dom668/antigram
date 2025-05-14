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
        """Log into Instagram."""
        try:
            print("Navigating to Instagram...")
            self.driver.get("https://www.instagram.com/")
            
            # Wait for the page to load and accept cookies if prompted
            try:
                cookie_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Allow')]"))
                )
                cookie_button.click()
                print("Accepted cookies.")
            except TimeoutException:
                print("No cookie banner found or it already has been accepted.")
            
            # Find the username and password input fields
            print("Logging in...")
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
                print("Declined saving login info.")
            except TimeoutException:
                print("No 'Save Login Info' prompt found.")
            
            # Handle notifications popup if it appears
            try:
                notifications_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not now')]"))
                )
                notifications_button.click()
                print("Declined notifications.")
            except TimeoutException:
                print("No notifications prompt found.")
                
            print("Successfully logged in.")
            return True
            
        except Exception as e:
            print(f"Error during login: {e}")
            return False
    


    def handle_save_login_prompt(self):
        """Handle the 'Save your login info?' prompt and click 'Not now'."""
        try:
            # This looks specifically for the "Not now" button on the save login info page
            # We need to be more specific because there are multiple "Not Now" buttons on Instagram
            not_now_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Not now' or text()='Not Now']"))
            )
            not_now_button.click()
            print("Clicked 'Not now' on save login info prompt.")
        except TimeoutException:
            # Try alternative selector based on the screenshot
            try:
                not_now_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not now')]"))
                )
                not_now_button.click()
                print("Clicked 'Not now' on save login info prompt (alternative method).")
            except TimeoutException:
                print("No 'Save login info' prompt found or it was already handled.")






    
    def decline_instagram_save_password(self):
        try:
            print("gonna try read some stuff from the page")
            link = driver.find_element(By.LINK_TEXT, "Not now")
            print(f"Page Title is: {link}")
        except Exception as e:
            print(f"didnt work bro :  {e}")





    def search_and_visit_profile(self, account_name):
        """Search for a specific Instagram account and visit its profile."""
        try:
            print(f"Searching for account: {account_name}")
            
            # Click on search icon
            search_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(@aria-label, 'Search')]"))
            )
            search_button.click()
            
            # Wait for search input to appear
            search_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
            )
            
            # Enter account name in search bar
            search_input.clear()
            search_input.send_keys(account_name)
            time.sleep(2)  # Wait for search results to load
            
            # Click on the first result
            first_result = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{account_name}')]"))
            )
            first_result.click()
            
            print(f"Navigated to {account_name}'s profile.")
            return True
            
        except Exception as e:
            print(f"Error searching for account: {e}")
            return False
    
    def view_latest_posts(self, num_posts=5):
        """View the latest posts from the current profile."""
        try:
            print("Viewing latest posts...")
            
            # Wait for posts to load
            posts = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@role='button']/a"))
            )
            
            # Limit to the requested number of posts
            posts_to_view = min(num_posts, len(posts))
            
            for i in range(posts_to_view):
                try:
                    # Refresh the list of posts in case DOM has changed
                    posts = self.driver.find_elements(By.XPATH, "//div[@role='button']/a")
                    post = posts[i]
                    
                    # Scroll to the post
                    self.driver.execute_script("arguments[0].scrollIntoView();", post)
                    time.sleep(1)
                    
                    # Click the post
                    post.click()
                    print(f"Opened post {i+1}/{posts_to_view}")
                    
                    # Wait for post to load and view for a few seconds
                    time.sleep(3)
                    
                    # Close the post by clicking the escape key
                    webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error viewing post {i+1}: {e}")
                    # Try to close any modal if open
                    try:
                        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                    except:
                        pass
            
            print("Finished viewing posts.")
            return True
            
        except Exception as e:
            print(f"Error viewing posts: {e}")
            return False
    
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
            time.sleep(3)  # Wait a moment after login

            instagram_bot.handle_save_login_prompt()

            """"
            if instagram_bot.search_and_visit_profile(account_to_check):
                time.sleep(2)  # Wait for profile to load
                instagram_bot.view_latest_posts(num_posts)
            """
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Wait for a moment before closing
        time.sleep(5)
        instagram_bot.close()


if __name__ == "__main__":
    main()