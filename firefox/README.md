# Docker Firefox

Run Firefox in a container.

## How to use

While in same directory as the `docker-compose.yml` file,
run the below to start it:

> docker-compose up -d firefox

While in the same directory, run the below to stop it:

> docker-compose down

## Follow up actions

The below can be performed if you don't wish to keep any persistant data.

| Command | Effect |
| --- | --- |
docker volume ls | List volumes
docker volume prune | Remove all unused local volumes
docker volume rm | Remove one or more volumes
