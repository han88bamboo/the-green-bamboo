#!/usr/bin/env bash
set -ex

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "${SCRIPT_DIR}"/..

echo "Pushing docker images..."

AWS_REGION="${AWS_DEFAULT_REGION:-ap-southeast-1}"
AWS_ACCOUNT="851725425890"
ECR_HOST="${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"
ECR_REPO="be-drinkx"

if [ -z "$GITHUB_SHA" ]; then
  echo "Running locally - outside of CI"
  GIT_HASH=$(git rev-parse --short HEAD)
else
  echo "Running inside CI box"
  GIT_HASH="${GITHUB_SHA::7}"
fi

GIT_TAG="${ECR_HOST}/${ECR_REPO}:${GIT_HASH}"
BUILD_HASH=$(docker image ls --no-trunc --quiet "${ECR_REPO}:${GIT_HASH}" | sed -e 's/:/-/g')
BUILD_TAG="${ECR_HOST}/${ECR_REPO}:${BUILD_HASH}"
LATEST_TAG="${ECR_HOST}/${ECR_REPO}:latest"

# should have already been built by previous step
aws ecr get-login-password --region "${AWS_REGION}" | docker login --username AWS --password-stdin "${ECR_HOST}"

docker image tag "${ECR_REPO}:${GIT_HASH}" "${BUILD_TAG}"
docker image push "${BUILD_TAG}"

docker image tag "${ECR_REPO}:${GIT_HASH}" "${GIT_TAG}"
docker image push "${GIT_TAG}"

docker image tag "${ECR_REPO}:${GIT_HASH}" "${LATEST_TAG}"
docker image push "${LATEST_TAG}"

echo "${BUILD_HASH}" >be-drinkx-hash.txt
