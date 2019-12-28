#/bin/bash

docker stop -rm -f flask-boilerplate_app_1
docker stop -rm -f flask-boilerplate_db_1

docker rmi -f $(docker image ls | grep -i boiler | awk '{print $3}')

docker-compose down -v
docker-compose build --no-cache
docker-compose up -d 
