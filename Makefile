PYTHON ?= python3
TOX ?= tox

build:
	$(TOX) run -m build

install: clean
	$(PYTHON) -m pip install --editable .

clean:
	$(PYTHON) setup.py clean
	rm -rf build
	rm -f src/smartcard/scard/_scard*.so

pypi: clean
	# files generated by swig
	rm -f src/smartcard/scard/scard.py
	rm -f src/smartcard/scard/scard_wrap.c
	# files generated by sphinx
	rm -rf src/smartcard/doc/_build
	# files generated by pydoctor
	rm -rf src/smartcard/doc/html
	rm -rf dist
	# Use the tox 'build' label to generate wheels for all Python versions.
	$(TOX) run -m build
	python3 -m twine upload dist/*

test:
	$(TOX) run -e py

coverage:
	$(TOX) run

ChangeLog.git:
	git log --stat --decorate=short > $@

.PHONY: clean build pypi test
