"""
Module to scrape Lamudi
and stores data in local storage as CSV.

Fetched Fields:
name, description, location, link, price, operation, rooms, bathrooms, construction (m2), terrain (m2)
"""
from clients.http_client import HttpClient
from savers.xlsx_saver import XlsxSaver
from base import Scraper as BaseScraper
from random import random, choice
from math import trunc
from requests.exceptions import HTTPError


class Scraper(BaseScraper):

    FIELDS = {
        'name': {
            'resolve_element': lambda element: element.find(class_="ListingCell-KeyInfo-title"),
            'attribute': 'text'
        },
        'description': {
            'resolve_element': lambda element: element.find(class_="ListingCell-shortDescription"),
            'attribute': 'text'
        },
        'location': {
            'resolve_element': lambda element: element.find(class_="ListingCell-KeyInfo-address"),
            'attribute': 'text'
        },
        'link': {
            'resolve_element': lambda element: element.find('a'),
            'attribute': 'href'
        },
        'public_price': {
            'resolve_element': lambda element: element.find(class_="PriceSection-FirstPrice"),
            'attribute': 'text'
        },
        'price': {
            'resolve_element': lambda element: element,
            'attribute': 'data-price'
        },
        'category': {
            'resolve_element': lambda element: element,
            'attribute': 'data-category'
        },
        'rooms': {
            'resolve_element': lambda element: element,
            'attribute': 'data-bedrooms'
        },
        'garage': {
            'resolve_element': lambda element: element,
            'attribute': 'data-bedrooms'
        },
        'bathrooms': {
            'resolve_element': lambda element: element,
            'attribute': 'data-bedrooms'
        },
        'construction (m2)': {
            'resolve_element': lambda element: element,
            'attribute': 'data-building_size'
        },
        'geolocation': {
            'resolve_element': lambda element: element,
            'attribute': 'data-geo-point'
        },
        'terrain (m2)': {
            'resolve_element': lambda element: element,
            'attribute': 'data-land_size'
        }
    }

    PHONE_CODES = (414, 424, 416, 426, 412)

    def resolve_extrafields(self, temp_data):
        temp_data.update(
            self.resolve_phones(temp_data['link'])
        )

    def resolve_phones(self, link):
        phone =  trunc(1_000_000 + random() * 8_999_999)
        code = choice(self.PHONE_CODES)
        url = f"{link}/whatsapp-request-phone?pageType=catalog&deviceType=desktop"
        data = {'request_phone[phone_input]': f"{code}{phone}", 'request_phone[phone]': f"+58{code}{phone}"}
        try:
            json_response = HttpClient().make('post', url, data= data).json()
        except HTTPError:
            return { 'phone_number': None, 'mobile_number': None, 'office_phone': None }
        return {
            'phone_number': json_response['phone_number'],
            'mobile_number': json_response['mobilePhone'],
            'office_phone': json_response['officePhone']
        }

def start():
    """ Loop over pages to retrieve all info available
    """
    state = 'nuevo-leon'
    operation = 'sale'
    base_url = f"https://www.lamudi.com.mx/{state}/for-{operation}/?page=" + '{}'
    page_number = 1
    while True:
        try:
            response = HttpClient().make('get', base_url.format(page_number))
        except HTTPError:
            print("Wrong Response!")
            break

        departeres = Scraper(response.content).run()
        if departeres.empty:
            print("No more departments")
            break

        XlsxSaver('lamudi', state, operation).save(departeres)
        page_number += 1


def main():
    """ Main method """
    print('Starting to scrape Lamudi')
    start()
    print('Done')


if __name__ == '__main__':
    main()
