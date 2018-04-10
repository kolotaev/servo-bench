#!/usr/bin/env bash

# Update sources
apt-get update

# Install curl
apt-get install curl -y

# Install python3
apt-get install python3 -y

# Install Postgres 9.4
apt-get install postgresql-9.4 postgresql-client-9.4 -y

# Configure Postgres
sudo -u postgres psql -c "ALTER USER \"postgres\" WITH PASSWORD 'root';"
mkdir -p /etc/postgresql/9.4/main/conf.d
cp /shared/postgres_custom.conf /etc/postgresql/9.4/main/conf.d/00postgres_custom.conf
service postgresql restart

# Install Docker
if [ -x "$(command -v docker)" ]; then
    echo "Docker is already installed"
else
    echo "Install docker"
    cd /tmp
    curl -fsSL get.docker.com -o get-docker.sh
    sh get-docker.sh
    usermod -aG docker vagrant
fi

# Build all images
cd /shared && ./mule.sh -x && cd -

