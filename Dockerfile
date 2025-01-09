FROM python:3.9.19-slim

ENV DEBIAN_FRONTEND noninteractive

# Create user and group for MWiki
RUN groupadd -r mwiki && useradd -r -g mwiki mwiki
ENV PYTHONPATH=/app
RUN mkdir -p /app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt  --progress-bar=off 
COPY src/mwiki /app/mwiki
##RUN pip install --upgrade pip
EXPOSE 9090

RUN mkdir -p /wiki
WORKDIR /wiki 

CMD ["python3", "-m", "mwiki", "server", "--wsgi", "--host=0.0.0.0", "--port=9090", "--wikipath=/wiki"]