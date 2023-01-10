import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# soup 생성
def create_soup(url, user_agent, verify = True, parser = "html.parser"):
    headers = {"User-Agent": user_agent}
    res = requests.get(url, headers = headers, verify = verify)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, parser)
    return soup

# selenium으로 페이지 로딩 후 soup 생성
def create_soup_selenium(url, user_agent, wait_for = None):
    try:
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument(f"user-agent = {user_agent}")

        browser = webdriver.Chrome("./chromedriver", options=options)
        browser.get(url)
        if wait_for == None:
            pass
        else:
            WebDriverWait(browser, 5).until(EC.presence_of_element_located(wait_for))

        soup = BeautifulSoup(browser.page_source, "html.parser")

    finally:
        browser.quit()
        
    return soup