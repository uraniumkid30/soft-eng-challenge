from .base import *
import secrets
import subprocess

db_name = "development_database.sqlite3"
db_path = os.path.join(DATABASE_DIR, db_name)
FileProcessingTool.check_and_create_file(db_path)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": db_path,
    }
}

DEBUG = True

SECRET_KEY:str = f"django-insecure-{secrets.token_urlsafe(50)}"

# process requirements
base_requirements:str = os.path.join(REQUIREMENTS_DIR, "base.txt")
dev_requirements:str = os.path.join(REQUIREMENTS_DIR, "development.txt")
for _file in (base_requirements, dev_requirements):
    if not FileProcessingTool.is_file_exists(_file):
        subprocess.call(f"pip freeze > {_file}", shell=True)
