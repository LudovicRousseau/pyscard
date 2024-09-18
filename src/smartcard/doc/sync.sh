#!/bin/sh

set -e
set -v

cd $(dirname $0)

ARGS="--recursive --verbose --update --rsh=ssh --links"

rsync $ARGS html/ ludov@web.sourceforge.net:/home/project-web/pyscard/htdocs/
