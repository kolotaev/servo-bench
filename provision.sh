#!/usr/bin/env bash

# Update sources
apt-get update

# Install curl
apt-get install curl -y

# Install python3
apt-get install python3 -y

# Install postgres 9.4
apt-get install postgresql-9.4 postgresql-client-9.4 -y

# Install Docker
cd /tmp
curl -fsSL get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker $USER
