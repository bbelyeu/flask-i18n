#!/bin/bash

echo "> running pycodestyle..."
pycodestyle --max-line-length=99 --exclude='.eggs,build,dist' .
if [ $? != 0 ]
then
    exit 1
else
    echo "pycodestyle looks good!"
fi
echo

echo "> running flake8..."
flake8 --exclude='.eggs,build,dist' --max-line-length=99
if [ $? != 0 ]
then
    exit 1
else
    echo "flake8 looks good!"
fi
echo

echo "> running pylint..."
pylint flask_i18n

if [ $? != 0 ] && [ $? != 32 ]; then
    echo "Exit code: $?"
    exit 1
else
    echo "pylint looks good!"
fi
echo

echo "> running isort..."
isort -c --diff
if [ $? != 0 ]; then
    exit 1
else
    echo "isort looks good!"
fi
echo

echo ">Running detect-secrets..."
git diff --cached --stat=500 | grep '+' | awk {'print $1'} | awk 'NR>1 {print l} {l=$0}' | xargs detect-secrets-hook
