"""Module which contains functions for each route."""
from app import app, models, db, utils, schemas, logger
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity


def log_request(method, request_url, center_id, entity_type, entity_id):
    """
    Function that add information to log file.
    :param method: request method.
    :param request_url: request url.
    :param center_id: id of user that send request.
    :param entity_type: type of entity that user add or change.
    :param entity_id:
    :return:
    """
    logger.info('method %s - request_url %s - center_id %s - entity_type %s - entity_id %s', method, request_url, center_id,
                entity_type, entity_id)


@app.route('/')
def index():
    return "Hello"


@app.route('/login', methods=['GET'])
def login():
    user_login = request.args.get('login')
    user_password = request.args.get('password')
    if not user_login or not user_password:
        return jsonify(message="Login and password are required"), 400
    user = models.AnimalCenter.query.filter_by(login=user_login).first()
    if not user:
        return jsonify(message="No user with such login"), 400

    access_request = models.AccessRequest(center_id=user.id)
    db.session.add(access_request)
    db.session.commit()

    if not user.check_password(user_password):
        return jsonify(message="Incorrect password"), 400
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)


@app.route('/animals', methods=['GET', 'POST'])
@utils.jwt_required_for_change
@utils.json_validate_for_change(schemas.animal_schema)
def animals():
    if request.method == 'GET':
        animals = [animal.to_dict() for animal in models.Animal.query.all()]
        return jsonify(animals)
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
        # logger = logging.getLogger("")
        # f_handler = logging.FileHandler('app.log')
        # f_handler.setLevel(logging.INFO)
        # f_format = logging.Formatter('%(asctime)s - %(message)s')
        # f_handler.setFormatter(f_format)
        # logger.addHandler(f_handler)
        # logger.info('method %s request_url %s center_id %s entity_type %s entity_id %s', request.method, request.url, user_id, 'animal', animal.id)
        return jsonify(animal.to_dict()), 201


@app.route('/animals/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@utils.jwt_required_for_change
@utils.json_validate_for_change(schemas.animal_update_schema)
def animal_inform(id):
        animal = models.Animal.query.get(id)
        if not animal:
            return jsonify(message='Not found'), 404
        if request.method == 'GET':
            return jsonify(animal.to_dict(long=True))
        if request.method == 'DELETE':
            db.session.delete(animal)
            db.session.commit()
            user_id = get_jwt_identity()
            log_request(request.method, request.url, user_id, 'animal', animal.id)
            return jsonify({'id': id})
        data = request.get_json()
        for key, value in data.items():
            setattr(animal, key, value)
        db.session.commit()
        user_id = get_jwt_identity()
        log_request(request.method, request.url, user_id, 'animal', animal.id)
        return jsonify(animal.to_dict(long=True))


@app.route('/centers', methods=['GET'])
def centers_list():
    # centers = models.AnimalCenter.query.all()
    return jsonify([center.to_dict() for center in models.AnimalCenter.query.all()])


@app.route('/centers/<int:id>', methods=['GET'])
def center_inform(id):
    center = models.AnimalCenter.query.get(id)
    if not center:
        return jsonify(message='Not found'), 404
    return jsonify(center.to_dict(long=True))


@app.route('/species', methods=['GET', 'POST'])
@utils.jwt_required_for_change
@utils.json_validate_for_change(schemas.specie_schema)
def species():
    if request.method == 'GET':
        result = db.session.query(
            models.Species.name, db.func.count(models.Animal.name))\
            .join(models.Animal, models.Species.id == models.Animal.species_id)\
            .group_by(models.Species.id).all()
        result = [{'species_name': name, 'count_of_animals': count}
                  for name, count in result]
        return jsonify(result)
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


@app.route('/species/<int:id>', methods=['GET'])
def specie_inform(id):
    species = models.Species.query.get(id)
    animals = models.Animal.query.filter_by(species_id=id).all()
    if not species:
        return jsonify('Not found'), 404
    return jsonify(species.to_dict(), [animal.to_dict() for animal in animals])


@app.route('/register', methods=['POST'])
@utils.json_validate_for_change(schemas.register_schema)
def registration():
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






