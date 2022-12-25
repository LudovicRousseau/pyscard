#!/bin/bash

set -e

cd $(dirname $0)

rm -r html

# Sphinx
make html
mv _build/html .

# pydoctor
(cd .. && pydoctor \
	--project-name=PySCard \
	--project-url=https://github.com/LudovicRousseau/pyscard \
	--html-output=doc/html/apidocs \
	.)

echo
echo "The documentation is available in file://$(pwd)/html/index.html"
