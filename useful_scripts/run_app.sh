#!/bin/bash

# This script executes flask application
export FLASK_ENV=development
export FLASK_APP=wsgi:app
flask run