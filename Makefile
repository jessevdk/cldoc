PYTHON = python
SETUP = $(PYTHON) setup.py
COFFEE = node_modules/.bin/coffee
INLINE_SOURCE = node_modules/inline-source
SASS = gems/.bin/sass
UNAME = $(shell uname)

ifeq ($(UNAME),Darwin)
OPEN = open
else
OPEN = xdg-open
endif

all:

deps: $(COFFEE) $(INLINE_SOURCE) $(SASS)

$(COFFEE):
	@echo "Installing coffee"; \
	npm install "coffee-script@1.9.2"

$(INLINE_SOURCE):
	@echo "Installing inline-source"; \
	npm install "inline-source@4.0.1"

$(SASS):
	@echo "Installing sass"; \
	mkdir -p gems/.bin; \
	gem install --user-install -b gems -n gems/.bin --no-ri --no-rdoc sass

generate: deps
	$(SETUP) generate --coffee=$(COFFEE) --inline=scripts/inline --sass=$(SASS)

install:
	$(SETUP) install --user

tests:
	$(PYTHON) tests/regression.py

test-coverage:
	(cd tests && coverage run regression.py && coverage html) && $(OPEN) tests/htmlcov/index.html

.PHONY: all deps generate install tests
