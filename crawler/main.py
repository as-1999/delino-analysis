from os import path
import crawler

if __name__ == '__main__':
    file_path = path.dirname(__file__)
    crawler.CrawlerTool('firefox', file_path)
    #crawler.CrawlerTool('chrome', file_path)
