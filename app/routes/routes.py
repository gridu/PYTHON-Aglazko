"""Functions that are registered as enpoints in flask application"""
from app.utils import decorators, schemas, log
from flask import request, jsonify, Blueprint, current_app
from flask_jwt_extended import create_access_token, get_jwt_identity
from app.dao import dao

bp = Blueprint("app", __name__)


@bp.after_request
def add_dao_header(response):
    response.headers['DAO_TYPE'] = 'SQL' if current_app.config['DAO_SQL'] else "ORM"
    return response


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
    user = dao.AnimalCenterDAO.get_center_by_login(user_login)
    if not user:
        return jsonify(message="No user with such login"), 400

    check = dao.AnimalCenterDAO.check_password(user_password, user['id'])
    if not check:
        return jsonify(message="Incorrect password"), 400
    dao.AccessRequestDAO.create_access_request(user['id'])
    access_token = create_access_token(identity=user['id'])
    return jsonify({'access_token': access_token})


@bp.route('/animals', methods=['GET', 'POST'])
@decorators.jwt_required_for_change
@decorators.json_validate_for_change(schemas.animal_schema)
def animals():
    if request.method == 'GET':
        return jsonify(dao.AnimalDAO.get_animals())
    else:
        data = request.get_json()
        user_id = get_jwt_identity()
        if not dao.SpeciesDAO.get_species_inform(data['species_id']):
            return jsonify(message="No such specie"), 400
        animal = dao.AnimalDAO.add_animal(data, user_id)
        log.log_request(request.method, request.url, user_id, 'animal', animal['id'])
        return jsonify(animal), 201


@bp.route('/animals/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@decorators.jwt_required_for_change
@decorators.json_validate_for_change(schemas.animal_update_schema)
def animal_inform(id):
    """
    Function that view detailed information about one animal
    :param id: id of animal that we would like to see.
    :return: If there is no animal with such id, function will return "Not found", 404.
             If request method GET function will return detailed information about animal.
             If request method DELETE function will return id of animal that was deleted.
             If request method PUT function will change param that give user and return detailed information about animal.
    """
    animal = dao.AnimalDAO.get_animal(id)
    if not animal:
        return jsonify(message='Not found'), 404
    if request.method == 'GET':
        return jsonify(animal)
    if request.method == 'DELETE':
        dao.AnimalDAO.delete_animal(id)
        user_id = get_jwt_identity()
        log.log_request(request.method, request.url, user_id, 'animal', id)
        return jsonify({'id': id})
    if request.method == 'PUT':
        data = request.get_json()
        animal.update(data)
        dao.AnimalDAO.update_animal(animal)
        user_id = get_jwt_identity()
        log.log_request(request.method, request.url, user_id, 'animal', id)
        return jsonify(animal)


@bp.route('/centers', methods=['GET'])
def centers_list():
    """
    Function that view all animal centers.
    :return: Short information about centers (id and login).
    """
    return jsonify(dao.AnimalCenterDAO.get_centers())


@bp.route('/centers/<int:id>', methods=['GET'])
def center_inform(id):
    """
    Function that show detailed information about animal center.
    :param id: id of center that user would like to see.
    :return: Dictionary that contain detailed information about center.
    """
    center = dao.AnimalCenterDAO.get_center_inform(id)
    if not center:
        return jsonify({'message': 'Not found'}), 404
    return jsonify(center)


@bp.route('/species', methods=['GET', 'POST'])
@decorators.jwt_required_for_change
@decorators.json_validate_for_change(schemas.specie_schema)
def species():
    """
    Function that show list of species and count of animals that have this species.
    Also function can add new species.
    :return: If method GET, function will return list of dictionaries that contain species name and count of animals,
             that have these species.
             If method POST,function will return detailed information about species.
    """
    if request.method == 'GET':
        return jsonify(dao.SpeciesDAO.get_species())
    else:
        data = request.get_json()
        if dao.SpeciesDAO.get_species_by_name(data['name']):
            return jsonify(message="This species is already taken"), 400
        specie = dao.SpeciesDAO.add_species(data)
        user_id = get_jwt_identity()
        log.log_request(request.method, request.url, user_id, 'species', specie['id'])
        return jsonify(specie), 201


@bp.route('/species/<int:id>', methods=['GET'])
def specie_inform(id):
    """
    Function that show detailed information about species.
    :param id: Id of species that user would like to see.
    :return: Information about species and list of animals of this specie.
    """
    result = dao.SpeciesDAO.get_species_inform(id)
    if not result:
        return jsonify({'message':'Not found'}), 404
    return jsonify(result)


@bp.route('/register', methods=['POST'])
@decorators.json_validate_for_change(schemas.register_schema)
def registration():
    """
    Function that register user.
    :return: If user name is already taken function will return "This user name is already taken".
             If registration was successfully function will return "Successfully registered" and access token.
    """
    data = request.get_json()
    if dao.AnimalCenterDAO.get_center_by_login(data['login']):
        return jsonify(message="This user name is already taken"), 400
    center_id = dao.AnimalCenterDAO.add_center(data)

    dao.AccessRequestDAO.create_access_request(center_id)

    log.log_request(request.method, request.url, center_id, 'animal_center', center_id)

    access_token = create_access_token(identity=center_id)
    return jsonify({'message': "Successfully registered",
                    'access_token': access_token}), 201
