#!/usr/bin/env bash
echo "PEP 8:\n"
python3.6 -m pep8 --count --benchmark --exclude=migrations project_manager

echo "\n\nPEP 257:\n"
python3.6 -m pydocstyle project_manager

echo "\n\nPyFlakes:\n"
python3.6 -m pyflakes project_manager

echo "\n\nPyLint:\n"
python3.6 -m pylint --rcfile .pylintrc --reports=y project_manager
