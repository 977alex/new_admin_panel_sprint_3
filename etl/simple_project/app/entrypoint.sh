#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

echo "python manage.py migrate"
python manage.py migrate & wait
echo "python manage.py createcachetable --noinput || true"
python manage.py createcachetable --noinput || true & wait

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    echo "python manage.py createsuperuser --noinput || true"
    python manage.py createsuperuser --noinput || true & wait

fi

echo "python manage.py collectstatic --noinput || true"
python manage.py collectstatic --noinput || true & wait

cd sqlite_to_postgres

echo "python main.py"
python main.py

cd ../
echo "uwsgi --strict --ini uwsgi.ini"
uwsgi --strict --ini uwsgi.ini
