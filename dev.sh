#!/bin/sh
docker_container_name=$1
version="python3.10"
if [ -z "$docker_container_name" ]; then
  echo "Usage: $0 <docker_container_name>"
  exit 1
fi

if [ ! -d .venv ]; then
  poetry env use $version
  poetry install
  docker exec $1 mkdir -p $(pwd)
fi

docker exec $1 rm -r $(pwd)/.venv
docker cp .venv $1:$(pwd)/.venv
docker cp lnurlcln $1:$(pwd)/.venv/lib/$version/site-packages/lnurlcln
docker exec $1 rm $(pwd)/.venv/lib/$version/site-packages/lnurlcln.pth

docker exec $1 lightning-cli --network regtest plugin stop $(pwd)/.venv/bin/lnurlcln
docker exec $1 lightning-cli --network regtest plugin start $(pwd)/.venv/bin/lnurlcln
