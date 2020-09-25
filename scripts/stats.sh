#!/bin/bash

coverage run -m unittest
coverage report |grep TOTAL
coverage html --skip-covered
# Remove TODO tag in generated 3rd-pary file so it doesn't show up in TODO lists
sed --in-place s/TODO/DODO/ htmlcov/jquery.hotkeys.js

echo -n "Source lines: "; find cadlib/ -name \*.py |xargs cat |wc -l
echo -n "Test lines:   "; find tests/ -name \*.py |xargs cat |wc -l
echo -n "Low TODOs:    "; grep -i low doc/todo.txt  |wc -l
echo -n "Medium TODOs: "; grep -i medium doc/todo.txt  |wc -l
echo -n "High TODOs:   "; grep -i high doc/todo.txt  |wc -l
echo -n "Code TODOs:   "; grep -riI todo cadlib/ tests/ |wc -l
echo -n "Code FIXMEs:  "; grep -riI fixme cadlib/ tests/ |wc -l

