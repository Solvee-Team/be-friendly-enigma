#!/bin/bash
python manage.py migrate --noinput

python manage.py collectstatic --noinput

#write fcm-keys file from env
echo $FCM_KEY_BASE64 | base64 -d > /usr/src/app/fcm-keys.json

# Start memcached server in detached mode for celery
service memcached start

# Start rabbitmq server in detached mode for celery
service rabbitmq-server start

# run celery worker with beat_schedule
celery -A friendly_enigma worker
