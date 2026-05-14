#!/bin/sh
set -e
python /app/scripts/docker_wait_mongo.py
python /app/scripts/docker_startup_seeds.py
exec "$@"
