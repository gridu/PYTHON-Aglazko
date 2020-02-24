from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class AnimalCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20))
    password_hash = db.Column(db.String(256))
    address = db.Column(db.String(200))
    animals = db.relationship("Animal", backref="animals")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {'id': self.id,
                'login': self.login,
                'address': self.address,
                'animals': self.animals}


class AccessRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, db.ForeignKey("animal_center.id"))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {'id': self.id,
                'center_id': self.center_id,
                'timestamp': self.timestamp}


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, db.ForeignKey("animal_center.id"))
    name = db.Column(db.String(40))
    description = db.Column(db.String(500), nullable=True)
    age = db.Column(db.Integer)
    species_id = db.Column(db.Integer, db.ForeignKey("species.id"))
    price = db.Column(db.Float, nullable=True)

    def to_dict(self, long=False):
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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description,
                'price': self.price}

