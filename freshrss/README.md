# FreshRSS

It is a self hosted RSS feed aggregator.
It includes a web based reader to access the feeds.

## Sample template

```docker-compose
---
version: "2.1"
services:
  freshrss:
    image: lscr.io/linuxserver/freshrss:latest
    container_name: freshrss
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/London
    volumes:
      - /path/to/data:/config
    ports:
      - 80:80
    restart: unless-stopped
```
