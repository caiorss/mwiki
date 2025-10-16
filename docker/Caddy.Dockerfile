FROM alpine 

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN apk add --no-cache python3 py3-jinja2
RUN apk add caddy 

COPY ./docker/confgen.py  /bin 
COPY ./docker/entrypoint.sh  /bin 

ENTRYPOINT [ "sh", "/bin/entrypoint.sh" ]
