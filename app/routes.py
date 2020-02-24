from app import app, models, db, utils, schemas, logger
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity


@app.after_request
def log_request(response):
    if request.method in ['POST', 'PUT', 'DELETE'] and response.status_code < 300:
        logger.info(
            '%s url=%s center_id=%s entity=%s entity_id=%s',
            request.method, request.url, get_jwt_identity(),
            request.base_url.split('/')[-1], response.json['id']
        )
    return response


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
            return jsonify({'id': id})
        data = request.get_json()
        for key, value in data.items():
            setattr(animal, key, value)
        db.session.commit()
        return jsonify(animal.to_dict(long=True))


@app.route('/centers', methods=['GET'])
def centers_list():
    centers = models.AnimalCenter.query.all()
    return jsonify([center.to_dict() for center in centers])


@app.route('/centers/<int:id>', methods=['GET'])
def center_inform():
    pass


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
        return jsonify(specie.to_dict()), 201


@app.route('/species/<int:id>', methods=['GET'])
def specie_inform():
    pass


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

    access_token = create_access_token(identity=center.id)
    return jsonify(message="Successfully registered", access_token=access_token), 201






