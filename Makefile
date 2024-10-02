PYTHON ?= python3
TOX ?= tox
COVERAGE ?= coverage

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
	rm -rf dist
	# Use the tox 'build' label to generate wheels for all Python versions.
	$(TOX) run -m build
	python3 -m twine upload dist/*

test:
	pytest --verbose

coverage:
	$(COVERAGE) erase
	$(COVERAGE) run -m pytest
	$(COVERAGE) combine
	$(COVERAGE) report
	$(COVERAGE) html

pylint:
	$(PYTHON) -m pylint --errors-only smartcard

ChangeLog.git:
	git log --stat --decorate=short > $@

.PHONY: sync-docs
sync-docs: clean
	$(TOX) -e docs
	rsync \
		--recursive --verbose --update --rsh=ssh --links \
		build/docs/ \
		ludov@web.sourceforge.net:/home/project-web/pyscard/htdocs/

.PHONY: clean build pypi test
