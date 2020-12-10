build: train
	docker network create interpreter_net
	docker-compose build

train:
	rasa train \
		--config rasa/config.yml \
		--data rasa/data \
		--domain rasa/domain.yml \
		--out rasa/models

delmod:
	rm -rf rasa/models/