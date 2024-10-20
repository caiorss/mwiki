.PHONY: run 
run
	poetry run python -m mdwiki

# Build virtual-env with same dependencies specified
# in the Pipfile and the lockfile.
.PHONY: poetry-install
pipenv-install:
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


.PHONY: clean 
clean:
	rm -rf -v ./mdwiki.egg-info 
	rm -rf -v build 
	rm -rf -v dist 
	rm -rf -v flask_session 


.PHONY: build 
build: 
	poetry build 

.PHONY: install clean run vscode 