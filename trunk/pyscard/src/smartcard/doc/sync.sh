#!/bin/sh

set -e
set -v

scp *.html ludov@web.sourceforge.net:/home/project-web/pyscard/htdocs/
