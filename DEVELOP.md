## Installing the backend
The backend of cldoc is implemented in python and follows the standard python project
layout and setup.py tooling. To install the frontend use `make install` or
alternatively `python setup.py --user-install`.

## Dependencies
The website frontend of cldoc (which consumes the generate XML doc specification) is
implemented in coffee-script and uses sass for styling. The final generated html,
css and javascript is combined into a single index.html using inline-source.

The easiest way to install the necessary dependencies is to run `make deps`. If you
do not have `make` available, then use:

```
	npm install
	gem install --user-install -b gems -n gems/.bin --no-ri --no-rdoc sass
```

## Generating the frontend
Generating the frontend is necessary if any of the `.coffee`, `.html` or `.scss` files
have been modified. To generate the frontend, use `make generate` to run `setup.py` with
the correct paths to the installed dependencies. Again, if you do not have `make` available, use:

```
	python setup.py generate --coffee=node_modules/.bin/coffee --inline=scripts/inline --sass=gems/.bin/sass
```

## Developing without installing
To make it easier to develop cldoc without installing it continuously, a convenience script
is provided, `scripts/cldoc-dev` which runs cldoc from the source tree. Additionally, when
using it to generate a site, it copies the `javascript` and `styles` directories to the
output so you can run the site without having to `inline` it. A convenience `make` target
called `dev` is provided to run coffee and sass, without running `inline`.

```
	# Run coffee/sass
	make dev

	# Run local cldoc
	scripts/cldoc-dev [command] [OPTIONS] [FILES...]
```