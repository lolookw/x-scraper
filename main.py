from funcs import get_users,send_messages, filter_users, load_config, login
from urllib.parse import quote

if __name__=="__main__":
    mail, username, password, mail2, username2, password2, busquedas = load_config()
    driver = None
    try:
        driver = get_users(busquedas, mail, username, password)
        if driver is not None:
            filter_users()
        # send_messages(driver)  # Keep DM automation out of the default flow.
    finally:
        if driver is not None:
            driver.quit()
