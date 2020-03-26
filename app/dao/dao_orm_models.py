"""Classes to retrieve data from database via ORM"""

from copy import copy
from app.models.models import AnimalCenter, Animal, AccessRequest, Species
from app.dao.interfaces import IDaoAccessRequest, IDaoAnimalCenter, IDaoAnimal, IDaoSpecies, IDaoDeserializer
from app import db
from . import dao
from werkzeug.security import check_password_hash


class AnimalCenterORM(IDaoAnimalCenter, IDaoDeserializer):

    def deserialize(self, record=None, long=False):
        """
        Function that create dictionary from object.
        :param long: Value of this param define which version of data will be returned. If value True function will
                     return long version of dictionary with such keys: id, login, address. Otherwise dictionary wil
                     not contain kye address.
        :return data: Dictionary with information about object.
        """
        data = {'id': record.id,
                'login': record.login}
        if long:
            data.update({'address': record.address})
        return data

    def check_password(self, password, user_id):
        record = AnimalCenter.query.get(user_id)
        return check_password_hash(record.password_hash, password)

    def get_centers(self):
        return [self.deserialize(record, long=False) for record in AnimalCenter.query.all()]

    def get_center_inform(self, id):
        record = AnimalCenter.query.get(id)
        if record:
            return (self.deserialize(record, long=True),
                    [dao.AnimalDAO.deserialize(animal) for animal in record.animals])
        return None

    def get_center_by_login(self, user_login):
        center = AnimalCenter.query.filter_by(login=user_login).first()
        if center:
            return self.deserialize(center)
        else:
            return None

    def add_center(self, data):
        center = AnimalCenter(login=data['login'], address=data['address'])
        center.set_password(data['password'])
        db.session.add(center)
        db.session.commit()
        return center.id


class AccessRequestORM(IDaoAccessRequest):

    def create_access_request(self, user_id):
        access_request = AccessRequest(center_id=user_id)
        db.session.add(access_request)
        db.session.commit()


class AnimalORM(IDaoAnimal, IDaoDeserializer):

    def deserialize(self, record=None, long=False):
        """
        Function that create dictionary from object.
        :param long: Value of this param define which version of data will be returned. If value True function will
                     return long version of dictionary with such keys: id, name, center_id, description, age,
                     species_id, price. Otherwise dictionary wil contain only id and name.
        :return data: Dictionary with information about object.
        """
        data = {'id': record.id,
                'name': record.name}
        if long:
            data.update({
                'center_id': record.center_id,
                'description': record.description,
                'age': record.age,
                'species_id': record.species_id,
                'price': record.price
            })
        return data

    def get_animals(self):
        animals = [self.deserialize(animal) for animal in Animal.query.all()]
        return animals

    def add_animal(self, data, userid):
        animal = Animal(name=data['name'], center_id=userid,
                        description=data['description'], price=data['price'],
                        species_id=data['species_id'], age=data['age'])
        db.session.add(animal)
        db.session.commit()
        return self.deserialize(animal)

    def get_animal(self, animal_id):
        animal = Animal.query.get(animal_id)
        return self.deserialize(animal, long=True) if animal else None

    def delete_animal(self, animal_id):
        animal = Animal.query.get(animal_id)
        db.session.delete(animal)
        db.session.commit()

    def update_animal(self, animal):
        animal = copy(animal)
        animal_id = animal.pop('id')
        animal_obj = Animal.query.get(animal_id)
        for key, value in animal.items():
            setattr(animal_obj, key, value)
        db.session.commit()


class SpeciesORM(IDaoSpecies, IDaoDeserializer):

    def deserialize(self, record=None, long=False):
        """
        Function that create dictionary from object.
        :return: Dictionary with information about object.
        """
        data = {'id': record.id,
                'name': record.name,
                'description': record.description,
                'price': record.price}
        return data

    def get_species(self):
        result = db.session.query(
            Species.name, db.func.count(Animal.name)) \
            .join(Animal, Species.id == Animal.species_id, isouter=True) \
            .group_by(Species.id).all()
        return [{'species_name': name, 'count_of_animals': count} for name, count in result]

    def get_species_inform(self, id):
        species = Species().query.get(id)
        animals = Animal.query.filter_by(species_id=id).all()

        if species:
            return (self.deserialize(species, long=True),
                    [dao.AnimalDAO.deserialize(animal) for animal in animals])
        else:
            return None

    def add_species(self, data):
        specie = Species(name=data['name'], description=data['description'],
                         price=data['price'])
        db.session.add(specie)
        db.session.commit()
        return self.deserialize(specie, long=True)

    def get_species_by_name(self, name):
        species = Species.query.filter_by(name=name).first()
        if species:
            return self.deserialize(species)
        else:
            return None
