import sys
import os
import traceback
import csv
import logging
import traceback
from os import listdir
from pathlib import Path
from os.path import isfile, join
from django.conf import settings
import pandas as pd

logger = logging.getLogger("default")


class FileProcessingTool:
    ACCEPTED_EXTENSIONS: list = []
    DISALLOWED_NAMES: list = [".", "..", ".DS_Store"]

    @staticmethod
    def archive_file(file_path: str, filename: str):
        try:
            archive_dir = FileProcessingTool.get_archive_dir()
            destination_dir = join(archive_dir, filename)
            complete_file_path = join(file_path, filename)
            os.rename(complete_file_path, destination_dir)
        except Exception as err:
            traceback_str = traceback.format_exc()
            print(traceback_str)
            return False
        else:
            return True

    @staticmethod
    def get_unprocessed_files(new_files: list) -> list:
        # Fetch files from archive folder
        logger.info("Trying to make a list of archived files.")
        archived_files = listdir(FileProcessingTool.get_archive_dir())
        logger.info("There are {} archived files.".format(len(archived_files)))

        # Remove already processed files from list of to be processed files
        filename_list = list(set(new_files) - set(archived_files))
        logger.info(
            "There are {} new files to be processed.".format(len(filename_list))
        )

        filenames = []
        if filename_list:
            accepted_extensions = FileProcessingTool.ACCEPTED_EXTENSIONS
            filenames = [
                file
                for file in filename_list
                if file not in FileProcessingTool.DISALLOWED_NAMES
            ]
            filenames = [
                file
                for file in filenames
                if FileProcessingTool.get_extension(file) in accepted_extensions
            ]
        logger.info("Finally, I've got a file list: {}.".format(",".join(filenames)))
        return filenames

    @staticmethod
    def is_file_exists(_path: str) -> bool:
        _file = Path(_path)
        if not _file.is_file():
            return False
        return True

    @staticmethod
    def remove_file(_path: str):
        try:
            if FileProcessingTool.is_file_exists(_path):
                os.remove(_path)
        except:
            pass
        else:
            print(f"{_path} removed")

    @staticmethod
    def is_folder_exists(_dir: str) -> bool:
        if os.path.exists(_dir) and os.path.isdir(_dir):
            return True
        return False

    @staticmethod
    def get_extension(filename: str) -> Path:
        return Path(filename).suffix

    @staticmethod
    def get_file_name(file_path):
        return file_path.split("/")[-1]

    @staticmethod
    def get_file_path_name(file_path: str) -> str:
        directories = file_path.split("/")
        return "/".join(directories[:-1])

    @staticmethod
    def get_number_of_files_in_a_folder(dir: str) -> int:
        all_files = FileProcessingTool.scan_dir(dir)
        return len(all_files)

    @staticmethod
    def scan_dir(_dir: str):
        if not FileProcessingTool.is_folder_exists(_dir):
            print("File with path %s not found." % _dir)
            return None

        only_files = [f for f in listdir(_dir) if isfile(join(_dir, f))]
        return only_files

    @staticmethod
    def check_and_create_dir(dir_name: str, retrn_val: str = False):
        not_exists: bool = not FileProcessingTool.is_folder_exists(dir_name)
        if not_exists:
            os.makedirs(dir_name)
            print("Directory <" + dir_name + "> created")

        if retrn_val:
            return not_exists

    @staticmethod
    def check_and_create_file(file_path: str, retrn_val: bool = False):
        not_exists: bool = not FileProcessingTool.is_file_exists(file_path)
        if not_exists:
            with open(file_path, "a"):
                os.utime(file_path, None)
            print("File <" + file_path + "> created")
        if retrn_val:
            return not_exists

    @staticmethod
    def get_archive_dir() -> str:
        path: list = [settings.FILES_DIR, "ARCHIVE"]
        temp_dir: str = os.path.join(*path)
        FileProcessingTool.check_and_create_dir(temp_dir)
        return temp_dir
