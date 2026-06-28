FROM docker.io/python:3.13-slim

ENV DEBIAN_FRONTEND noninteractive

# Create user and group for MWiki
RUN groupadd -r mwiki && useradd -r -g mwiki mwiki
# Set PYTHONPATH environment variable in order 
# to be able to find Python modules
ENV PYTHONPATH=/app
ENV MWIKI_PATH=/wiki
ENV PATH="$PATH:/opt"
ENV MWIKI_WEBSITE=http://localhost
RUN mkdir -p /app && mkdir -p /wiki  && mkdir -p /opt
RUN apt-get update && apt-get install -y curl libnss3-tools

COPY ./requirements.txt /app
RUN pip3 install -r /app/requirements.txt  --progress-bar=off && pip install jinja2

COPY ./src/mwiki /app/mwiki
COPY ./LICENSE.txt  /app/
COPY ./docker/mwiki.sh  /opt/mwiki
COPY ./docker/mwiki-auth.sh   /opt/mwiki-auth
RUN  chmod +x /opt/mwiki && chmod +x /opt/mwiki-auth

WORKDIR /root 
RUN curl -L  -o caddy.tar.gz https://github.com/caddyserver/caddy/releases/download/v2.10.2/caddy_2.10.2_linux_amd64.tar.gz \
  &&  tar -xvzf caddy.tar.gz \
  &&  rm -rf caddy.tar.gz    \
  &&  chmod +x caddy \
  &&  mv caddy /usr/bin/


WORKDIR /wiki 

COPY ./docker/confgen.py     /bin 
COPY ./docker/entrypoint.sh  /bin 
COPY ./docker/Caddyfile_.j2   /etc/


##RUN pip install --upgrade pip
EXPOSE 80
EXPOSE 443
EXPOSE 2019

ENV MWIKI_X_ACCEL_REDIRECT=true
ENV MWIKI_WEBSITE="http://localhost"
ENV MWIKI_URL="http://localhost"
ENV ROOT_CRT="/root/.local/share/caddy/pki/authorities/lab/root.crt" 

# Persist caddy server's data
VOLUME /root/.config/caddy 
VOLUME /root/.local/share/caddy

RUN cat <<EOF > /bin/entrypoint.sh 
#!/usr/bin/env sh
python3 /bin/confgen.py  /etc/Caddyfile_.j2 > /etc/Caddyfile
cat /etc/Caddyfile
caddy run --config /etc/Caddyfile &

# Check whether the execution of somecommand 
# was successful
if [ $? -ne 0 ]
then
  echo "An error happened. Terminate"
  exit 1
fi

sleep 10
echo "Copy ROOT CRT = $ROOT_CRT"

if [ -f $ROOT_CRT ]
then
  cp -v "$ROOT_CRT" /app/mwiki/static/
fi

echo "Starting mwiki server ... wait"
python3 -m mwiki server --wsgi --host=0.0.0.0 --port=9090 --wikipath=/wiki 
EOF


ENTRYPOINT [ "sh", "/bin/entrypoint.sh" ]
