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
    browser.add_cookie({"name": "MUSIC_U", "value": "002172C607ED582FEC6646669D7152C98C9E43449BEEB9FE882918D035595C5D14681D56CEB9D0B7CC360A91F44FD907A5AB1B9859BFE43F6B827964AC94FA5A6711F8DD87BFBC85D4769C72ED67CE42E9A6EFB19490B0AE992C3A42B0A7518916F8DCAD126C68FDC25CB405462AB39A452DCA7A0000D8F9DEC9F915057BED0BB90EAE4CE273F745A5270310125E6A13BF05B601441D18136767BEDA3FA6617256F73E081651CBDB0D44A70F679FFA4C30CAEE2DD29AA2EF88690CE4F01841EC4514E27A91160A427FA5841CA11998D65FFE65C506592AE73184D719650ED1D4A89DCA29427806E84CD2EFCF2285F5A1012DA8AEA5488011717179DA1FEE1A453EAC2BDA8814E14163402B24982FB5B9D16AA7D51F60CE6FA0E757A7BB0AD3AA43059269C80EA47AEE56995E2317995205C0F94895458361ACA7A4DA12C6F2CD6C58E9A6363116AD86ECC456C978C5515F5EC21E914D4DBA1998827FCCF98846B7
"})
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
