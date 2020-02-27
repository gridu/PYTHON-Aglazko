"""This module contain schemas for each kind of objects that used in project."""
specie_schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'price': {'type': 'number'}
    },
    'required': ['name', 'description', 'price']
}

register_schema = {
    'type': 'object',
    'properties': {
        'login': {'type': 'string'},
        'password': {'type': 'string'},
        'address': {'type': 'string'}
    },
    'required': ['login', 'password', 'address']
}

animal_schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'age': {'type': 'integer'},
        'species_id': {'type': 'integer'},
        'price': {'type': 'number'}
    },
    'required': ['name', 'age', 'species_id']
}

animal_update_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'age': {'type': 'integer'},
        'species_id': {'type': 'integer'},
        'price': {'type': 'number'}
    },
    'required': []
}