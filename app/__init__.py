from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger

from app.commands import usersbp

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(usersbp)
swagger = Swagger(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import transaction, user
from app.apis import dashboard, transaction, user
