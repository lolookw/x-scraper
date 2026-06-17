from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import ast
import time
import json
from urllib.parse import quote
from funcs import load_config, login

def load_usernames(filename):
    """Load Twitter usernames from a file containing tuples."""
    usernames = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    data = ast.literal_eval(line)
                    if isinstance(data, (list, tuple)) and len(data) >= 2:
                        usernames.append(data[1])  # Extract the Twitter handle
                except (SyntaxError, ValueError):
                    print("⚠️ Invalid line format skipped.")
    return usernames

def open_user_pages(driver, usernames):
    """Open each username's Twitter page in a new tab, wait for it to close, then continue."""
    for username in usernames:
        driver.execute_script(f"window.open('https://x.com/{username}', '_blank');")
        new_tab = driver.window_handles[-1]  # Get the latest opened tab
        driver.switch_to.window(new_tab)
        
        print(f"✅ Opened: https://x.com/{username}")

        # Wait for the tab to be closed manually before proceeding
        while new_tab in driver.window_handles:
            time.sleep(1)

        # Switch back to the main window
        driver.switch_to.window(driver.window_handles[0])

if __name__ == "__main__":
    mail, username, password, *_ = load_config()  # Unpack only needed values
    driver = login(mail, username, password)

    if driver:
        try:
            usernames = load_usernames("ordered+filtered_users.txt")
            if usernames:
                print(f"📌 Loaded {len(usernames)} usernames.")
                open_user_pages(driver, usernames)
            else:
                print("⚠️ No valid usernames found.")
        finally:
            driver.quit()
