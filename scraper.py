from typing import Generator
from bs4 import element
from uuid import uuid1
import json

class Scraper:
    def __init__(self, correntCity, pageContent, dic, url, file_path) -> None:
        '''
        :param correntCity: the city that the restaurant is in
        :param pageContent: the page content of the restaurant
        :param dic: a dictionary that contains the menu, comment and info of the restaurant
        :param url: the url of the restaurant
        :param file_path: the path of the file that the data will be saved in
        '''
        self.progress = None
        self.scrapeTask = None
        self.url = url
        self.correntCity = correntCity
        self.file_path = file_path
        with open(self.file_path, 'a') as file:
            json.dump(self._detaile_extractor(pageContent, dic), file)
            


        
    def _detaile_extractor(self, pageContent, dic) -> dict:
        '''
        :param pageContent: the page content of the restaurant
        :param dic: a dictionary that contains the menu, comment and info of the restaurant
        :return: a dictionary that contains the data of the restaurant
        '''
        data = {
            'id': str(uuid1().hex),
            'city': self.correntCity,
            'link': self.url
        }
        try:
            
            # restaurant introduction (cover) section
            rightSide = pageContent.find('div', {"class", "right-side"})
            leftSide = pageContent.find('div', {"class", "left-side"})
            data['title'] = self._title_ex(rightSide)
            data['rate'] = self._rate_ex(rightSide)
            data['total_reviews'] = self._total_review_ex(rightSide)
            data['delivery_time'] = self._delivery_time_ex(leftSide.find('div', {"class", "mini-info"}))
            data['district'] = self._district_ex(rightSide)
            # restaurant menu section
            data['menu'] = self._menu_ex(dic['menu'].find('div', {"class", "food-menu clearfix"}), self.__food_item_ex)
            # restaurant reviews section
            data['overall_summary'] = self._overall_summary_ex(dic['comment'].find('ul', {"class", "overall-summary"}))
            # restaurant info section
            infos = dic['info'].find('div', {"class", "wrapper"}).find_all('section')
            data['address'] = self._address_ex(infos[0])
            data['coordinates'] = self._coordinates_ex(infos[0])
            data['types'] = self._type_ex(infos[1])
            data['service_hours_table'] = self._service_hours_table_ex(infos[2])
            return data
        except Exception as error:
            
            return data

    @staticmethod
    def _title_ex(content: element.Tag) -> str|None:
        '''
        :param content: the page content of the restaurant
        :return: the title of the restaurant
        '''
        try:
            return content.find('h1', {"class", "rest-title"}).text.strip()
        except Exception as error:
            return None 

    @staticmethod
    def _rate_ex(content: element.Tag) -> float|None:
        '''
        :param content: the page content of the restaurant
        :return: the rate of the restaurant
        '''
        try:
            return float(content.find('b').text.strip())
        except Exception as error:
            return None 

    @staticmethod
    def _total_review_ex(content: element.Tag) -> int|None:
        '''
        :param content: the page content of the restaurant
        :return: the total number of reviews of the restaurant
        '''
        try:
            return int(content.find('span').text.strip())
        except Exception as error:
            return None
    
    @staticmethod
    def _delivery_time_ex(content: element.Tag) -> str|None:
        '''
        :param content: the page content of the restaurant
        :return: the delivery time of the restaurant
        '''
        try:
            text = content.find('b').text.strip()
            return text.replace(' تا ', ' _ ').replace(' دقیقه', '')
        except Exception as error:
            return None

    @staticmethod
    def _district_ex(content: element.Tag) -> str|None:
        '''
        :param content: the page content of the restaurant
        :return: the district of the restaurant
        '''
        try:
            return content.find('div', {"class", "short-address"}).text.strip()
        except Exception as error:
            return None

    @staticmethod
    def _menu_ex(content: element.Tag, food_item_ex) -> dict|None:
        '''
        :param content: the page content of the restaurant
        :param food_item_ex: a function that extracts the food item
        :return: the menu of the restaurant
        '''
        try:
            menu = {}
            sections = content.find_all('section', {"class", "food-list"})
            for section in sections:
                sectionName = section.find('h2').find('b').text.strip()
                menu[sectionName] = []
                for item in section.find_all('div', {"class", "food-item"}):
                    menu[sectionName].append(food_item_ex(item))
            return menu
        except Exception as error:
            return None
    
    @staticmethod
    def __food_item_ex(content: element.Tag) -> dict:
        '''
        :param content: the page content of the restaurant
        :return: the food item of the restaurant
        '''
        food = None
        try:
            food = {}
            item = content.find('div', {"class", "details-holder"})
            food['name'] = item.find('h3').text.strip()
            food['ingredient'] = item.find('div', {"class", "ingredient"})['title'].strip()
            food['price'] = item.find('small').text.replace('تومان', '').strip()
            food['meal_badge'] = item.find('label', {"class", "meal-badge"})['title'].strip()
            return food
        except Exception as error:
            return food

    @staticmethod
    def _overall_summary_ex(content: element.Tag) -> dict:
        '''
        :param content: the page content of the restaurant
        :return: the overall summary of the restaurant
        '''
        dictedReview = None
        try:
            category = ['good', 'neutral', 'bad']
            reviews = content.find_all('li')
            dictedReview = {}
            for i in range(0, len(reviews)):
                dictedReview[category[i]] = int(reviews[i].find('span').text.replace(' نظر', '').strip())
            return dictedReview
        except Exception as error:
            return dictedReview
        
    @staticmethod
    def _address_ex(content: element.Tag) -> str|None:
        '''
        :param content: the page content of the restaurant
        :return: the address of the restaurant
        '''
        try:
            return content.find('span').text.strip()
        except Exception as error:
            return None
    
    @staticmethod
    def _coordinates_ex(content: element.Tag) -> list|None:
        '''
        :param content: the page content of the restaurant
        :return: the coordinates of the restaurant
        '''
        try:
            coordinates = content.find('div', {"class", "map-holder"}).find('div')['style'].split('|')[1]
            coordinates = coordinates[:len(coordinates)-2].split(',')
            return [float(coordinate) for coordinate in coordinates]
        except Exception as error:
            return None
    
    @staticmethod
    def _type_ex(content: element.Tag) -> list|None:
        '''
        :param content: the page content of the restaurant
        :return: the type of the restaurant
        '''
        try:
            restTypes = content.find('ul').find_all('li')[-1].find_all('a')
            for i in range(0, len(restTypes)):
                restTypes[i] = restTypes[i].text.strip()
            return restTypes
        except Exception as error:
            return None
    
    @staticmethod
    def _service_hours_table_ex(content: element.Tag) -> dict|None:
        '''
        :param content: the page content of the restaurant
        :return: the service hours table of the restaurant
        '''
        try:
            extractedTable = {}
            table = content.find('table', {"class", "table-whrs"})
            tableHead = table.find('thead')
            tableBody = table.find('tbody')
            listOfMeals = [th.text.strip() for th in tableHead.find_all('th')[1:]]
            listOfDays = [tr.find_all('td')[0].find('span').text.strip() for tr in tableBody.find_all('tr')]
            for i in range(0, len(listOfDays)):
                tmp = {}
                row = tableBody.find_all('tr')[i]
                for j in range(0, len(listOfMeals)):
                    tmp[listOfMeals[j]] = row.find_all('td')[j+1].find('span').text.replace('تا', '_').strip()
                extractedTable[listOfDays[i]] = tmp
            return extractedTable    
        except Exception as error:
            return None