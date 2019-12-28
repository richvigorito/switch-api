#/bin/bash

docker stop flask-boilerplate_app_1
docker stop flask-boilerplate_db_1

docker rmi -f $(docker image ls | grep -i boiler | awk '{print $3}')

docker-compose up --build -d
