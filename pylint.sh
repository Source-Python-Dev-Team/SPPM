#!/usr/bin/env bash
printf "Python Code Style:\n"
python -m pycodestyle --count --benchmark --exclude=migrations project_manager

printf "\n\nPython Doc Style:\n"
python -m pydocstyle project_manager --match-dir='^(?!migrations).*'

printf "\n\nPyFlakes:\n"
python -m pyflakes project_manager

printf "\n\nPyLint:\n"
python -m pylint --rcfile .pylintrc --reports=y project_manager
