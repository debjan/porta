import json, os, re

import requests


base_url = 'https://www.porta.com.mk/'
headers = {'User-agent': 'Mozilla/5.0'}
buildings = ['residence-1', 'residence-2']


def validate(url):
    '''Verify that URL exists'''
    return requests.get(url, headers=headers).status_code == 200


def get_floor(url, floor={}):
    '''Get floor apartments'''
    r = requests.get(url, headers=headers)
    settings = re.search('var settings = ({.*?});', r.text)
    spots = json.loads(settings.group(1))['spots']
    for spot in spots:
        try:
            fill =spot['default_style']['fill']
            if fill == '#ff0000':
                state = 'Продаден'
            elif fill == '#ffff00':
                state = 'Резервиран'
            else:
                state = 'Достапен'

            floor[spot['title']] = state
        except:
            pass

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
    path = f'{os.path.dirname(os.path.abspath(__file__))}'
    if not os.path.exists(f'{path}/static'):
        os.makedirs(f'{path}/static')
    for building in buildings:
        with open(f'{path}/static/{building}.json', 'w') as js:
            apartments = get_building(building)
            json.dump(apartments, js, ensure_ascii=False)


if __name__ == '__main__':

    update_buildings()
