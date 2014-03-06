#!/bin/sh

cp config.ini config.bak
cp config.dist config.ini
python setup.py sdist --no-defaults
cp config.bak config.ini
rm config.bak
