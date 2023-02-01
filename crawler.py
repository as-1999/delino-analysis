from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
# selenium servise


from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
# Chrome servise

from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as firefoxeService
# Firefox servise

from webdriver_manager.microsoft  import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
# Edge servise

from bs4 import BeautifulSoup
import time
class CrawlerTool(object):
    
    def __init__(self, browser:str,file_path:str) -> None:
        self._check_witch_browser(browser)
        self._url = r'https://www.delino.com/search?cityid='
        self.file_path = file_path
        self._make_url()
    def _check_witch_browser(self, browser:str):
        match browser:
            case 'chrome':
                service = ChromeService(executable_path=ChromeDriverManager().install())
                # op = webdriver.ChromeOptions()
                # op.add_argument('headless')
                # self.driver = webdriver.Chrome(service=service, options=op)
                caps = DesiredCapabilities().CHROME
                caps['pageLoadStrategy'] = 'normal'
                self.driver = webdriver.Chrome(service=service, desired_capabilities=caps)
            case 'firefox':
                service = firefoxeService(executable_path=GeckoDriverManager().install())
                # op = webdriver.FirefoxOptions()
                # op.add_argument('headless')
                # self.driver = webdriver.Firefox(service=service, options=op)
                self.driver = webdriver.Firefox(service=service)
                # print(self.driver.capabilities)
            case 'edge':
                service = EdgeService(executable_path=EdgeChromiumDriverManager().install())
                # op = webdriver.EdgeOptions()
                # op.add_argument('headless')
                # self.driver = webdriver.Edge(service=service, options=op)
                self.driver = webdriver.Edge(service=service)
            case _:
                raise ValueError('your chosen browser is not found! valid options:(chrome, firefox, edge)')

    def _make_url(self):
        self.driver.get(self._url)
        delay = 3
        link_of_citys = '/html/body/div[2]/div[3]/div/div[1]/div/div/span/strong'
        while True:
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_all_elements_located((
                        By.XPATH, link_of_citys
                    ))
                )
                break
            except TimeoutException:
                delay += 1
                continue
        links = self.driver.find_element(By.XPATH, link_of_citys)
        links.click()
        html =  self.driver.page_source
        be = BeautifulSoup(html, 'html.parser')
        ul = be.find('ul', {'class':'list'})
        url = {}
        for li in ul.find_all('li'):
            url[li.text] =self._url + li['data-value']
        
        self.find(url)


    def find(self, urls):
        
        for url in urls:
            self.driver.get(urls[url])
            more = '/html/body/div[2]/div[3]/div/div[3]/div/div[4]/button/span'
            more_btn = '/html/body/div[2]/div[3]/div/div[3]/div/div[4]/button'
            delay = 3
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[2]/div[3]/div/div[3]/div/header/small')))
            how_much = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[3]/div/header/small').text
            try:
                how_much = int(how_much.replace(' مورد', ''))
            except:
                print(how_much)
            while True:
                self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                while True:
                    try:
                        WebDriverWait(self.driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, more)))
                        break
                    except TimeoutException:
                        continue
                try:
                    if len(self.driver.find_elements(By.XPATH, '/html/body/div[2]/div[3]/div/div[3]/div/div[3]/a')) == how_much:
                        break
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                        (
                            By.XPATH, more_btn
                        )
                    )).click()
                except TimeoutException:
                    break
                except ElementClickInterceptedException:
                    continue
            html = self.driver.page_source
            be = BeautifulSoup(html, 'html.parser')
            items = be.find_all('a', {'class':'r-i'})
            print(len(items))
            urls[url] = items

        with open(self.file_path+r'\res.txt', 'w', encoding='utf-8') as f:
            for page in urls:
                f.write(str(urls[page]) + '\n')

