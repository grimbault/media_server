Media-Server
===

This is a media server tool allowing you to download film and series thanks to several tools:

- Radarr: Select movies to download ([Github](https://github.com/Radarr/Radarr))
- Sonarr: Select series to downloads ([Github](https://github.com/Sonarr/Sonarr))
- Bazarr: Download subtitles ([Github](https://github.com/morpheus65535/bazarr))
- Jackett : Parse torrenting sites to find your media ([Github](https://github.com/Jackett/Jackett))
- Deluge : Torrent client ([Github](https://github.com/deluge-torrent/deluge))
- Jellyfin : Media server itself (allow you to stream your media on your device) ([Github](https://github.com/jellyfin/jellyfin))

All these tools are free & open-source

Requirements
===

```
ansible
docker or podman
docker-compose or podman-compose
```

I use a raspberry pi 3 to make this work

Configuration
===

There is some configuration in the file .env like :
- The time zone
- The PUID & PGID ($> id $USER)
- The root folder
- The version of the containers

    * Radarr : [hub.docker.com/r/linuxserver/radarr](hub.docker.com/r/linuxserver/radarr)
    * Sonarr : [hub.docker.com/r/linuxserver/sonarr](hub.docker.com/r/linuxserver/sonarr)
    * Bazarr : [hub.docker.com/r/linuxserver/bazarr](hub.docker.com/r/linuxserver/bazarr)
    * Jackett : [hub.docker.com/r/linuxserver/jackett](hub.docker.com/r/linuxserver/jackett)
    * Deluge : [hub.docker.com/r/linuxserver/deluge](hub.docker.com/r/linuxserver/deluge)
    * Jellyfin : [hub.docker.com/r/jellyfin/jellyfin](hub.docker.com/r/jellyfin/jellyfin)

You need to create a file named credentials.ini in the same folder than the main.py.
In this file must be stored all your credentials for sutitles providers of for private/semi-private trackers.

There is a sample of credentials.ini :

```ini
[OPENSUBTITLES]
Username=<your username>
Password=<your password>

[YOUR TRACKER]
Username=<your username>
Password=<your password>
```

How to use
===

By default the host name is : mediaserver

```sh
ansible-playbook media-server.yaml

# wait a while while the server are starting

python3 main.py
```

Then you have to go on the deluge interface the enable it. By default the password is 'deluge'.

There are the ports for the web interfaces :

- Radarr: 7878
- Sonarr: 8989
- Bazarr: 6767
- Jackett : 9117
- Deluge : 8112
- Jellyfin : 8096

TODO
===

Work on the paths
