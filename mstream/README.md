# Mstream

mstream is a bit like spotify.
It enables you to stream your music,
but you need to host the music files yourself.

A big plus of this over spotify would be that there is no compression.
This means that the quality of your music will be what is streamed.

## Sample template

```docker-compose
---
version: "2.1"
services:
  mstream:
    image: lscr.io/linuxserver/mstream:latest
    container_name: mstream
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/London
    volumes:
      - /path/to/data:/config
      - /path/to/music:/music
    ports:
      - 3000:3000
    restart: unless-stopped
```
