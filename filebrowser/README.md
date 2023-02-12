# FileBrowser

FileBrowser is a way to be able to view and manage your files through a web based gui.
This can be useful for remote instances without a gui.
More installation details here: <https://filebrowser.org/installation>

The docker command to run is as below:

```docker
docker run \
    -v /path/to/root:/srv \
    -v /path/to/filebrowser.db:/database/filebrowser.db \
    -v /path/to/settings.json:/config/settings.json \
    -e PUID=$(id -u) \
    -e PGID=$(id -g) \
    -p 8080:80 \
    filebrowser/filebrowser:s6
```

But we'll turn that into a compose template

The default `settings.json` is below:

```json
{
  "port": 80,
  "baseURL": "",
  "address": "",
  "log": "stdout",
  "database": "/database/filebrowser.db",
  "root": "/srv"
}
```

For the `filebrowser.db`, create an empty file first if there isn't one that you have already.
