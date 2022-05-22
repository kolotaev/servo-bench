# Openresty

FROM openresty/openresty:alpine-fat

RUN apk add --no-cache git

# Create app directory
WORKDIR /usr/src/app

# Bundle app source
COPY . .

RUN /usr/local/openresty/luajit/bin/luarocks install luasocket
RUN /usr/local/openresty/luajit/bin/luarocks install pgmoon
RUN /usr/local/openresty/luajit/bin/luarocks install lua-resty-http

EXPOSE 8080
CMD nginx -c /usr/src/app/nginx.conf -g "worker_processes '"$(nproc)"';"
