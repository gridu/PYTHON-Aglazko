"""This module declares models(AnimalCenter, AccessRequest, Animal, Species) for database."""
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.interfaces import IAnimalCenter, IAccessRequest, ISpecies, IAnimal


class AnimalCenter(db.Model, IAnimalCenter):
    """
    This is a class for creating animalcenter table in database.
    It contains detailed information about each animal center.
    Attributes:
        id (int): Auto-generated id for user, primary key.
        login (string): Login(user name) that user use for authorization.
        password_hash (string): Store password in db insecure, so we keep only hash of password in db.
        address (string): The address of animal center.
    """
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20))
    password_hash = db.Column(db.String(256))
    address = db.Column(db.String(200))
    animals = db.relationship("Animal", backref="animals")

    def set_password(self, password):
        """
        Function that creates password hash.
        :param password: Password that set user.
        :return : None
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password, user_id=None):
        """
        The function that check user password when he/she is trying to authorize.
        :param password: Password that set user.
        :return True: If password is correct.
        :return False: If password is incorrect.
        """
        return check_password_hash(self.password_hash, password)


class AccessRequest(db.Model, IAccessRequest):
    """
    Class for creating accessrequest table in db.
    In db will saved history of all successful requests.
    Parameters:
        id (int): Id of access request, auto-generated, primary key.
        center_id: Id of user that had access request.
        timestamp: Time when was request.
    """
    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, db.ForeignKey("animal_center.id"))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Animal(db.Model, IAnimal):
    """
    Class for creating animal table in db.
    It contains detailed information about each animal.
    Parameters:
        id (int): Id of animal, auto-generated, primary key.
        center_id (int): Animal owner id, foreign key.
        name (string): Animal name.
        description (string): Description of animal.
        age (int): Animal age.
        species_id (int): Species id to which belongs animal.
        price (float): Animal price.

    """
    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, db.ForeignKey("animal_center.id"))
    name = db.Column(db.String(40))
    description = db.Column(db.String(500), nullable=True)
    age = db.Column(db.Integer)
    species_id = db.Column(db.Integer, db.ForeignKey("species.id"))
    price = db.Column(db.Float, nullable=True)


class Species(db.Model, ISpecies):
    """
    Class for creating species table in db.
    Contains detailed information about species.
    Parameters:
        id (int): Species id.
        name (string): Species name.
        description (string): Description of species.
        price (float): Species price.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=True)
