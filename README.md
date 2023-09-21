# The Data Engineering Docker-Compose Starter Kit

This repository contains the source code for my post "The Data Engineering Docker-Compose Starter Kit".

Running this docker-compose you will get in your local environment the next services:

* RedPanda UI: localhost:8080 with precreated my-topic in it
* Mage: localhost:6789 with precreated my_project in it
* Jupyter: localhost:8888 with precreated my-notebook.ipynb
* Minio: localhost:9001 with precreated my-bucket bucket and data.csv file inside
* MySQL: localhost:3306 with precreated my_database
* Python Consumer service that should create sessions table in my_database

## How to run

Create a file for secrets

    touch .secrets

Write MYSQL_ROOT_PASSWORD=very_strong_password to it and save

Then

    docker-compose up -d --build

If you want to run only infra services without Python Consumer

    docker-compose -f docker-compose-infra-services.yml up --build

## How to do a clean restart of a docker compose

1.Stop the container(s) using the following command:

    docker-compose down

2.Delete all containers using the following command:

    docker rm -f $(docker ps -a -q)

3.Delete all volumes using the following command:

    docker volume rm $(docker volume ls -q)

4.Restart the containers using the following command:

    docker-compose up -d
