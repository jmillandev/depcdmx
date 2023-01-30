"""
Module to scrape Lamudi
and stores data in local storage as XLSX.

Fetched Fields:
name, description, location, link, price, operation, rooms, bathrooms, construction (m2), terrain (m2)
"""
from clients.http_client import HttpClient
from base import Scraper as BaseScraper
from random import random, choice
from math import trunc
from requests.exceptions import HTTPError
from application import Entrypoint


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
        },
        'id': {
            'resolve_element': lambda element: element,
            'attribute': 'data-sku'
        },
        'agent_name': {
            'resolve_element': lambda element: element.find(class_="ListingDetail-agent-name"),
            'attribute': 'text'
        },
        'agent_link': {
            'resolve_element': lambda element: element.find(class_="ListingDetail-agentDetail-agentLink"),
            'attribute': 'href'
        },
        'agent_id': {
            'resolve_element': lambda element: element.find(class_="ListingCell-contactAgent-button"),
            'attribute': 'data-agent-id'
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
            'phone_number': json_response.get('phone_number'),
            'mobile_number': json_response.get('mobilePhone'),
            'office_phone': json_response.get('officePhone')
        }

if __name__ == '__main__':
    Entrypoint(
        'distrito-federal',
        'rent',
        'https://www.lamudi.com.mx/{state}/for-{operation}/?sorting=newest&page={page_number}',
        Scraper
    ).start()
