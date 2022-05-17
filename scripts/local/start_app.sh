#!/bin/bash
APP_NAME="" # update to app_name
APP_TARGET_FOLDER="applications"
BASE_DIR=`pwd`
FULL_DIR="${BASE_DIR}/${APP_TARGET_FOLDER}/${APP_NAME}"
echo "About creating ${APP_NAME} App in ${APP_TARGET_FOLDER} Folder"
echo "Current directory is ${BASE_DIR}"
echo "Full directory is ${FULL_DIR}"
if [ ${APP_NAME} ]
then
mkdir ${FULL_DIR}
python manage.py startapp ${APP_NAME} ./${APP_TARGET_FOLDER}/${APP_NAME}
fi