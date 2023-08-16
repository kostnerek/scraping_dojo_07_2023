from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import re
from dotenv import dotenv_values

from utils import save_to_json, validate_envs
from consts import *

def extract_data_from_quote(quote):
    quote_text = quote.find_element(By.CLASS_NAME, QUOTE_CONTAINER_CLASS).text
    author = quote.find_element(By.CLASS_NAME, AUTHOR_CONTAINER_CLASS).text
    tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, TAG_CONTAINER_CLASS)]
    return {
        "text": re.sub(r"[^\x00-\x7F]+", "", quote_text), # delete non-ascii characters
        "by": author,
        "tags": tags
    }

def scrape_data(driver, url, filename):
    driver.get(url)
    elements = WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))
    )
    quotes = []
    for element in elements:
        quotes.append(extract_data_from_quote(element))
    save_to_json(quotes, filename)

    try:
        next_page_button = driver.find_element(By.CLASS_NAME, NEXT_PAGE_BUTTON_CLASS) # messy, but selenium doesnt fallbacks with None, but rather raises an exception
    except:
        return
    if next_page_button:
        next_page_button.find_element(By.TAG_NAME, "a").click()
        scrape_data(driver, driver.current_url, filename)


if __name__ == "__main__":
    config = dotenv_values(".env")
    validate_envs(config)
    options = webdriver.ChromeOptions()
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    scrape_data(driver, config['INPUT_URL'], config['OUTPUT_FILE'])
    driver.quit()