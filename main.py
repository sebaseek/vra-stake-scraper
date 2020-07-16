import os
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()
gmail_user = os.environ.get('gmail_user')
gmail_password = os.environ.get('gmail_password')
sent_from = gmail_user
to = ['sebastiangseijo@gmail.com']
subject = 'VRA STAKING UPDATE'
body = f'VRA has change from '

browser = webdriver.Chrome('./chromedriver')
browser.get('https://verawallet.tv/stake-vra')
timeout = 5
try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'staking-block'))
    WebDriverWait(browser, timeout).until(element_present)
    vra_element = browser.find_elements(By.CSS_SELECTOR, '.staking-block .staking-block-value')[2].text
    vra_number = vra_element.replace(' VRA', '')
    available_for_stake = (int(vra_number) > 50000)
    print(available_for_stake)
    if available_for_stake:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)


except TimeoutException:
    print("Timed out waiting for page to load")
except:
    print('an error has occurred.')

browser.quit()
