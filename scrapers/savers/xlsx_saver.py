from datetime import date
import pandas as pd
from os import mkdir
import traceback


class XlsxSaver:

    def __init__(self, base_name, state, operation) -> None:
        self.folter_name = f"data/{date.today().isoformat()}"
        self.file_name = f"{self.folter_name}/{base_name}-{state.replace('/', '-')}-{operation}.xlsx"

    def save(self, buildings_data: list):
        """ Append page data

            Params:
            -----
            buildings_data : list
                Dataframe of Departments
        """
        self.create_folder()
        buildings_data = pd.DataFrame(buildings_data)
        try:
            pd.concat([self.df, buildings_data]).set_index('id').to_excel(self.file_name)
        except Exception:
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
        try:
            return pd.read_excel(self.file_name)
        except FileNotFoundError:
            return pd.DataFrame()
