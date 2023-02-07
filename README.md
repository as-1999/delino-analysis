# download these
```bash
pip install selenium
pip install webdriver-manager
pip install BeautifulSoup4
```

# how to use 
```python
from crawler import CrawlerTool
CrawlerTool('firefox', file_path)

```
or (not recommended)
```python
from crawler import CrawlerTool
CrawlerTool('chrome', file_path)

```
file_path is the path of the file you want to save the data
