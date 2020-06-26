#!/bin/bash
rm app.db &&
rm app/app.db &&
rm -r migrations &&
flask db init &&
flask db migrate &&
flask db upgrade &&
python3 create_db.py &&
flask run
