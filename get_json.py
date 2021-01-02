import json

from lxml import html
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


base_url = 'https://www.porta.com.mk/'
headers = {'User-agent': 'Mozilla/5.0'}
buildings = ['residence-1', 'residence-2']


def validate(url):
    '''Verify that URL exists'''

    req = requests.get(url, headers=headers)

    return req.status_code == 200


def get_driver(url):
    '''Get page from selenium'''

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--no-startup-window')
    options.add_argument('log-level=3')

    driver = Chrome(options=options)
    driver.get(url)

    return driver


def get_floor(url, floor={}):
    '''Get floor apartments'''

    driver = get_driver(url)
    doc = html.fromstring(driver.page_source)
    polygons = doc.xpath('//svg[@class="hs-poly-svg"]/polygon')
    for polygon in polygons:
        style = {x.split(':')[0]: x.split(':')[1].strip() for x in
                 polygon.xpath('@style')[0].split(';') if len(x)}

        if style['fill'].startswith('rgba(255, 0, 0'):
            state = 'Продаден'
        elif style['fill'].startswith('rgba(255, 255, 0'):
            state = 'Резервиран'
        else:
            state = 'Достапен'

        floor[polygon.xpath('@data-shape-title')[0]] = state

    driver.close()

    return floor


def get_building(building, ceil=100):
    '''Get building apartments'''

    apartments = {}
    for floor in range(ceil):
        url = f'{base_url}{building}-sprat-{floor + 1}/'
        if not validate(url):
            break
        floor = get_floor(url)
        apartments.update(floor)

    return apartments


def update_buildings():
    '''Update buildings data'''

    for building in buildings:
        with open(f'static/{building}.json', 'w') as js:
            apartments = get_building(building)
            json.dump(apartments, js)

if __name__ == '__main__':

    update_buildings()
