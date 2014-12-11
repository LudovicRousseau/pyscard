#!/bin/sh

set -e
set -v

scp -r _build/html/* ludov@web.sourceforge.net:/home/project-web/pyscard/htdocs/
