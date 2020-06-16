#!/usr/bin/env bash

set -eu
set -o pipefail
cd "$(dirname "$0")"


RELEASE="$1"
BUILD="msjpq/kvm-windows-build:latest"
IMAGE="msjpq/kvm-windows:$RELEASE"


# docker build -t "$BUILD" . -f "build/Dockerfile"
docker build -t "$IMAGE" . -f "release/$RELEASE/Dockerfile"


if [[ $# -gt 1 ]]
then
  # docker push "$BUILD"
  docker push "$IMAGE"
fi

