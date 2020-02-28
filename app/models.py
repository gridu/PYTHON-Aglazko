"""This module declares models(AnimalCenter, AccessRequest, Animal, Species) for database."""
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.interfaces import IAnimalCenter


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
    # animals = db.relationship("Animal", backref="animals")

    def set_password(self, password):
        """
        Function that creates password hash.
        :param password: Password that set user.
        :return : None
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        The function that check user password when he/she is trying to authorize.
        :param password: Password that set user.
        :return True: If password is correct.
        :return False: If password is incorrect.
        """
        return check_password_hash(self.password_hash, password)

    def deserialize(self, record=None, long=False):
        """
        Function that create dictionary from object.
        :param long: Value of this param define which version of data will be returned. If value True function will
                     return long version of dictionary with such keys: id, login, address. Otherwise dictionary wil
                     not contain kye address.
        :return data: Dictionary with information about object.
        """
        data = {'id': self.id,
                'login': self.login}
                # TODO 'animals': self.animals}
        if long:
            data.update({'address': self.address})
        return data


class AccessRequest(db.Model):
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

    def to_dict(self):
        """
        Function that create dictionary from object.
        :return: Dictionary with information about object.
        """
        return {'id': self.id,
                'center_id': self.center_id,
                'timestamp': self.timestamp}


class Animal(db.Model):
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

    def to_dict(self, long=False):
        """
        Function that create dictionary from object.
        :param long: Value of this param define which version of data will be returned. If value True function will
                     return long version of dictionary with such keys: id, name, center_id, description, age,
                     species_id, price. Otherwise dictionary wil contain only id and name.
        :return data: Dictionary with information about object.
        """
        data = {'id': self.id,
                'name': self.name}
        if long:
            data.update({
                'center_id': self.center_id,
                'description': self.description,
                'age': self.age,
                'species_id': self.species_id,
                'price': self.price
            })
        return data


class Species(db.Model):
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

    def to_dict(self):
        """
        Function that create dictionary from object.
        :return: Dictionary with information about object.
        """
        return {'id': self.id,
                'name': self.name,
                'description': self.description,
                'price': self.price}
