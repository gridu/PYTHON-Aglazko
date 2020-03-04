"""Application config as object"""
import configparser
import os

parser = configparser.ConfigParser()
parser.read('config.ini')


class Config:
    """Class that reads config.ini and stores its values for further use"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        parser['default']['db_file'])
    SQLALCHEMY_TRACK_MODIFICATIONS = parser['default']['track_modifications']
    JWT_SECRET_KEY = parser['default']['jwt_secret']
