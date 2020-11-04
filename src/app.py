from flask import Flask

from blueprints.server_routes import server_routes
from blueprints.user_routes import user_routes
from blueprints.errors import error_handling
from config.config import FlaskConfig
from exts import bootstrap
from exts import login
from exts import db


BLUEPRINTS = [server_routes, user_routes, error_handling]


def register_extensions(app: Flask) -> None:
    """Registering the extensions to the app object"""

    bootstrap.init_app(app)
    login.init_app(app)
    db.init_app(app)

    # Creating the database TODO this comment is dumb
    with app.app_context():
        db.create_all()


def create_app(config: object) -> Flask:
    """Flask factory pattern to return an app object."""
    app = Flask(__name__)

    app.config.from_object(config)

    register_extensions(app)

    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)

    return app


app = create_app(FlaskConfig)
