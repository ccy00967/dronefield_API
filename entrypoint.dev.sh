#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASES_HOST $DATABASES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#python manage.py flush --settings=core.settings.docker --no-input 
python manage.py migrate --settings=core.settings

exec "$@"