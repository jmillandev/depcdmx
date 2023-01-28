from datetime import date
import pandas as pd
from os import mkdir
import traceback


class XlsxSaver:

    def __init__(self, base_name, state, operation) -> None:
        self.folter_name = f"data/{date.today().isoformat()}"
        self.file_name = f"{self.folter_name}/{base_name}-{state}-{operation}.xlsx"
        self._df = None

    def save(self, buildings_data):
        """ Append page data

            Params:
            -----
            buildings_data : pd.Dataframe()
                Dataframe of Departments
        """
        self.create_folder()
        print(buildings_data.head(1).to_dict())
        try:
            df = pd.concat([self.df, buildings_data])
            df.set_index(['name', 'location']).to_excel(self.file_name)
        except Exception as e:
            print("ERROR ---- BEGIN")
            print(traceback.format_exc())
            print("ERROR ---- END")
            print(f"Could not save file: {self.file_name}")
        print(f"Correctly saved file: {self.file_name}")

    def create_folder(self):
        print('Creating folder..')
        try:
            mkdir(self.folter_name)
            print('Created folder!')
        except FileExistsError:
            print('Folder already exists!')

    @property
    def df(self):
        if self._df:
            return self._df

        try:
            self._df = pd.read_excel(self.file_name)
        except FileNotFoundError:
            self._df = pd.DataFrame()

        return self._df
