from app import db
from copy import copy
from werkzeug.security import check_password_hash
from app.interfaces import IAnimalCenter


class AnimalsDAO(IAnimalCenter):
    # @staticmethod
    def _deserialize(self, record=None, long=False):
        data = {
            'id': record[0],
            'name': record[2]
        }
        if long:
            data.update({
                'center_id': record[1],
                'description': record[3],
                'age': record[4],
                'species_id': record[5],
                'price': record[6]
            })
        return data

    @staticmethod
    def get_animals():
        records = db.engine.execute("SELECT * FROM animal;")
        return [AnimalsDAO._deserialize(record) for record in records]

    @staticmethod
    def get_animal(animal_id):
        record = db.engine.execute(
            "SELECT * FROM animal WHERE id={}".format(animal_id)).first()
        return AnimalsDAO._deserialize(record, long=True) if record else None

    @staticmethod
    def delete_animal(animal_id):
        db.engine.execute("DELETE FROM animal WHERE id={}".format(animal_id))

    @staticmethod
    def update_animal(animal):
        animal = copy(animal)
        animal_id = animal.pop('id')
        update_string = ','.join(
            ['{}={}'.format(key, value) for key, value in animal.items()])
        db.engine.execute(
            "UPDATE animal SET {} WHERE id={}".format(
                update_string, animal_id))


class AnimalCentersDAO(IAnimalCenter):
    # @staticmethod
    def deserialize(self, record=None, long=False):
        data = {'id': record.id,
                'login': record.login}
        if long:
            data.update({'address': record.address})
        return data

    # @staticmethod
    def get_centers(self):
        records = db.engine.execute("SELECT * FROM animal_center;")
        return [AnimalCentersDAO().deserialize(record, long=False) for record in records]

    @staticmethod
    def get_center_inform(id):
        record = db.engine.execute(
            "SELECT * FROM animal_center WHERE id ={};".format(id)).first()
        return AnimalCentersDAO.deserialize(record, long=True) if record else None

    @staticmethod
    def get_center_by_login(login):
        record = db.engine.execute(
            "SELECT * FROM animal_center WHERE login='{}';".format(login)).first()
        return AnimalCentersDAO.deserialize(record, long=True) if record else None

    @staticmethod
    def check_password(user_id, password):
        record = db.engine.execute(
            "SELECT password_hash FROM animal_center "
            "WHERE id ={};".format(user_id)).first()
        return check_password_hash(record.password_hash, password)


class AccessRequestDAO:
    @staticmethod
    def create_access_request(center_id):
        db.engine.execute(
            "INSERT INTO access_request (center_id) VALUES ({});".format(center_id))


class SpeciesDAO:
    @staticmethod
    def _deserialize(record, long=False):
        data = {'species_name': record[0],
                'count_of_animals': record[1]}
        if long:
            data = {'id': record[0],
                'name': record[1],
                'description': record[2],
                'price': record[3]}
        return data

    @staticmethod
    def get_species():
        records = db.engine.execute("SELECT species.name, count(animal.name) FROM species "
                                   "LEFT OUTER JOIN animal ON species.id = animal.species_id "
                                   "GROUP BY species.name")
        return [SpeciesDAO._deserialize(record) for record in records]

    @staticmethod
    def get_species_inform(id):
        record = db.engine.execute("SELECT * FROM species WHERE id = {};". format(id)).first()
        return SpeciesDAO._deserialize(record, long=True)