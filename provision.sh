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
echo "include_dir 'conf.d'" >> /etc/postgresql/9.4/main/postgresql.conf

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

# Configure system for high load.
sysctl -w net.core.rmem_max=16777216
sysctl -w net.core.wmem_max=16777216
sysctl -w net.ipv4.tcp_rmem="4096 87380 16777216"
sysctl -w net.ipv4.tcp_wmem="4096 16384 16777216"

sysctl -w net.core.somaxconn=4096

sysctl -w net.core.netdev_max_backlog=16384
sysctl -w net.ipv4.tcp_max_syn_backlog=8192
sysctl -w net.ipv4.tcp_syncookies=1

sysctl -w net.ipv4.ip_local_port_range="1024 65535"
sysctl -w net.ipv4.tcp_tw_recycle=1

echo "*            hard nofile     40000" >> /etc/security/limits.conf
echo "*            soft nofile     40000" >> /etc/security/limits.conf

sysctl -w net.ipv4.tcp_congestion_control=cubic

# ? https://stackoverflow.com/questions/9798705/arval-sqlexception-fatal-sorry-too-many-clients-already-in-postgres#14191857
sysctl -w kernel.shmmax=134217728
sysctl -w kernel.shmall=2097152
echo "kernel.shmmax=134217728" >> /etc/sysctl.conf
echo "kernel.shmall=2097152" >> /etc/sysctl.conf


# Restarting services
service postgresql restart
