# Heimdall

This is a simple customisable homepage/landing page.

## Sample template

```docker-compose
---
version: "2.1"
services:
  heimdall:
    image: lscr.io/linuxserver/heimdall:latest
    container_name: heimdall
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Australia/Brisbane
    volumes:
      - /path/to/appdata/config:/config
    ports:
      - 8080:80
      - 8443:443
    restart: unless-stopped
```
