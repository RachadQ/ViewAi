from flask import Flask
from flask import Flask, render_template
from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException

import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



app = Flask(__name__)


# Load environment variables from .env file
load_dotenv()


# Access environment variables
spotify_username = os.getenv('user')
spotify_password = os.getenv('password')
@app.route('/')
def run_selenium():
    # Set up Chrome options
    #chrome_options = webdriver.ChromeOptions()

    # Choose a random User-Agent string
   # chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

    # Set the window size
   # chrome_options.add_argument("--window-size=1920,1080")
     # Create a new instance of the browser driver (Chrome in this example)
    driver = webdriver.Chrome()

   
    try:
        
        # Navigate to the Spotify URL
        driver.get('https://open.spotify.com/artist/3IF61yXqfjrZFaDiGEDr17?flow_ctx=cde520ee-4ea0-4bc8-8d2e-fcef96258760%3A1710463388#login')

        # Wait for the page to load completely
        WebDriverWait(driver, 10).until(EC.title_contains('Spotify'))

          # Click on the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="login-button"]'))
        )
        login_button.click()

      # Wait for the username input field to be visible and enabled
        username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'login-username'))
        )
        # Input the username
        username_input.send_keys(spotify_username)

    # Wait for the password input field to be visible and enabled
        password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'login-password'))
        )
        # Input the username
        password_input.send_keys(spotify_password)
       
        
       # Wait for the login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.ButtonInner-sc-14ud5tc-0.cJdEzG.encore-bright-accent-set'))
        )

        # Click the login button
        login_button.click()
        

        try:
            # Wait for the button to be clickable
            play_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.ButtonInner-sc-14ud5tc-0.fGgTkO.encore-bright-accent-set'))
            )

            # Click the button
            play_button.click()

        except TimeoutException as e:
            print("Timeout occurred while waiting for the play button:", e)

        except Exception as e:
            print("An error occurred:", e)

        # Click the button
        print('work')
       # Wait for 2 minutes
        time.sleep(120)
        return driver
    except Exception as e:
        print('Error:', e)
'''   finally:
        # Close the browser
        driver.quit()
'''
@app.route('/')
def Playspotify():
    # Run the Selenium WebDriver code
    driver = run_selenium()

    if driver:
        # Return a response to the client
        message = 'Selenium actions completed successfully.'
    else:
        message = 'An error occurred.'

    # Return a response to the client
    return render_template('index.html', message=message)
if __name__ == '__main__':
    app.run(debug=True)