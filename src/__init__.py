from src.controllers import home_api, users_api
from src.config.app_config import config_by_name

from flask import Flask


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
    app.register_blueprint(users_api, url_prefix='/api/users')

    return app
