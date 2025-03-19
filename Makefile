version := $(shell python -c 'from tapy import __version__; print(__version__)')

.PHONY: format
format:
	ruff format tapy
	ruff check tapy --select I --fix

.PHONY: test
test:
	pytest --cov=tapy -vv test/

.PHONY: clean
clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -f
	rm -Rf dist
	rm -Rf *.egg-info

.PHONY: docs
docs:
	cd docs && make html

.PHONY: authors
authors:
	git log --format='%aN <%aE>' `git describe --abbrev=0 --tags`..@ | sort | uniq >> AUTHORS
	cat AUTHORS | sort --ignore-case | uniq >> AUTHORS_
	mv AUTHORS_ AUTHORS
