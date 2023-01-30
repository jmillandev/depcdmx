"""
Module to scrape Segunda Mano DF appartments
and stores data in local storage as XLSX.
"""
from application import Entrypoint
from re import search
from requests.exceptions import HTTPError
from clients.http_client import HttpClient
import json
from json.decoder import JSONDecodeError


class Scraper:
    ID_REGEX = r'(?P<id>\d+)$'

    FIELDS = {
        'description': 'body',
        'price': 'list_price.price_value',
        'link': 'share_link',
        'name': 'subject',
        'agent_name': 'user.account.name',
        'agent_id': 'user.account.user_uuid',
        'category': 'estate_type.single.label',
        'posted_on': 'list_time.label',
        'company_ad': 'company_ad',
        'paid': 'paid',
        'phone_hidden': 'phone_hidden',
        'bathrooms': 'ad_details.bathrooms.single.label',
        'terrain (m2)': 'ad_details.lot_area.single.label',
        'construction (m2)': 'ad_details.size.single.label',
        'rooms': 'ad_details.rooms.single.label',
        'garage': 'ad_details.parking_lots.single.label',
    }

    def __init__(self, content: str):
        self.content = content

    def resolve_value(self, item, path):
        for key in path.split('.'):
            if not item:
                return None
            item = item.get(key, None)
        return item
    
    def build_location(self, data):
        location = ''
        data = data.get('locations', None)
        while data:
            data = data[0]
            location += ' - ' + data['label']
            data = data.get('locations', None)
        return location

    def resolve_phones(self, id):
        url = f"https://webapi.segundamano.mx/nga/api/v1/public/klfst/{id}/phone"
        try:
            return HttpClient().make('get', url).json()['phones'][0]['value']
        except (HTTPError, IndexError):
            return None

    def resolve_item(self, raw_item):
        item = {}
        for field, path in self.FIELDS.items():
            item[field] = self.resolve_value(raw_item['ad'], path)

        item['id'] = search(self.ID_REGEX, item['link']).group('id')
        item['location'] = self.build_location(raw_item['ad'])
        item['phone'] = self.resolve_phones(item['id'])
        return item

    def run(self)-> list:
        return [self.resolve_item(raw_item) for raw_item in self.raw_items()['list_ads']]

    def raw_items(self):
        for line in self.content.split('\n'):
            if 'initialAds' in line:
                break
        else:
            raise Exception('initialAds Not found')

        string = line[:-1].removeprefix('var initialAds="').replace('\\"', '"').replace('\\"', "'").replace("\\'", "'")
        try:
            return json.loads(string)
        except JSONDecodeError:
            with open('data/segundamano.json', 'w') as file:
                file.write(string)
            raise Exception('initialAds with invalid')


if __name__ == '__main__':    
    Entrypoint(
        'ciudad-de-mexico',
        'renta',
        'https://www.segundamano.mx/anuncios/{state}/{operation}-inmuebles?orden=date&page={page_number}',
        Scraper
    ).start()
