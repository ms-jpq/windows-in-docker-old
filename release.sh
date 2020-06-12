#!/usr/bin/env bash

set -eu
set -o pipefail

IMAGE="msjpq/kvm-windows:latest"

cd "$(dirname "$0")"
docker build -t "$IMAGE" . -f "Dockerfile"

if [[ $# -gt 0 ]]
then
  docker push "$IMAGE"
fi

