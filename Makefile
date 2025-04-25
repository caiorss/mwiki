.PHONY: run 
run:
	poetry run python -m mdwiki

# Build Docker container image 
docker: docker-build.log 

# Build Podman container image
podman: podman-build.log

# Build virtual-env with same dependencies specified
# in the Pipfile and the lockfile.
.PHONY: poetry 
poetry:
	poetry install 


.PHONY: vscode 
vscode:
	cp -v .vscode/settings.json .vscode/settings.json.back
	cp -v .vscode/launch.json .vscode/launch.json.back
	python3 vscode.py


# Install package using pipx tool 
# Install pipx first $ pip install pipx
.PHONY: install 
install:
	pipx install . --force


## All Python files
PYFILES := $(shell find ./src/ -name "*.py" -print)
## All template files
TPLFILES := $(shell find ./src/ -name "*.html" -print)

# Create the file requirements.txt, which is useful 
# for building docker images.
requirements.txt:  pyproject.toml
	poetry export --output requirements.txt

docker-build.log: requirements.txt $(PYFILES) $(TPLFILES) docker/mwiki.Dockerfile 
	docker build -f docker/mwiki.Dockerfile --tag mwiki-server . 2>&1 | tee ./docker-build.log 2>&1 | tee ./docker-build.log

podman-build.log: requirements.txt $(PYFILES) $(TPLFILES) docker/mwiki.Dockerfile 
	podman build -f docker/mwiki.Dockerfile --tag mwiki-server . 2>&1 | tee ./docker-build.log 2>&1 | tee ./podman-build.log

requirements: requirements.txt 

.PHONY: clean 
clean:
	rm -rf -v ./mdwiki.egg-info 
	rm -rf -v build 
	rm -rf -v dist 
	rm -rf -v flask_session 


.PHONY: build 
build: 
	poetry build 


# Build a deployable .pex archive (Similar to Java's JAR files)
# Requires installing PEX 
# $ pip install pex
.PHONY: pex 
pex:
	pex . -e mwiki.cli:main -o mwiki.pex

.PHONY: install clean run vscode 