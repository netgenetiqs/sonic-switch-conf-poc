.PHONY: clean install install-all

.PHONY: clean
clean:
	@rm -rf $$(pipenv --venv)

.PHONY: install
install:
	@asdf install
	@mkdir -p .venv
	@pipenv install

.PHONY: install-all
install-all:
	@asdf install
	@mkdir -p .venv
	@pipenv install
	@pipenv install -d

.PHONY: run
run:
	@.venv/bin/python main.py

.PHONY: create
create:
	@.venv/bin/python main.py create.yml

.PHONY: delete
delete:
	@.venv/bin/python main.py delete.yml

.PHONY: init
init:
	/usr/bin/env pip install -r requirements.txt

.PHONY: docker
docker:
	docker build . --tag ttl.sh/sonic-switch-conf-poc:24h
	docker push ttl.sh/sonic-switch-conf-poc:24h

.PHONY: docker-run
docker-run:
	docker run -v $(pwd)/main.py:/main.py -v $(pwd)/config.yml:/config.yml ttl.sh/sonic-switch-conf-poc:2h python main.py "192.168.2.190" admin *** config.yml
