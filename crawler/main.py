from rich.progress import Progress
from source.tools.json_tools import appender
from source.scraper import Scraper

TARGET_URL = r'https://www.delino.com/restaurant/malibu'

if __name__ == '__main__':
    with Progress() as progress:
        pageNumber = 1
        lastPagecNumber = 1
        while pageNumber <= lastPagecNumber:
            data = []
            fidilioScraper = Scraper()
            scrapeTask = progress.add_task("[cyan]page:{} scrapeing...".format(pageNumber), total=1)
            for item in fidilioScraper.start([TARGET_URL], progress, scrapeTask):
                data.append(item)
            storageTask = progress.add_task("[green]page:{} storaging...".format(pageNumber), total=len(data))
            while not progress.finished:
                appender(data, 'restaurants.json')
                progress.update(storageTask, advance=len(data))
            pageNumber += 1

        
