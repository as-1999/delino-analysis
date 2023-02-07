from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
# selenium servise


from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
# Chrome servise

from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as firefoxeService
# Firefox servise


from bs4 import BeautifulSoup
from scraper import Scraper
class CrawlerTool(object):
    
    def __init__(self, browser:str,file_path:str) -> None:
        self._check_witch_browser(browser)
        self._url = r'https://www.delino.com/search?cityid='
        self.file_path = file_path
        self._make_url()
    def _check_witch_browser(self, browser:str):
        '''
        this method check witch browser you want to use
        '''
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


            case _:
                raise ValueError('your chosen browser is not found! valid options:(chrome, firefox)')

    def _make_url(self):
        '''
        this method get url of all citys in delino.com
        '''
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
        '''
        this method get urls of citys and find all items in each city
        '''
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
                pass
            while True:
                try:
                    self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                except :
                    continue
                while True:
                    try:
                        WebDriverWait(self.driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, more)))
                        break
                    except TimeoutException:
                        continue
                    except:
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
                except:
                    continue
            html = self.driver.page_source
            be = BeautifulSoup(html, 'html.parser')
            items = be.find_all('a', {'class':'r-i'})
            print(len(items))
            urls[url] = []
            for item in items:
                urls[url].append('https://www.delino.com'+item['href']) 

    
        for city in urls:
            self._get_data_from_page(urls[city], city)
            

    def _get_data_from_page(self, urls, city):
        '''
        this method get data from each page
        '''
        for url in urls:
            self.driver.get(url)
            try:
                page = '/html/body/div[2]/div[3]/div/div/div[1]/div[2]/div/aside/div[1]/h1'
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                                (
                                    By.XPATH, page
                                )
                        ))
            except TimeoutException:
                return False
            
            menu = '/html/body/div[2]/div[3]/div/div/div[2]/div/div[2]/div[2]/div[2]'
            count = 0
            while True:
                try:
                    find = '//section[@itemtype="http://schema.org/MenuItem"]'
                    
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                                (
                                    By.XPATH, find
                                )
                            ))
                    menu = self.driver.find_element(By.XPATH,menu)
                    menu = menu.get_attribute('innerHTML')
                    break
                except:
                    break
            
            

            while True:
                try:
                    comments = '/html/body/div[2]/div[3]/div/div/div[2]/div/div[1]/div[1]/ul/li[2]/a'
                    
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                                (
                                    By.XPATH, comments
                                )
                            )).click()
                    comments ='/html/body/div[2]/div[3]/div/div/div[2]/div/div[3]'
                    span='/html/body/div[2]/div[3]/div/div/div[2]/div/div[3]/div/div/div[2]/div[1]/ul/li[1]/span'
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                                (
                                    By.XPATH, span
                                )
                            ))
                    self.driver.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL + Keys.HOME)
                    comment = self.driver.find_element(By.XPATH,comments)
                    comment = comment.get_attribute('innerHTML')
                    
                    break
                except:
                    
                    continue

                
            
            count = 0            
            while True:
                try:
                    info = '/html/body/div[2]/div[3]/div/div/div[2]/div/div[1]/div[1]/ul/li[3]/a'
                    
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                                (
                                    By.XPATH, info
                                )
                            )).click()
                    info = '/html/body/div[2]/div[3]/div/div/div[2]/div/div[4]/div'
                    info = self.driver.find_element(By.XPATH,info)
                    info = info.get_attribute('innerHTML')
                    
                    

                    break
                except:
                    count += 1
                    if count == 6:
                        break
                    # if more than 5 times, it means that there is no info
                    continue
            
            html = BeautifulSoup(self.driver.page_source, 'html.parser')
            res = {'menu':BeautifulSoup(str(menu), 'html.parser'), 'comment':BeautifulSoup(str(comment), 'html.parser'), 'info':BeautifulSoup(str(info), 'html.parser')}
            Scraper(correntCity=city, pageContent = html, dic = res, url=url, file_path=self.file_path)

        

