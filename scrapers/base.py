import pandas as pd
from bs4 import BeautifulSoup
import traceback

class Scraper:

    # FIELDS example TODO: Create a json or yml base
    # FIELDS = {
    #     'name': {
    #         'resolve_element': lambda element: element.find(class_="ListingCell-KeyInfo-title"),
    #         'attribute': 'text'
    #     },
    #     'price': {
    #         'resolve_element': lambda element: element,
    #         'attribute': 'data-price'
    #     }
    # }

    def __init__(self, content):
        self.parser = BeautifulSoup(content, 'html.parser')
        self.data_list = []
        self.data_frame = pd.DataFrame(columns=self.FIELDS.keys())

    def get_value(self, element, attribute):
        try:
            if attribute == 'text':
                return element.text.strip()
            
            return element.get(attribute).strip()
        except AttributeError:
            return None

    def run(self):
        for element in self.parser.find_all(class_="ListingCell-AllInfo"):
            temp_data = {}
            try:
                for field, resolver in self.FIELDS.items():
                    temp_data[field] = self.get_value(
                        resolver['resolve_element'](element),
                        resolver['attribute']
                    )
            except Exception as e:
                print("ERROR ---- BEGIN")
                print(traceback.format_exc())
                print("ERROR ---- END")
                continue
            self.data_list.append(temp_data)

        print(f"Found {self.data_frame.size} depts")
        return pd.DataFrame(self.data_list)
