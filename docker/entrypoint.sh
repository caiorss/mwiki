#!/usr/bin/env/sh 

python3 /bin/confgen.py  /etc/Caddyfile.tpl > /etc/Caddyfile
cat /etc/Caddyfile
caddy run --config /etc/Caddyfile 