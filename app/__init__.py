from flasgger import Swagger
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.commands import usersbp
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(usersbp)
swagger = Swagger(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.apis import dashboard, transaction, user
from app.models import transaction, user
