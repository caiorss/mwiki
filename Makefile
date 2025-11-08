.PHONY: run 
run:
	poetry run python -m mdwiki

# Run pytest 
test:
	uv run pytest -v --tb=short 

# Generate sample static websiste by compiling the repository ./sample-wiki
gh-pages:
	uv run mwiki compile --wikipath=./sample-wiki \
		--website-name=MBook \
		--main-font=cmu-concrete \
		--title-font=chicago \
		--code-font=libertinus-mono \
		--allow-language-switch \
		--root-url=/mwiki \
		--output=./dist


# Generate sample static websiste for testing by compiling the wiki
# repository ./sample-wikki
static:
	uv run mwiki compile --wikipath=./sample-wiki \
		--website-name=MBook \
		--main-font=cmu-concrete \
		--title-font=chicago \
		--code-font=libertinus-mono \
		--allow-language-switch \
		--output=./out

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
## Javascript files
JSFILES := $(shell find ./src/ -name "*.js" -print)
## Docker config files
DOCKER_FILES := $(shell find ./docker -type f -print)
SOURCES := $(PYFILES) $(TPLFILES) $(JSFILES) $(DOCKER_FILES)


# Create the file requirements.txt, which is useful 
# for building docker images.
requirements.txt:  pyproject.toml
	uv export --format requirements-txt | sed -s 's/-e .//' > requirements.txt

docker-build.log: requirements.txt  $(SOURCES)
	docker build -f docker/mwiki.Dockerfile --tag mwiki-server . 2>&1 | tee ./docker-build.log 2>&1 | tee ./docker-build.log

podman-build.log: requirements.txt $(SOURCES)
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
