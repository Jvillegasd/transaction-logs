import os
import json
from importlib import import_module

from src.connection.database import DataAccessLayer


class DataImporter:

    def __init__(self):
        self.dal = DataAccessLayer()
        self.pwd = os.path.abspath(os.path.dirname(__file__))
        self.order_dir = os.path.abspath(
            os.path.join(self.pwd, 'import_order.json')
        )
        self.seeds_dir = os.path.abspath(os.path.join(self.pwd, 'seeds'))
        seeds_files = os.listdir(self.seeds_dir)

        self.seeds: dict[str, dict] = {}
        for file_name in seeds_files:
            file = os.path.abspath(os.path.join(self.seeds_dir, file_name))

            with open(file, 'r') as f:
                self.seeds[file_name[:-5]] = json.load(f)

        with open(self.order_dir, 'r') as f:
            self.import_order = json.load(f)
