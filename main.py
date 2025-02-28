from funcs import get_users,send_messages, filter_users, load_config, login
from urllib.parse import quote

if __name__=="__main__":
    mail, username, password, mail2, username2, password2, busquedas = load_config()
    #print(busquedas)
    driver = get_users(busquedas, mail, username, password)
    #driver = login(mail, username, password)
    filter_users()
    #send_messages(driver)
    