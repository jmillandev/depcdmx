from clients.http_client import HttpClient
from requests.exceptions import HTTPError
from savers.xlsx_saver import XlsxSaver
from re import search


class Entrypoint:
    HOST_REGEX = r':\/\/(\w+\.)?(?P<host>\w+)(\.\w+)'

    def __init__(self, state, operation, base_url, scraper_class) -> None:
        self.base_url = base_url
        self.state = state
        self.operation = operation
        self.Scraper = scraper_class
        self.page_number = 1
        self._safer = None

    def start(self):
        """ Loop over pages to retrieve all info available
        """
        print('Starting to scrape')
        while True:
            departeres = self.Scraper(self.visit_page()).run()
            if not departeres:
                print("No more departments")
                break

            self.safer.save(departeres)
            self.page_number += 1
        print('Done')

    def visit_page(self):
        try:
            return HttpClient().make('get', self.url).text
        except HTTPError:
            print("Wrong Response!")
            return ''

    @property
    def url(self):
        return self.base_url.format(
            state= self.state,
            operation= self.operation,
            page_number= self.page_number
        )

    @property
    def safer(self):
        if self._safer is None:
            host = search(self.HOST_REGEX, self.base_url).group('host')
            self._safer = XlsxSaver(host, self.state, self.operation)
        return self._safer
