#!/bin/bash
# uncomment if not using poetry
# source ./venv/bin/activate
# sleep 2

#poetry
poetry shell
poetry install
poetry lock --no-update
source $(poetry env info --path)/bin/activate

python manage.py check
# migrate
python manage.py makemigrations
python manage.py migrate


# run
python manage.py test