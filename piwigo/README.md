# piwigo

Host your own photo album and stuff.

version: '3'
services:
  piwigo:
    container_name: piwigo
    image: lscr.io/linuxserver/piwigo:latest
	environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
	volumes:
      - ./config:/config
      - /path/to/appdata/gallery:/gallery
	ports:
      - 80:80
    networks:
      - piwigo
	restart: unless-stopped

  mysql:
    container_name: piwigo_mysql
    image: mysql:8.2
    command: ["--default-authentication-plugin=mysql_native_password"]
    networks:
      - piwigo
    environment:
      MYSQL_USER: "piwigo"
      MYSQL_PASSWORD: "piwigo"
      MYSQL_DATABASE: "piwigo"
      MYSQL_RANDOM_ROOT_PASSWORD: "true"
	volumes:
	  - ./mysql:/var/lib/mysql

networks:
  piwigo:
