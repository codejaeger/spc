#!/bin/bash
source vvenv/bin/activate
cd spc
python3 manage.py makemigrations usrs
python3 manage.py migrate
python3 manage.py runserver
