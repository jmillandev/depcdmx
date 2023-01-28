"""
Module to scrape Lamudi
and stores data in local storage as CSV.

Fetched Fields:
name, description, location, link, price, operation, rooms, bathrooms, construction (m2), terrain (m2)
"""
from clients.http_client import HttpClient
from savers.xlsx_saver import XlsxSaver
from base import Scraper as BaseScraper

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
        # TODO: Add Phone resolver
        }
    }

def start():
    """ Loop over pages to retrieve all info available
    """
    state = 'nuevo-leon'
    operation = 'sale'
    base_url = f"https://www.lamudi.com.mx/{state}/for-{operation}/?page=" + '{}'
    page_number = 1
    while True:
        response = HttpClient().make('get', base_url.format(page_number))
        if response.status_code != 200:
            print("Wrong Response!")
            breakpoint() # TODO: Use bad request exception
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
