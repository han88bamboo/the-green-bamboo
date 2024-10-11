#!/usr/bin/env bash
set -ex

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "${SCRIPT_DIR}"/..

PG_VERSION=15.8

docker compose --project-name drink-x \
    --env-file=.env \
    -f docker-compose-db.yml \
    -f docker-compose-be.yml \
    -f docker-compose-fe.yml \
    down --remove-orphans --volumes

docker compose --project-name drink-x \
    --env-file=.env \
    -f docker-compose-db.yml \
    -f docker-compose-be.yml \
    -f docker-compose-fe.yml \
    up --build --remove-orphans --detach --pull=missing --renew-anon-volumes "$@"
