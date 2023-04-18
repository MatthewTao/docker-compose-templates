# docker-compose-templates

Collection of docker compose templates that might help self hosting some useful tools.

Here's an interesting repo with a good list of things that can be hosted:
<https://github.com/petersem/dockerholics>

## Ports used

If you are leaving the ports unmodified,
these are the ports that are in use by the services listed here:

| Service | Port |
| --- | --- |
| bookstack | 6875|
| firefox | 3000 |
| freshrss | 8082 |
| grocy | 9283 |
| heimdall | 8080, 8443|
| syncthing | 8384 |
| yacht | 8001 |
| wikijs | 6885 |

## Quick docker compose guide

Here are some of the frequently used commands when using docker compose:

| Command | Effect |
| --- | --- |
| docker compose pull | Attempt to pull the associated image |
| docker compose up | Builds, (re)creates, starts, and attaches to containers for a service|
| docker compose down | Stops containers and removes containers, networks, volumes, and images created by up. |
| docker compose stop | Stops running containers without removing them.|
| docker compose start | Starts existing containers for a service.|
