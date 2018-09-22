all: build run

build:
	sudo docker build . -t wolnosciowiec/infracheck

run:
	sudo docker kill infracheck || true
	sudo docker run --name infracheck -p 8000:8000 -t --rm wolnosciowiec/infracheck