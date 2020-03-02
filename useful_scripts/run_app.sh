#!/bin/bash

export FLASK_ENV=development
export FLASK_APP=wsgi:app
flask run