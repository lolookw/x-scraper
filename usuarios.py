from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from urllib.parse import quote
from funcs import load_config, login

def load_usernames(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip()]

def open_user_pages(driver, usernames):
    for username in usernames:
        driver.execute_script(f"window.open('https://x.com/{username}', '_blank');")
        new_tab = driver.window_handles[-1]  # Get the latest opened tab
        driver.switch_to.window(new_tab)
        
        # Wait for the tab to be closed
        while new_tab in driver.window_handles:
            time.sleep(1)
        
        # Once tab is closed, switch back to the main window
        driver.switch_to.window(driver.window_handles[0])

if __name__ == "__main__":
    mail, username, password, _ = load_config()
    driver = login(mail, username, password)
    if driver:
        usernames = load_usernames("drop.txt")
        print(usernames)
        open_user_pages(driver, usernames)
        driver.quit()
