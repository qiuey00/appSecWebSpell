#!/bin/bash

export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=/spell-app/app.py

export SECRET_KEY=$(cat /run/secrets/secret_key)
export ADMIN_PASS=$(cat /run/secrets/adminpass)