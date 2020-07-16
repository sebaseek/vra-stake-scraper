import time
import smtplib
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

from EmailData import EmailData

load_dotenv()
first_run = None

VERA_WALLET_STAKING_URL = 'https://verawallet.tv/stake-vra'


def main():
    global first_run
    vra_default_value = 0
    browser = webdriver.Chrome('./chromedriver')
    browser.get(VERA_WALLET_STAKING_URL)
    timeout = 5
    while True:
        try:
            # Refresh web if it's not the first run
            if first_run is not None:
                print('Sleep 15 seconds until browser refresh')
                time.sleep(15)
                browser.refresh()
            print('Reading VRA Wallet Stake status')
            email_data = EmailData()
            # get staking block element
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'staking-block'))
            WebDriverWait(browser, timeout).until(element_present)
            # get VRA text
            vra_element = browser.find_elements(By.CSS_SELECTOR, '.staking-block .staking-block-value')[2].text
            # Parse VRA from string to int
            vra_number = int(vra_element.replace(' VRA', ''))
            print(f'VRA actual staking status {vra_number}')
            if first_run is None:
                print(f'First run')
                first_run = False
                vra_default_value = vra_number
                print(f'VRA default value is {vra_default_value}')
            # is available for stake ( greater than 0 or different to previous value )
            available_for_stake = (vra_number > 0 and vra_number != vra_default_value)
            print('VRA Staking is available:' 'Yes' if available_for_stake else 'No')
            if available_for_stake:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(email_data.gmail_user, email_data.gmail_password)
                email_data.set_mail_body(vra_default_value, vra_number)
                email_data.set_mail_text(email_data.body)
                server.sendmail(email_data.gmail_user, email_data.to, email_data.text)
                server.close()
                print('Email Sent Correctly!')
        except Exception as e:
            logging.exception(e)
        except TimeoutException:
            print("Timed out waiting for page to load")


main()
