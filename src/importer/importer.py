import os
import json
from importlib import import_module

from src.models.base_model import BaseModel
from src.connection.database import DataAccessLayer
from src.models.transaction import TransactionStatus

from sqlalchemy.orm.session import Session


class DataImporter:

    def __init__(self):
        self.dal = DataAccessLayer()
        self.pwd = os.path.abspath(os.path.dirname(__file__))

        self.seeds: dict[str, dict] = self._load_seeds()
        self.import_order: list[str] = self._load_import_order()

    def _load_seeds(self) -> dict[str, dict]:
        """This method loads seeds JSON files stored in their
        folder for in-memory consulting.

        Returns:
            -   dict[str, dict] = A dict with the seeds
            stored in the specified folder. Where their keys represents
            model's name and their value the seeds.
        """

        seeds: dict[str, dict] = {}
        seeds_dir = os.path.abspath(os.path.join(self.pwd, 'seeds'))
        seeds_files = os.listdir(seeds_dir)

        for file_name in seeds_files:
            file = os.path.abspath(os.path.join(seeds_dir, file_name))

            with open(file, 'r') as f:
                seed_dict = json.load(f)
                seeds[seed_dict['model_name']] = seed_dict

        return seeds

    def _load_import_order(self) -> list[str]:
        """This method loads the import order list stored
        in JSON file and it's used for loads all models in the right
        order.

        Returns:
            -   list[str] = List of model names.
        """

        import_order: dict = {}
        order_dir = os.path.abspath(
            os.path.join(self.pwd, 'import_order.json')
        )

        with open(order_dir, 'r') as f:
            import_order = json.load(f)

        return import_order

    def _load_transaction_model(
        self,
        data: dict,
        model: BaseModel,
        db: Session
    ) -> list:
        """Loads transaction model seeds and calculates
        transaction status by checking if user has sufficient
        funds at the moment this transaction occurs.

        Args:
            -   data: dict = Transaction seeds.
            -   model: BaseModel = Transaction model.
            -   db: Session = SQLAlchemy session.

        Returns:
            -   list = A list with the seeds of the model.
        """

        user_balance: dict[str, float] = {}
        negative_types: set[str] = {'withdraw', 'expense'}

        for i in range(len(data['records'])):
            seed = data['records'][i]

            user_id = seed['user_id']
            if user_id not in user_balance:
                user_balance[user_id] = 0.0

            amount = seed['amount']
            if seed['transaction_type'] in negative_types:
                amount = abs(amount) * -1
                seed['amount'] = amount

            if user_balance[user_id] + amount >= 0:
                seed['status'] = TransactionStatus.acepted
                user_balance[user_id] += amount
            else:
                seed['status'] = TransactionStatus.rejected

            record = model(**seed)
            db.add(record)
            db.commit()

        return data['records']

    def load_model(self, model_name: str) -> list:
        """Loads seeds to database for the provided
        model name.

        Args:
            -   model_name: str

        Returns:
            -   list = A list with the seeds of the model.
        """

        data = self.seeds[model_name]
        with self.dal.get_session() as db:
            module_name, class_name = data['model'].rsplit('.', 1)
            module = import_module(module_name)
            model = getattr(module, class_name)

            if model_name != 'transactions':
                for seed in data['records']:
                    record = model(**seed)
                    db.add(record)
                    db.commit()
            else:
                data['records'] = self._load_transaction_model(
                    data,
                    model,
                    db
                )

        return data['records']

    def load_all_models(self):
        """This method load all tables of models that
        have created seeds.
        """

        for model_name in self.import_order:
            self.load_model(model_name)

    def clear_model(self, model_name: str):
        """This method clean records from database
        related to provided model name.

        Args:
            -   model_name: str
        """

        data = self.seeds[model_name]
        with self.dal.get_session() as db:
            module_name, class_name = data['model'].rsplit('.', 1)
            module = import_module(module_name)
            model = getattr(module, class_name)
            db.query(model).delete()
            db.commit()

    def clear_all_models(self):
        """This method clean all tables of loaded
        models.
        """

        remove_order = list(reversed(self.import_order))
        for model_name in remove_order:
            self.clear_model(model_name)
