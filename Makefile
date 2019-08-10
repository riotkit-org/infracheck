.SILENT:
.PHONY: help

PIP = sudo pip3
SUDO = sudo
PY_BIN = python3

help:
	@grep -E '^[a-zA-Z\-\_0-9\.@]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

all: build_package install unit_test

build_image: ## Build docker image
	sudo docker build . -f ./.infrastructure/Dockerfile -t quay.io/riotkit/infracheck

build_image_arm: ## Build image for ARM/ARMHF
	sudo docker build -f ./.infrastructure/armhf.Dockerfile . -t wolnosciowiec/infracheck:armhf

run_in_container: ## Run (for testing)
	sudo docker kill infracheck || true
	sudo docker run --name infracheck -p 8000:8000 -t --rm wolnosciowiec/infracheck

run_standalone_server: ## Run (standalone)
	infracheck --server --server-port 8000

run_standalone: ## Run (standalone)
	infracheck

build_package: ## Build
	${SUDO} ${PY_BIN} ./setup.py build

build_docs: ## Build documentation
	cd ./docs && make html

install: build_package ## Install
	${PIP} install -r ./requirements.txt
	${SUDO} ${PY_BIN} ./setup.py install
	which infracheck
	make clean

clean: ## Clean up the local build directory
	${SUDO} rm -rf ./build ./infracheck.egg-info

unit_test: ## Run unit tests
	${PY_BIN} -m unittest discover -s ./tests

coverage: ## Generate code coverage
	coverage run --rcfile=.coveragerc --source . -m unittest discover -s ./tests
