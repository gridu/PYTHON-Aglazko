#!/bin/bash

rm -r migrations
rm app.db
source env/bin/activate
export FLASK_APP=wsgi.py
flask db init
flask db migrate
flask db upgrade