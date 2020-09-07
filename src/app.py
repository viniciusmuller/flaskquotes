from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from config import FlaskConfig

# Flask app configuration
app = Flask(__name__)
app.config.from_object(FlaskConfig)

login = LoginManager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

import utils
import routes

if __name__ == '__main__':
    app.run()
