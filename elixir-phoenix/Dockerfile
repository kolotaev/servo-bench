FROM elixir:1.6-alpine

# install mix
RUN mix local.hex --force

# configure work directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# copy source files
COPY serv/* .

# install dependencies and compile
RUN mix deps.get --only prod
RUN MIX_ENV=prod mix compile
# RUN mix phx.digest

EXPOSE 8080

# launch server
CMD ["PORT=8080", "MIX_ENV=prod", "mix", "phx.server"]
