#!/usr/bin/env bash
set -ex

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "${SCRIPT_DIR}"/..

echo "Building FE release..."

ECR_REPO="fe-drinkx"

if [ -z "$GITHUB_SHA" ]; then
  echo "Running locally - outside of CI"
  DOCKER_FILE="Dockerfile.frontend"
  GIT_HASH=$(git rev-parse --short HEAD)
else
  echo "Running inside CI box"
  DOCKER_FILE="Dockerfile.frontend"
  GIT_HASH="${GITHUB_SHA::7}"
fi

cd ./frontend

docker image build \
  --platform linux/amd64 \
  --build-arg LOGLEVEL="info" \
  --file "${DOCKER_FILE}" \
  --tag "${ECR_REPO}:latest" \
  --tag "${ECR_REPO}:${GIT_HASH}" .

nvm use

npm install
npm run build --production --progress
