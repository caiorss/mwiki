---
title:       Self-hosting deployment with podman(docker) all-in-one
label:       
description: 
keywords:    
---

## Overview

Linux containers can be thought as lightweight disposable virtual machine since they provide a way to virtualize software with less resource usage than full-featured virtual machines as containers share the same kernel and are based on process isolation rather than hardware emulation. By using containers, server software, including MWiki can be deployed isolated from the host machine in a secure fashion without causing disruptions or breaking changes. Moreover, as containers are sandboxed by default, they are able to mitigate and limit the reach of security vulnerabilities in the host machine if any container is ever compromised.

The all-in-one container provides an easy and lightweight approach to deploy MWiki with everything pre configured, including Mwiki server and Caddy web server in  a single docker or podman container. Caddy web server is used for serving static files and providing TLS (Transport Layer Security), also known as SSL - Socket Layer Security, by encrypting the network traffic between the server and a client web browser.
##  Installation

### Disable SELinux

Since SELinux may cause podman to fail with the error `[Errno 13] Permission denied: ...`, it may be worth to disable SELinux by using

```sh
sudo setenforce 0 
```

for temporarily disabling SELinux.

**See**

+ *Security-Enhanced Linux*, Wikipedia
  + https://en.wikipedia.org/wiki/Security-Enhanced_Linux
+ *How to Disable SELinux on Fedora 40 or 39*
  + https://linuxcapable.com/how-to-disable-selinux-on-fedora-linux/
+ *How to Disable SELinux Temporarily or Permanently*
  + https://www.tecmint.com/disable-selinux-in-centos-rhel-fedora/
+ *How to disable SELinux (with and without reboot)*
  + https://www.golinuxcloud.com/disable-selinux/
+ *Changing SELinux States and Modes*
  + https://docs.fedoraproject.org/en-US/quick-docs/selinux-changing-states-and-modes/


### Build the Podman Container Image

Clone the repository and enter its root folder.

```sh
git clone https://github.com/caiorss/mwiki && cd mwiki
```

Build the container image using podman (recommended).

```sh
podman build -t mwiki  --file docker/all-in-one.Dockerfile .
```

Build the container image using docker.

```sh
docker build -t mwiki  --file docker/all-in-one.Dockerfile .
```

   

### Set the environment variables.

```sh
export MWIKI_WEBSISTE="https://mydomain.com"
export MWIKI_URL="https://mydomain.com"
export MWIKI_FOLDER=/home/username/wiki
```

If the websiste is not public use

```sh
export MWIKI_PUBLIC=false
```

If the website is public (anyone can view), set the environment variable MWIKI_PUBLIC to true. The default value of this setting is false.

```sh
export MWIKI_PUBLIC=true
```

Set the Wiki name (website name).

```sh
export MWIKI_SITENAME=MBook
```

### Open TCP Ports - Firewall

Make sure that the firewall allows network traffic through the TCP ports 80 (HTTP) and 443 (HTTPS) before running this command.

### Create the container 

This step creates podman container, which is equivalent to a lightweight virtual machine, detached from the terminal.

```sh
podman run --name=mwiki --detach  \
    --publish=80:80 --publish=443:443  \
    --env MWIKI_URL=$MWIKI_URL \
    --env=MWIKI_SITENAME=$MWIKI_SITENAME \
    --env=MWIKI_PUBLIC=$MWIKI_PUBLIC \
    --env MWIKI_WEBSITE="$MWIKI_WEBSITE" \
    --volume $MWIKI_FOLDER:/wiki mwiki
```

Now, the website will be available at 

+ `https://mydomain.com`
 

To deploy on local host set the website environment variable to 

```sh
export MWIKI_WEBSITE="localhost http://[MACHINE-HOSTNAME].local"
```

The machine hostname can be obtained using the commmand $ hostname on Windows, Linux and other Unix-like operating systems.

```sh
$ hostname
dummy
```

So, the url of this dummy machine on the local network would be 

+ `http://dummy.local`
   

### Logging in / Authentication

It is possible to log in without password by using a temporary magic hyperlink using the command

```sh
podman exec -it mwiki mwiki-auth
```

Output:

```
Copy and paste the following URL in the web browser to authenticate.

  https://mydomain.com/auth?token=eyJ1c2VyIjogImFkbWluIiwgInNhbHQiOiAxNzQsICJleHBpcmF0aW9uIjogMTc2OTA4MDU0NiwgInNpZ25hdHVyZSI6ICIxNTVlZDYxOTRhYTE5MTNmMzhkYWMzODI3ZTJiZTdiNzdiNGQ0NzVhYzVjMmJlNDU2ZTY5ZmViNTRiOTg0OGU4In0%3D

Or paste the following token in the log in form https://mydomain.com

 eyJ1c2VyIjogImFkbWluIiwgInNhbHQiOiAxNzQsICJleHBpcmF0aW9uIjogMTc2OTA4MDU0NiwgInNpZ25hdHVyZSI6ICIxNTVlZDYxOTRhYTE5MTNmMzhkYWMzODI3ZTJiZTdiNzdiNGQ0NzVhYzVjMmJlNDU2ZTY5ZmViNTRiOTg0OGU4In0=

NOTE: This URL is only valid for 20 seconds.
NOTE: If MWiki URL is not correct, set the environment variable $MWIKI_URL to the app URL.For instance, in bash Unix shell $ export MWIKI_URL=https://mydomain.com before running this comamnd again.
```

Then, copy this url to the web browser to log in. Note that the magic login link is valid only for 20 seconds. After this step, the user can set the administrator password. MWiki does not use a hardcoded default password, instead it generates a random default password for every wiki.
### Common Operations

The previous command for creating the container needs to be run only once. After the last step, the following commands can be used for managing the container.

View the MWiki container's logs:

```sh
podman logs --tail=50 -f mwiki
```

Stop the MWiki container:

```sh
podman stop mwiki
```

Start the MWiki container:

```sh
podman start mwiki
```

Delete MWiki container^[Note that this command is not prone to data loss if the wiki repository is mounted to the container folder /wiki]:

```sh
podman rm mwiki
```

## Further Reading

+ *Podman Documentation*, podman docs
  + https://docs.podman.io/en/latest/
+ *Podman Desktop - Containers and Kubernetes | Podman Desktop*, Podman Desktop
  + https://podman-desktop.io/
+ *How to Debug Permission Denied Errors in Podman Containers*, oneuptime (2026)
  + https://oneuptime.com/blog/post/2026-03-16-debug-permission-denied-errors-podman/view
+ *Container permission denied: How to diagnose this error*, Dan Walsh (2022) - Redhat
  + https://www.redhat.com/en/blog/container-permission-denied-errors
+ *I built a silent home server using an Intel N100 mini PC—here’s how it went*, Jeff Butts (2025) - XDA Developers
  + https://www.xda-developers.com/built-silent-home-server-using-intel-n100-mini-pc/
+ *Begin Your Homelab Journey: Self-Hosting Apps on a Mini PC with Proxmox*, SikuSiku
  + https://sikusiku.com/2025/09/begin-your-homelab-journey-self-hosting-apps-on-a-mini-pc-with-proxmox/
+ *I installed these 6 lightweight Linux tools on a cheap mini PC and turned it into a silent home server*, Afam Onymadu (2026) - makeuseof
  + https://www.makeuseof.com/installed-lightweight-linux-tools-mini-pc-turned-into-silent-home-server/