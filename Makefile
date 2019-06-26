.SILENT:

## Colors
COLOR_RESET   = \033[0m
COLOR_INFO    = \033[32m
COLOR_COMMENT = \033[33m

PIP = sudo pip3
SUDO = sudo
PY_BIN = python3

## Help
help:
	printf "${COLOR_COMMENT}Usage:${COLOR_RESET}\n"
	printf " make [target]\n\n"
	printf "${COLOR_COMMENT}Available targets:${COLOR_RESET}\n"
	awk '/^[a-zA-Z\-\_0-9\.@]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf " ${COLOR_INFO}%-25s${COLOR_RESET} %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

all: build build_arm install unit_test run

## Build docker image
build_image:
	sudo docker build . -t wolnosciowiec/infracheck

## Build image for ARM/ARMHF
build_image_arm:
	sudo docker build -f ./armhf.Dockerfile . -t wolnosciowiec/infracheck:armhf

## Run (for testing)
run:
	sudo docker kill infracheck || true
	sudo docker run --name infracheck -p 8000:8000 -t --rm wolnosciowiec/infracheck

## Build
build_package:
	${SUDO} ${PY_BIN} ./setup.py build

## Build documentation
build_docs:
	cd ./docs && make html

## Install
install: build_package
	${PIP} install -r ./requirements.txt
	${SUDO} ${PY_BIN} ./setup.py install
	which infracheck
	make clean

## Clean up the local build directory
clean:
	${SUDO} rm -rf ./build ./infracheck.egg-info

## Run unit tests
unit_test:
	${PY_BIN} -m unittest discover -s ./tests

## Generate code coverage
coverage:
	coverage run --rcfile=.coveragerc --source . -m unittest discover -s ./tests
