#!/bin/bash

set -e

# update the web site at sourceforge.net
pushd $(dirname $0)/generated
rsync --recursive --verbose --update epydoc ludov@web.sourceforge.net:/home/project-web/pyscard/htdocs/
popd
