PYTHON = python
SETUP = $(PYTHON) setup.py
COFFEE = node_modules/.bin/coffee
INLINE_SOURCE = node_modules/inline-source
SASS = node_modules/.bin/node-sass
UNAME = $(shell uname)

ifeq ($(UNAME),Darwin)
OPEN = open
else
OPEN = xdg-open
endif

all:

$(INLINE_SOURCE):
	npm install

# Fake chain to inline-source since they both install using a single npm install
$(COFFEE): $(INLINE_SOURCE)

deps: $(COFFEE) $(INLINE_SOURCE) $(SASS)

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

dev:
	$(PYTHON) setup.py generate --coffee=$(COFFEE) --sass=$(SASS) --inline=""

.PHONY: all deps generate install tests
