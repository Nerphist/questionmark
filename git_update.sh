#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'Branch not defined. Usage: ./git_update.sh master'
    exit 1
fi

git fetch --all
git reset --hard origin/$1

source venv/bin/activate

chmod 0775 ./git_update.sh

python3 manage.py runserver 10.0.1.129:8888 --noreload
