import pickle
import time
from typing import Optional

from selenium.webdriver.common.by import By
import undetected_chromedriver.v2 as uc

from src.config import AUTH_URL, PASSWORD, LOGIN
from src.writer import Writer


class Parser:
    def __init__(self, tech_stack: list = tuple(), headless=True):
        self.tech_stack = tech_stack
        self.writer = Writer()  # todo add first row and filename
        self._setup_driver(headless=headless)

    def get(self, url: str) -> None:
        self.driver.get(url)

    def auth(self, login: str, password: str) -> None:
        self.driver.get(AUTH_URL)
        time.sleep(20)
        self.driver.find_element(By.NAME, 'email').send_keys(login)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.CLASS_NAME, 'login').click()
        cookies = self.driver.get_cookies()
        pickle.dump(cookies, open("cookies.pkl", "wb"))

    def parse(self, href: str) -> None:
        pass

    def _parse_company(self, href) -> Optional[dict, None]:
        pass

    def _get_companies_hrefs(self, href: str) -> list[str]:
        self.driver.get(href)
        time.sleep(5)
        body_wrapper = self.driver.find_element(By.CLASS_NAME, 'body-wrapper')
        companies = body_wrapper.find_elements(By.TAG_NAME, 'grid-row')
        urls = []
        for company in companies:
            urls.append(company.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        return urls

    def _get_href_next_page(self, href: str) -> Optional[str, None]:
        self.driver.get(href)
        pass

    def _setup_driver(self, headless=True) -> None:
        options = uc.ChromeOptions()
        options.headless = headless
        # just some options passing in to skip annoying popups
        options.add_argument("--no-first-run")
        options.add_argument("--no-service-autorun")
        options.add_argument("--password-store=basic")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-notifications")
        options.add_argument("--content-shell-hide-toolbar")
        options.add_argument("--top-controls-hide-threshold")
        options.add_argument("--force-app-mode")
        options.add_argument("--hide-scrollbars")
        self.driver = uc.Chrome(options=options)
        try:
            self.driver.get('https://www.crunchbase.com/')
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        except FileNotFoundError:
            self.auth(LOGIN, PASSWORD)


if __name__ == "__main__":
    first_href = 'https://www.crunchbase.com/discover/organization.companies'
    p = Parser(headless=False)
    # p.auth(LOGIN, PASSWORD)
    companies = p.get_companies()

    for company in companies:
        print(company)