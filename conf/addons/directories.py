import os
from pathlib import Path
from services.file_manager.utils import FileProcessingTool

# Build paths inside the project like this: BASE_DIR / 'subdir'.
SETTINGS_DIR = Path(__file__).resolve().parent  # settings dir
PROJECT_DIR = Path(__file__).resolve().parent.parent  # project conf dir
ROOT_DIR = Path(__file__).resolve().parent.parent.parent  # dir housing conf dir

DATABASE_DIR = os.path.join(PROJECT_DIR, "databases")
LOGS_DIR = os.path.join(ROOT_DIR, "logs")
FILES_DIR = os.path.join(ROOT_DIR, "files")
THEME_DIR = os.path.join(ROOT_DIR, "themes")
ARCHIVE_DIR = os.path.join(FILES_DIR, "ARCHIVE")
NEWFILES_DIR = os.path.join(FILES_DIR, "NEW_FILES")
REQUIREMENTS_DIR = os.path.join(ROOT_DIR, "requirements")


def create_neccessary_directories():
    directory_list = [
        DATABASE_DIR,
        LOGS_DIR,
        FILES_DIR,
        ARCHIVE_DIR,
        NEWFILES_DIR,
        REQUIREMENTS_DIR,
        os.path.join(THEME_DIR, "templates"),
        os.path.join(THEME_DIR, "static", "css"),
        os.path.join(THEME_DIR, "static", "js"),
        os.path.join(THEME_DIR, "static", "img"),
    ]
    for _dir in directory_list:
        FileProcessingTool.check_and_create_dir(_dir)


create_neccessary_directories()
