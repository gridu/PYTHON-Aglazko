"""Module which contains functions for each route."""
from app import models, db, utils, schemas, logger, dao
from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, get_jwt_identity

bp = Blueprint("app", __name__)


def log_request(method, request_url, center_id, entity_type, entity_id):
    """
    Function that add information to log file.
    :param method: request method.
    :param request_url: request url.
    :param center_id: id of user that send request.
    :param entity_type: type of entity that user add or change.
    :param entity_id: id of entity that we add/delete/modify.
    :return:
    """
    logger.info('method %s - request_url %s - center_id %s - entity_type %s - entity_id %s', method, request_url, center_id,
                entity_type, entity_id)


@bp.route('/')
def index():
    return "Hello"


@bp.route('/login', methods=['GET'])
def login():
    """
    Function for authorization.
    :return:If password incorrect function will return "Incorrect password".
            if password was correct function will return access token.
    """
    user_login = request.args.get('login')
    user_password = request.args.get('password')
    if not user_login or not user_password:
        return jsonify(message="Login and password are required"), 400
    user = dao.AnimalCentersDAO.get_center_by_login(user_login)
    if not user:
        return jsonify(message="No user with such login"), 400
    dao.AccessRequestDAO.create_access_request(user['id'])

    if not dao.AnimalCentersDAO.check_password(user['id'], user_password):
        return jsonify(message="Incorrect password"), 400
    access_token = create_access_token(identity=user['id'])
    return jsonify({'access_token': access_token})


@bp.route('/animals', methods=['GET', 'POST'])
@utils.jwt_required_for_change
@utils.json_validate_for_change(schemas.animal_schema)
def animals():
    if request.method == 'GET':
        return jsonify(dao.AnimalsDAO.get_animals())
    else:
        data = request.get_json()
        user_id = get_jwt_identity()
        if not models.Species.query.get(data['species_id']):
            return jsonify(message="No such specie"), 400
        animal = models.Animal(name=data['name'], center_id=user_id,
                               description=data['description'], price=data['price'],
                               species_id=data['species_id'], age=data['age'])
        db.session.add(animal)
        db.session.commit()
        log_request(request.method, request.url, user_id, 'animal', animal.id)
        return jsonify(animal.to_dict()), 201


@bp.route('/animals/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@utils.jwt_required_for_change
@utils.json_validate_for_change(schemas.animal_update_schema)
def animal_inform(id):
    """
    Function that view detailed information about one animal
    :param id: id of animal that we would like to see.
    :return: If there is no animal with such id, function will return "Not found", 404.
             If request method GET function will return detailed information about animal.
             If request method DELETE function will return id of animal that was deleted.
             If request method PUT function will change param that give user and return detailed information about animal.
    """
    animal = dao.AnimalsDAO.get_animal(id)
    if not animal:
        return jsonify(message='Not found'), 404
    if request.method == 'GET':
        return jsonify(animal)
    if request.method == 'DELETE':
        dao.AnimalsDAO.delete_animal(id)
        user_id = get_jwt_identity()
        log_request(request.method, request.url, user_id, 'animal', id)
        return jsonify({'id': id})
    data = request.get_json()
    animal.update(data)
    dao.AnimalsDAO.update_animal(animal)
    user_id = get_jwt_identity()
    log_request(request.method, request.url, user_id, 'animal', id)
    return jsonify(animal)


@bp.route('/centers', methods=['GET'])
def centers_list():
    """
    Function that view all animal centers.
    :return: Short information about centers (id and login).
    """
    # return jsonify([center.deserialize() for center in models.AnimalCenter.query.all()])
    return jsonify(dao.AnimalCentersDAO().get_centers())


@bp.route('/centers/<int:id>', methods=['GET'])
def center_inform(id):
    """
    Function that show detailed information about animal center.
    :param id: id of center that user would like to see.
    :return: Dictionary that contain detailed information about center.
    """
    center = dao.AnimalCentersDAO.get_center_inform(id)
    if not center:
        return jsonify(message='Not found'), 404
    return jsonify(center)


@bp.route('/species', methods=['GET', 'POST'])
@utils.jwt_required_for_change
@utils.json_validate_for_change(schemas.specie_schema)
def species():
    """
    Function that show list of species and count of animals that have this species.
    Also function can add new species.
    :return: If method GET, function will return list of dictionaries that contain species name and count of animals,
             that have these species.
             If method POST,function will return detailed information about species.
    """
    if request.method == 'GET':
        # result = db.session.query(
        #     models.Species.name, db.func.count(models.Animal.name))\
        #     .join(models.Animal, models.Species.id == models.Animal.species_id)\
        #     .group_by(models.Species.id).all()
        # result = [{'species_name': name, 'count_of_animals': count}
        #           for name, count in result]
        return jsonify(dao.SpeciesDAO.get_species())
    else:
        data = request.get_json()
        if models.Species.query.filter_by(name=data['name']).first():
            return jsonify(message="This species is already taken"), 400
        specie = models.Species(name=data['name'], description=data['description'],
                                price=data['price'])
        db.session.add(specie)
        db.session.commit()
        user_id = get_jwt_identity()
        log_request(request.method, request.url, user_id, 'species', specie.id)
        return jsonify(specie.to_dict()), 201


@bp.route('/species/<int:id>', methods=['GET'])
def specie_inform(id):
    """
    Function that show detailed information about species.
    :param id: Id of species that user would like to see.
    :return: Information about species and list of animals of this specie.
    """
    species = models.Species.query.get(id)
    animals = models.Animal.query.filter_by(species_id=id).all()
    if not species:
        return jsonify('Not found'), 404
    return jsonify(species.to_dict(), [animal.to_dict() for animal in animals])


@bp.route('/register', methods=['POST'])
@utils.json_validate_for_change(schemas.register_schema)
def registration():
    """
    Function that register user.
    :return: If user name is already taken function will return "This user name is already taken".
             If registration was successfully function will return "Successfully registered" and access token.
    """
    data = request.get_json()
    if models.AnimalCenter.query.filter_by(login=data['login']).first():
        return jsonify(message="This user name is already taken"), 400
    center = models.AnimalCenter(login=data['login'], address=data['address'])
    center.set_password(data['password'])
    db.session.add(center)
    db.session.commit()
    access_request = models.AccessRequest(center_id=center.id)
    db.session.add(access_request)
    db.session.commit()

    log_request(request.method, request.url, center.id, 'animal_center', center.id)

    access_token = create_access_token(identity=center.id)
    return jsonify(message="Successfully registered", access_token=access_token), 201






