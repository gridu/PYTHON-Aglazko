# import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_jwt_extended import JWTManager
import logging

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

jwt = JWTManager(app)

FORMAT = '%(asctime)s %(message)s'
fh = logging.FileHandler('app.log')
fh.setFormatter(logging.Formatter(FORMAT))
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.addHandler(fh)
logger.setLevel(logging.INFO)

# logger = logging.getLogger("")




# def log_request(method, request_url, center_id, entity_type, entity_id):
#     logger.info('method %s request_url %s center_id %s entity_type %s entity_id %s', method, request_url, center_id,
#                 entity_type, entity_id)


from app import routes, models
