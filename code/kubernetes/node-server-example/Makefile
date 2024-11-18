.DELETE_ON_ERROR:

build:
	docker build -t  node_app_test .

run:
	docker run -d -p 1337:1337 node_app_test

curl:
	curl localhost:1337

status:
	docker ps

.PHONY: build run curl status
