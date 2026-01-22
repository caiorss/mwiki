---
title:       Self-hosting deployment with podman(docker) all-in-one
label:       
description: 
keywords:    
---

## Overview

The all-in-one container provides a easy way to deploy MWiki with everything pre configured, including Mwiki server and Caddy web server in  a single docker or podman container. Caddy web server is used for serving static files and providing TLS (Transport Layer Security), also known as SSL - Socket Layer Security, by encrypting the network traffic between the server and a client web browser.

## Build the podman or docker image

Clone the repository and enter its root folder.

```sh
$ cd repository_root_folder
```

Build the container image with podman (recommended).

```sh
podman build -t mwiki  --file docker/all-in-one.Dockerfile .
```

Build the container image with docker.

```sh
docker build -t mwiki  --file docker/all-in-one.Dockerfile .
```

## Create and run the container

### Set the environment variables.

```sh
export MWIKI_WEBSISTE="https://mydomain.com"
export MWIKI_URL="https://mydomain.com"
export MWIKI_FOLDER=/home/username/wiki
```

### Create the container 

Make sure that the firewall allows network traffic through the TCP ports 80 (HTTP) and 443 (HTTPS) before running this command.

```sh
podman run --name=mwiki -it \
    --publish=80:80 \
    --publish=443:443 \
    --env=MWIKI_URL="$MWIKI_URL"  \
    --env=MWIKI_WEBSITE="$MWIKI_WEBSITE" \
    --volume=$MWIKI_FOLDER:/wiki mwiki
```

Now, the websiste will be available at 

+ `https://mydomain.com`

### Logging in 

It is possible to log in without password by using a temporary magic hyperlink using the command

```sh
$ podman exec -it mwiki mwiki-auth
Copy and paste the following URL in the web browser to authenticate.

  https://mydomain.com/auth?token=eyJ1c2VyIjogImFkbWluIiwgInNhbHQiOiAxNzQsICJleHBpcmF0aW9uIjogMTc2OTA4MDU0NiwgInNpZ25hdHVyZSI6ICIxNTVlZDYxOTRhYTE5MTNmMzhkYWMzODI3ZTJiZTdiNzdiNGQ0NzVhYzVjMmJlNDU2ZTY5ZmViNTRiOTg0OGU4In0%3D

Or paste the following token in the log in form https://mydomain.com

 eyJ1c2VyIjogImFkbWluIiwgInNhbHQiOiAxNzQsICJleHBpcmF0aW9uIjogMTc2OTA4MDU0NiwgInNpZ25hdHVyZSI6ICIxNTVlZDYxOTRhYTE5MTNmMzhkYWMzODI3ZTJiZTdiNzdiNGQ0NzVhYzVjMmJlNDU2ZTY5ZmViNTRiOTg0OGU4In0=

NOTE: This URL is only valid for 20 seconds.
NOTE: If MWiki URL is not correct, set the environment variable $MWIKI_URL to the app URL.For instance, in bash Unix shell $ export MWIKI_URL=https://mydomain.com before running this comamnd again.
```

Then, copy this url to the web browser to log in. Note that the magic login link is valid only for 20 seconds.