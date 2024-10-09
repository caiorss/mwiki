.PHONY: run
run:
	env WIKIBASE_PATH=./pages python -m mdwiki

.PHONY: pipenv-run
pipenv-run:
	pipenv run python -m mdwiki

# Build virtual-env with same dependencies specified
# in the Pipfile and the lockfile.
.PHONY: pipenv-install
pipenv-install:
	pipenv install 