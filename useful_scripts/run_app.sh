#!/bin/bash

# This script executes flask application
source venv/bin/activate
export FLASK_ENV=development
export FLASK_APP=wsgi:app
flask run