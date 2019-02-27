all: build build_arm run

build:
	sudo docker build . -t wolnosciowiec/infracheck

build_arm:
	sudo docker build -f ./armhf.Dockerfile . -t wolnosciowiec/infracheck:armhf

run:
	sudo docker kill infracheck || true
	sudo docker run --name infracheck -p 8000:8000 -t --rm wolnosciowiec/infracheck
