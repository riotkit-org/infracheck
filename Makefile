.SILENT:
.PHONY: help

PIP = sudo pip3
SUDO = sudo
PY_BIN = python3
QUAY_REPO=quay.io/riotkit/infracheck
PUSH=true
SHELL=/bin/bash

help:
	@grep -E '^[a-zA-Z\-\_0-9\.@]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

all: build_package install unit_test

build_image: ## Build and push (args: PUSH, ARCH, GIT_TAG)
	set -e; DOCKER_TAG="latest-dev-${ARCH}"; \
	\
	if [[ "${GIT_TAG}" != '' ]]; then \
		DOCKER_TAG=${GIT_TAG}-${ARCH}; \
	fi; \
	\
	${SUDO} docker build . -f ./.infrastructure/${ARCH}.Dockerfile -t ${QUAY_REPO}:$${DOCKER_TAG}; \
	${SUDO} docker tag ${QUAY_REPO}:$${DOCKER_TAG} ${QUAY_REPO}:$${DOCKER_TAG}-$$(date '+%Y-%m-%d'); \
	\
	if [[ "${PUSH}" == "true" ]]; then \
		${SUDO} docker push ${QUAY_REPO}:$${DOCKER_TAG}-$$(date '+%Y-%m-%d'); \
		${SUDO} docker push ${QUAY_REPO}:$${DOCKER_TAG}; \
	fi

run_in_container: ## Run server in container (for testing)
	sudo docker kill infracheck || true
	sudo docker run --name infracheck -p 8000:8000 -t --rm quay.io/riotkit/infracheck:latest-dev-x86_64

run_standalone_server: ## Run server (standalone)
	infracheck --server --server-port 8000

run_standalone: ## Run (standalone)
	infracheck

build_package: ## Build
	${SUDO} ${PY_BIN} ./setup.py build

build_docs: ## Build documentation
	cd ./docs && make html

install: build_package ## Install as a package
	${PIP} install pipenv
	test -f ./requirements.txt || ./.infrastructure/generate-requirements-txt.py
	${SUDO} ${PIP} install -r ./requirements.txt
	${SUDO} ${PY_BIN} ./setup.py install
	which infracheck
	make clean

clean: ## Clean up the local build directory
	${SUDO} rm -rf ./build ./infracheck.egg-info

setup_venv: ## Setup virtual environment
	echo " >> Setting up virtual environment"
	${SUDO} PIPENV_IGNORE_VIRTUALENVS=1 pipenv sync -d

functional_test: setup_venv ## Run functional tests
	cd infracheck && ./functional-test.sh
	${SUDO} PIPENV_IGNORE_VIRTUALENVS=1  pipenv run ${PY_BIN} -m unittest discover -s . -p 'functional_test*.py'

unit_test: setup_venv ## Run unit tests
	${SUDO} PIPENV_IGNORE_VIRTUALENVS=1  pipenv run ${PY_BIN} -m unittest discover -s . -p 'unit_test*.py'

coverage: setup_venv ## Generate code coverage
	${SUDO} PIPENV_IGNORE_VIRTUALENVS=1 pipenv run coverage run --rcfile=.coveragerc --source . -m unittest discover -s . -p 'unit_test*.py'
