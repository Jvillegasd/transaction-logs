from src.config.app_config import config_by_name
from src.connection.database import DataAccessLayer

from flask import Flask

dal = DataAccessLayer()


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    return app
