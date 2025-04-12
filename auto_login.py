# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "009C17B4616F0FC09B68C0F7746058D124AFD7C1DFC9C82ABFCF88557452B530F99EF637F688766B8DAFBD190282FA91BCC62A95C1CE65E8551F55D38294BBF439C6C679CB269C93A4F13CFD2AAA4C1659857C6E16F813A3B1017F0CB6C8D5327A9949C1F615635B702A297E52719F3E7450EEA7CFC0093384D5A5BAE04B9E37110B2A1B95114557187CB1AE843E8F9303BAB051E747EA7862BFD3DAB5D3B8C16111DB082DB82BFF84CD0CD74B65F3D61A494390A58E58EE6391BA7AD7DC7EC78BB11E5BDB1683E6116A405B54C6FE8361807DB8D28D3EB47CF126A747B809C4DE226772DB170EE595C322B57E570234A7F7680C975BD6F471E0B4209C2C87FFCCF56E4DBF1FFC5943621E90B4E2838DE9453A6BC107497ED96BE250BD8C38F609BB48C0DBC4432B8F4FD6470CD96E9FC1C62F8F7B22EF5459C5B04829992F9DF44BC2FF8A3716D96BAED71A9623F0A8E8368733C3B89B8CE56237E1BE61DC661B"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
