from celery import Celery
from flasgger import Swagger
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.commands import usersbp
from config import Config


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery


app = Flask(__name__)
app.config.from_object(Config)
celery = make_celery(app)

app.register_blueprint(usersbp)
swagger = Swagger(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import tasks
from app.apis import dashboard, transaction, user
from app.models import transaction, user
