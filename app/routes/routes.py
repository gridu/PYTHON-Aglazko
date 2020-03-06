"""Functions that are registered as enpoints in flask application"""
from app import db, schemas, logger
from app.utils import utils
from app.models import models
from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, get_jwt_identity
from app.dao.dao_orm_models import AnimalCenterORM, AccessRequestORM, AnimalORM, SpeciesORM
from app.dao.dao_sql import AnimalCentersDaoSql, AnimalsDaoSql, SpeciesDaoSql, AccessRequestDaoSql

species_orm_obj = SpeciesORM()
animal_center_orm_obj = AnimalCenterORM()
access_request_orm_obj = AccessRequestORM()
animal_orm_obj = AnimalORM()

species_dao_sql_obj = SpeciesDaoSql()
animal_dao_sql_obj = AnimalsDaoSql()
animal_center_dao_sql_obj = AnimalCentersDaoSql()
access_request_dao_sql_obj = AccessRequestDaoSql()

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
    user = animal_center_dao_sql_obj.get_center_by_login(user_login)
    # user = animal_center_orm_obj.get_center_by_login(user_login)
    if not user:
        return jsonify(message="No user with such login"), 400

    check = animal_center_dao_sql_obj.check_password(user_password, user['id'])
    # check = animal_center_orm_obj.check_password(user_password, user['id'])
    if not check:
        return jsonify(message="Incorrect password"), 400
    access_request_dao_sql_obj.create_access_request(user['id'])
    # access_request_orm_obj.create_access_request(user['id'])
    access_token = create_access_token(identity=user['id'])
    return jsonify({'access_token': access_token})


@bp.route('/animals', methods=['GET', 'POST'])
@utils.jwt_required_for_change
@utils.json_validate_for_change(schemas.animal_schema)
def animals():
    if request.method == 'GET':
        return jsonify(animal_dao_sql_obj.get_animals())
        # return jsonify(animal_orm_obj.get_animals())
    else:
        data = request.get_json()
        user_id = get_jwt_identity()
        if not models.Species.query.get(data['species_id']):
            return jsonify(message="No such specie"), 400
        # animal = animal_orm_obj.add_animal(data, user_id)
        animal = animal_dao_sql_obj.add_animal(data, user_id)
        log_request(request.method, request.url, user_id, 'animal', animal['id'])
        return jsonify(animal), 201


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
    animal = animal_dao_sql_obj.get_animal(id)
    # animal = animal_orm_obj.get_animal(id)
    if not animal:
        return jsonify(message='Not found'), 404
    if request.method == 'GET':
        return jsonify(animal)
    if request.method == 'DELETE':
        animal_dao_sql_obj.delete_animal(id)
        # animal_orm_obj.delete_animal(id)
        user_id = get_jwt_identity()
        log_request(request.method, request.url, user_id, 'animal', id)
        return jsonify({'id': id})
    if request.method == 'PUT':
        data = request.get_json()
        animal.update(data)
        animal_dao_sql_obj.update_animal(animal)
        # animal_orm_obj.update_animal(data_upd=data, animal_id=id)
        user_id = get_jwt_identity()
        log_request(request.method, request.url, user_id, 'animal', id)
        return jsonify(animal)


@bp.route('/centers', methods=['GET'])
def centers_list():
    """
    Function that view all animal centers.
    :return: Short information about centers (id and login).
    """
    return jsonify(animal_center_dao_sql_obj.get_centers())
    # return jsonify(animal_center_orm_obj.get_centers())


@bp.route('/centers/<int:id>', methods=['GET'])
def center_inform(id):
    """
    Function that show detailed information about animal center.
    :param id: id of center that user would like to see.
    :return: Dictionary that contain detailed information about center.
    """
    center = animal_center_dao_sql_obj.get_center_inform(id)
    # center = animal_center_orm_obj.get_center_inform(id)
    if not center:
        return jsonify({'message': 'Not found'}), 404
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
        return jsonify(species_dao_sql_obj.get_species())
        # return jsonify(species_orm_obj.get_species())
    else:
        data = request.get_json()
        if models.Species.query.filter_by(name=data['name']).first():
            return jsonify(message="This species is already taken"), 400
        specie = species_dao_sql_obj.add_species(data)
        # specie = species_orm_obj.add_species(data)
        user_id = get_jwt_identity()
        log_request(request.method, request.url, user_id, 'species', specie['id'])
        return jsonify(specie), 201


@bp.route('/species/<int:id>', methods=['GET'])
def specie_inform(id):
    """
    Function that show detailed information about species.
    :param id: Id of species that user would like to see.
    :return: Information about species and list of animals of this specie.
    """
    result = species_dao_sql_obj.get_species_inform(id)
    # result = species_orm_obj.get_species_inform(id)
    if not result:
        return jsonify({'message':'Not found'}), 404
    return jsonify(result)


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
    access_request_dao_sql_obj.create_access_request(center.id)
    # access_request_orm_obj.create_access_request(center.id)

    log_request(request.method, request.url, center.id, 'animal_center', center.id)

    access_token = create_access_token(identity=center.id)
    return jsonify(message="Successfully registered", access_token=access_token), 201






