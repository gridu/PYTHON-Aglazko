# About application
This application is REST API for animal sales web site.

#### Project Structure
```
├── app
│   ├── dao_models.py
│   ├── dao.py
│   ├── __init__.py
│   ├── interfaces.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   └── utils.py
├── app.db
├── app.log
├── config.ini
├── config.py
├── fill_db.py
├── README.md
├── requirements.txt
├── tests
│   ├── conftest.py
│   ├── __init__.py
│   └── test_api.py
├── useful_scripts
│   ├── init_venv.sh
│   ├── reinit_db.sh
│   ├── run_app.sh
│   └── run_tests.sh
└── wsgi.py
```
- `app` - main application folder, where source code lives
- `dao_models.py` - dao classes which uses orm
- `dao.py` - dao classes which uses plain SQL
- `__init__.py` - flask plugins and logging initialization 
- `interfaces.py` - dao interfaces
- `main.py` - factory method that builds applications
- `models.py` - orm models
- `routes.py` - functions that are registered as endpoints
- `schemas.py` - json validation schemas
- `utils.py` - useful decorators
- `app.db` - application database
- `app.log` - application log
- `config.ini` - configuration file
- `config.py` - application configuration object
- `fill_db.py` - script that fills db with default values
- `README.md` - some useful information
- `requirements.txt` - project dependencies
- `tests` - test directory
- `conftest.py` - pytest fixtures
- `test_api.py` - api tests
- `useful_scripts` - folders with useful scripts to setup env and run app
- `init_venv.sh` - create virtualenv and install dependencies
- `reinit_db.sh` - recreate database and migrations + fill db with default values
- `run_app.sh` - run application
- `run_tests.sh` - run tests
- `wsgi.py` - main application entrypoint

#### Authentication
Authentication is required for `POST`, `PUT` and `DELETE` requests.\
Authentication type is jwt.\
To be able to run `POST`, `PUT` or `DELETE` request, you have to set up
header `Authorization: Bearer <your_token>`

# How to 
#### Run application
1. Run `./useful_scripts/init_venv.sh` to create virtualenv 
and install all requirements.
2. Run `./useful_scripts/reinit_db.sh` to create sqlite database and fill it 
with default values
3. Run `.useful_scripts/run_app.sh` to run application

#### Run tests
1. Run first step from [Run application](#run-application)
2. Run `./useful_scripts/run_tests.sh`

#### Make requests to application
##### Setup request env
1. Run application
2. create virtualenv `virtualenv -p python3 httpi`
3. Run `source httpi/bin/activate`
4. Run `pip install httpie httpie-jwt-auth`

##### Make requests
First, `httpie` virtualenv should be sourced. \
httpie uses `=` for string values, and `:=` for int, number etc\
`--auth-type=jwt` and `auth=$TOKEN`shoud be used with all `POST`, `PUT` and `DELETE` requests.\
Token can be obtained via `httpie GET localhost:5000/login?login=<your_login>&password=<your_password>`
and then can be saved as `export TOKEN=<access_token>` \
Now you can perform requests like:
- `httpie GET localhost:5000/animals`
- `httpie GET localhost:5000/login?login=<your_login>&password=<your_password>`
- `httpie POST localhost:5000/register login=<your_login> password=<your_password> address=<your_address>`
- `httpie POST localhost:5000/animals name=<animal_name> age:=<age> species_id:=<sp_id>`

[Screenshot of tests](test_screenshot.png)