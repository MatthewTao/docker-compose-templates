# Rdesktop

Can host environments in a docker container and remote desktop into them.

## Sample template

```docker-compose
---
version: "2.1"
services:
  rdesktop:
    image: lscr.io/linuxserver/rdesktop:latest
    container_name: rdesktop
    security_opt:
      - seccomp:unconfined #optional
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/London
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock #optional
      - /path/to/data:/config #optional
    ports:
      - 3389:3389
    devices:
      - /dev/dri:/dev/dri #optional
    shm_size: "1gb" #optional
    restart: unless-stopped
```
