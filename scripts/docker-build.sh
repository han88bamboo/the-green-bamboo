#!/usr/bin/env bash
set -ex

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "${SCRIPT_DIR}"/..

echo "Building docker images..."

ECR_REPO="be-drinkx"

if [ -z "$GITHUB_SHA" ]; then
  echo "Running locally - outside of CI"
  DOCKER_FILE="Dockerfile.backend"
  GIT_HASH=$(git rev-parse --short HEAD)
else
  echo "Running inside CI box"
  DOCKER_FILE="Dockerfile.backend"
  GIT_HASH="${GITHUB_SHA::7}"
fi

cd ./backend

docker image build \
  --platform linux/amd64 \
  --build-arg LOGLEVEL="info" \
  --file "${DOCKER_FILE}" \
  --tag "${ECR_REPO}:latest" \
  --tag "${ECR_REPO}:${GIT_HASH}" .
