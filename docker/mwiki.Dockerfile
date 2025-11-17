FROM python:3.9.19-slim

ENV DEBIAN_FRONTEND noninteractive

# Create user and group for MWiki
RUN groupadd -r mwiki && useradd -r -g mwiki mwiki
# Set PYTHONPATH environment variable in order 
# to be able to find Python modules
ENV PYTHONPATH=/app
ENV MWIKI_PATH=/wiki
ENV PATH="$PATH:/opt"
RUN mkdir -p /app && mkdir -p /wiki  && mkdir -p /opt
COPY ./requirements.txt /app
RUN pip3 install -r /app/requirements.txt  --progress-bar=off 
COPY ./src/mwiki /app/mwiki
COPY ./LICENSE.txt  /app/
COPY ./docker/mwiki.sh  /opt/mwiki
COPY ./docker/mwiki-auth.sh   /opt/mwiki-auth
RUN  chmod +x /opt/mwiki && chmod +x /opt/mwiki-auth
WORKDIR /wiki 
##RUN pip install --upgrade pip
EXPOSE 9090


CMD ["python3", "-m", "mwiki", "server", "--wsgi", "--host=0.0.0.0", "--port=9090", "--wikipath=/wiki"]
