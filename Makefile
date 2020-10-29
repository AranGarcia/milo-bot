build:
	docker build . --tag miloc

run:
	docker run -p 5005:5005 -d --name milo --rm -it miloc

bash:
	docker exec -it milo bash

stop:
	docker stop milo