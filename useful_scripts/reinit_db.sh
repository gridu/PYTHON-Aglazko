#!/bin/bash

# This script performs db clean and then initializes it and fills with predifined values
rm -r migrations
rm app.db
export FLASK_APP=wsgi.py
flask db init
flask db migrate
flask db upgrade
python fill_db.py