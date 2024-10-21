from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from xvfbwrapper import Xvfb
import time

class YandexMapParser:
    def __init__(self):
        self.vdisplay = Xvfb()
        self.vdisplay.start()  # Запуск Xvfb
        self.start_browser()

    def start_browser(self):
        o = Options()
        o.add_experimental_option("detach", True)
        o.add_argument("--no-sandbox")
        o.add_argument("--disable-setuid-sandbox")
        o.add_argument(f'--user_agent={UserAgent().random}')
        o.add_argument('--headless')  # Графический интерфейс отключен
        self.driver = webdriver.Chrome(options=o)
        self.driver.get('https://yandex.ru/maps/')

    def clear_cookies(self):
        self.driver.delete_all_cookies()

    def restart_browser(self):
        self.driver.quit()
        self.start_browser()

    def get_location_from_Yandex(self, address):
        search_input_not_found = False
        try:
            search_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="Поиск мест и адресов"]'))
            )
        except Exception as e:
            search_input_not_found = True
            location_dict = {'latitude': None, 'longitude': None, 'Yandex_address': None,
                             'Input_not_found': search_input_not_found}
            return location_dict

        try:
            search_input.send_keys(Keys.CONTROL + 'a')
            search_input.send_keys(Keys.BACKSPACE)
            search_input.send_keys(address)
            search_input.send_keys(Keys.RETURN)

            time.sleep(1)

            page = self.driver.page_source
            soup = BeautifulSoup(page, 'html.parser')

            coords_element = soup.find('div', class_='toponym-card-title-view__coords-badge')
            Yandex_address = soup.find('div', class_="card-title-view__wrapper").text

            if Yandex_address is None:
                return None

            if coords_element is not None:
                latitude, longitude = coords_element.text.split(', ')
                location_dict = {'latitude': latitude, 'longitude': longitude, 'Yandex_address': Yandex_address,
                                 'Input_not_found': search_input_not_found}
            else:
                raise ValueError("Coordinates element not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.clear_cookies()
            self.restart_browser()
            location_dict = None

        return location_dict

    def stop_browser(self):
        self.driver.quit()
        self.vdisplay.stop()  # Остановка Xvfb
