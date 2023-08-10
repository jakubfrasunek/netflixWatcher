import imaplib
import email
import re
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

NETFLIX_LOGIN = os.environ['NETFLIX_LOGIN']
NETFLIX_PASSWORD = os.environ['NETFLIX_PASSWORD']
EMAIL_IMAP = os.environ['EMAIL_IMAP']
EMAIL_LOGIN = os.environ['EMAIL_LOGIN']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']


def extract_links(text):
    url_pattern = r'https?://\S+'
    urls = re.findall(url_pattern, text)
    return urls


def open_link_with_selenium(link):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Remote(
        command_executor='http://netflix_watcher_selenium:4444/wd/hub',
        options=options
    )

    driver.get(link)
    time.sleep(2)
    email_field = driver.find_element('name', 'userLoginId')
    email_field.send_keys(NETFLIX_LOGIN)
    password_field = driver.find_element('name', 'password')
    password_field.send_keys(NETFLIX_PASSWORD)

    password_field.send_keys(Keys.RETURN)
    time.sleep(2)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-uia="set-primary-location-action"]'))
        )

        element.click()
    except Exception as e:
        print("Error:", e)

    time.sleep(2)
    driver.quit()


def fetch_last_unseen_email():
    mail = imaplib.IMAP4_SSL(EMAIL_IMAP)
    mail.login(EMAIL_LOGIN, EMAIL_PASSWORD)
    mail.select("inbox")

    status, email_ids = mail.search(None, '(UNSEEN FROM "info@account.netflix.com")')
    email_ids = email_ids[0].split()

    if email_ids:
        email_id = email_ids[-1]
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if "text/plain" in content_type:
                    body = part.get_payload(decode=True).decode()
                    links = extract_links(body)
                    for link in links:
                        if "update-primary-location" in link:
                            open_link_with_selenium(link)
        else:
            body = msg.get_payload(decode=True).decode()
            links = extract_links(body)
            for link in links:
                if "update-primary-location" in link:
                    open_link_with_selenium(link)

    mail.logout()


if __name__ == "__main__":
    while True:
        fetch_last_unseen_email()
        time.sleep(20)
