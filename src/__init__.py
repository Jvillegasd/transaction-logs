from src.controllers import home_api
from src.config.app_config import config_by_name
from src.connection.database import DataAccessLayer

from flask import Flask, g


def get_dal() -> DataAccessLayer:
    """Store a Data Access Layer instance in Flask
    Application context for use this across requests.

    Returns:
        -   DataAccessLayer
    """

    if 'dal' not in g:
        g.dal = DataAccessLayer()

    return g.dal


def create_app(config_name: str) -> Flask:
    """Creates a Flask application and loads configurations
    depending on the provided environment. After the application
    is created, current application context is pushed for 
    use loaded varibles outside context.

    Args:
        -   config_name: str = Enviroment configuration

    Returns:
        -   Flask = Flask application
    """

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Push the Application context
    app.app_context().push()

    # Blueprints
    app.register_blueprint(home_api, url_prefix='/api')

    return app
