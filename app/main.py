from flask import Flask
from config import Config
from app import db, migrate, jwt
from app.routes import bp as routes_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    app.register_blueprint(routes_bp)
    app.db = db
    return app
