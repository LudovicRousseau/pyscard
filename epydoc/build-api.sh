#!/bin/bash

set -e

DIR=/tmp
VERSION=$(pyversions -i)
export PYTHON=python

pushd $(dirname $0)/..

# build from source
make clean
make build

# install in /tmp
PYTHONPATH=$DIR/lib/$VERSION/site-packages
echo $PYTHONPATH
mkdir -p $PYTHONPATH
export PYTHONPATH

$PYTHON setup.py install --prefix=$DIR

popd

# generate doc
mkdir -p generated/epydoc
epydoc --verbose --html --output generated/epydoc --config=epydoc.cfg

