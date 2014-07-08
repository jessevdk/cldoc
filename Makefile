PYTHON = python
SETUP = $(PYTHON) setup.py
COFFEE = node_modules/.bin/coffee
INLINER = node_modules/.bin/inliner
SASS = gems/.bin/sass

all:

deps: $(COFFEE) $(INLINER) $(SASS)

$(COFFEE):
	@echo "Installing coffee"; \
	npm install coffee-script

$(INLINER):
	@echo "Installing inliner"; \
	npm install inliner

$(SASS):
	@echo "Installing sass"; \
	mkdir -p gems/.bin; \
	gem install --user-install -b gems -n gems/.bin --no-ri --no-rdoc sass

generate: deps
	$(SETUP) generate --coffee=$(COFFEE) --inliner=$(INLINER) --sass=$(SASS)

install:
	$(SETUP) install --user

tests:
	$(PYTHON) tests/regression.py

.PHONY: all deps generate install tests
