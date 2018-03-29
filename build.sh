#!/usr/bin/env bash

IMAGE=$(basename $(pwd))

docker build -t ${IMAGE} .
