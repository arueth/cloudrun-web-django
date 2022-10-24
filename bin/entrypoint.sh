#!/bin/bash
set -e

if [ "${DJANGO_MANAGEPY_MIGRATE,,}" = 'true' ]; then
    echo "Running manage.py migrate"
    python3 manage.py migrate --noinput
fi

if [ "${DJANGO_MANAGEPY_COLLECTSTATIC,,}" = 'true' ]; then
    echo "Running manage.py collectstatic"
    python3 manage.py collectstatic --noinput
fi

if [ "${DJANGO_DONT_START_SERVER,,}" = 'true' ]; then
    echo "Not starting the server, exiting..."
    exit 0
fi

exec "$@"