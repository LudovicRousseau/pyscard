PYTHON ?= python

clean:
	$(PYTHON) setup.py clean

build:
	$(PYTHON) setup.py build

pypi: clean
	rm -f smartcard/scard/scard.py
	rm -f smartcard/scard/scard_wrap.c
	$(PYTHON) setup.py sdist upload

.PHONY: clean build pypi
