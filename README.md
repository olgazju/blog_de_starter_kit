# blog_de_test_assigment_template


say about .secrets


## How to do a clean restart of a docker compose

1.Stop the container(s) using the following command:

    docker-compose down

2.Delete all containers using the following command:

    docker rm -f $(docker ps -a -q)

3.Delete all volumes using the following command:

    docker volume rm $(docker volume ls -q)

4.Restart the containers using the following command:

    docker-compose up -d