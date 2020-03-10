"""Application config as object"""
import configparser
from os import path

basepath = path.dirname(path.dirname(path.abspath(__file__)))
parser = configparser.ConfigParser()
parser.read(path.join(basepath, 'config.ini'))


class Config:
    """Class that reads config.ini and stores its values for further use"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(
        path.dirname(path.dirname(path.abspath(__file__))),
        parser['database']['db_file'])
    SQLALCHEMY_TRACK_MODIFICATIONS = parser['database']['track_modifications']
    JWT_SECRET_KEY = parser['security']['jwt_secret']
    DAO_SQL = parser.getboolean('database', 'dao_sql', fallback=False)
