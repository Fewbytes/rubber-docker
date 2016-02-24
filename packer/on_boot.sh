#!/bin/bash

mkdir -p /workshop/containers

# Pull latest version of rubber-docker, install requirements & build the C extension
if [[ -d /workshop/rubber-docker ]]; then
    pushd /workshop/rubber-docker
    git pull && python setup.py install
    [[ -f requirements.txt ]] && pip install -r requirements.txt
    popd
fi

chown ubuntu:ubuntu -R /workshop
