from bs4 import BeautifulSoup
import traceback

class Scraper:

    FIELDS = {
        'name': {
            'resolve_element': lambda element: element.find(class_="ListingCell-KeyInfo-title"),
            'attribute': 'text'
        },
        'price': {
            'resolve_element': lambda element: element,
            'attribute': 'data-price'
        }
    }
    CARD_CLASS = "ListingCell-AllInfo"

    def __init__(self, content):
        self.parser = BeautifulSoup(content, 'html.parser')
        self.data_list = []

    def get_value(self, element, attribute):
        try:
            if attribute == 'text':
                return element.text.strip()
            
            return element.get(attribute).strip()
        except AttributeError:
            return None

    def resolve_extrafields(self, temp_data):
        pass

    def run(self) -> list:
        for element in self.parser.find_all(class_=self.CARD_CLASS):
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

            self.resolve_extrafields(temp_data)
            self.data_list.append(temp_data)

        print(f"Found {len(self.data_list)} depts")
        return self.data_list
