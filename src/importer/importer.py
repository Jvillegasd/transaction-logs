import os
import json
from importlib import import_module

from src.connection.database import DataAccessLayer


class DataImporter:

    def __init__(self):
        self.dal = DataAccessLayer()
        self.pwd = os.path.abspath(os.path.dirname(__file__))

        self.seeds: dict[str, dict] = self._load_seeds()
        self.import_order: dict = self._load_import_order()

    def _load_seeds(self) -> dict[str, dict]:
        seeds: dict[str, dict] = {}
        seeds_dir = os.path.abspath(os.path.join(self.pwd, 'seeds'))
        seeds_files = os.listdir(seeds_dir)

        for file_name in seeds_files:
            file = os.path.abspath(os.path.join(seeds_dir, file_name))

            with open(file, 'r') as f:
                seeds[file_name[:-5]] = json.load(f)

        return seeds

    def _load_import_order(self) -> dict:
        import_order: dict = {}
        order_dir = os.path.abspath(
            os.path.join(self.pwd, 'import_order.json')
        )

        with open(order_dir, 'r') as f:
            import_order = json.load(f)

        return import_order
