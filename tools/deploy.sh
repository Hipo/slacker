#!/usr/bin/env bash
DOCKER_CMD='CONTAINER_UID=$(id -u) CONTAINER_GID=$(id -g) docker-compose -f docker-compose.yml -f docker-compose.production.yml'

# GIT_SSH_COMMAND="ssh -i ~/.ssh/slacker_backend" git reset --hard
GIT_SSH_COMMAND="ssh -i ~/.ssh/slacker_backend" git fetch
GIT_SSH_COMMAND="ssh -i ~/.ssh/slacker_backend" git checkout production
GIT_SSH_COMMAND="ssh -i ~/.ssh/slacker_backend" git pull origin production

CONTAINER_UID=$(id -u) CONTAINER_GID=$(id -g) docker-compose -f docker-compose.yml -f docker-compose.production.yml stop --timeout 60
CONTAINER_UID=$(id -u) CONTAINER_GID=$(id -g) docker-compose -f docker-compose.yml -f docker-compose.production.yml rm --force
CONTAINER_UID=$(id -u) CONTAINER_GID=$(id -g) docker-compose -f docker-compose.yml -f docker-compose.production.yml up --remove-orphans --build --no-start
CONTAINER_UID=$(id -u) CONTAINER_GID=$(id -g) docker-compose -f docker-compose.yml -f docker-compose.production.yml start postgres

echo Sleeping for 120 seconds..
sleep 30
echo 90 seconds remaining.
sleep 30
echo 60 seconds remaining.
sleep 30
echo 30 seconds remaining.
sleep 30
echo waking-up.

CONTAINER_UID=$(id -u) CONTAINER_GID=$(id -g) docker-compose -f docker-compose.yml -f docker-compose.production.yml run slacker ./manage.py migrate --no-input
CONTAINER_UID=$(id -u) CONTAINER_GID=$(id -g) docker-compose -f docker-compose.yml -f docker-compose.production.yml run slacker ./manage.py collectstatic --no-input
CONTAINER_UID=$(id -u) CONTAINER_GID=$(id -g) docker-compose -f docker-compose.yml -f docker-compose.production.yml start slacker notification_sender

docker image prune -f
docker container prune -f
docker network prune -f