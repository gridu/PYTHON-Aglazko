"""Initialization of flask plugins and logging """

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import logging

db = SQLAlchemy()

migrate = Migrate()

jwt = JWTManager()

FORMAT = '%(asctime)s %(message)s'
fh = logging.FileHandler('app.log')
fh.setFormatter(logging.Formatter(FORMAT))
# logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.addHandler(fh)
logger.setLevel(logging.INFO)



