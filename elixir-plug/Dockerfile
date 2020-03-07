FROM elixir:1.10-alpine

ENV PORT=8080 MIX_ENV=prod
EXPOSE 8080

# copy source files
COPY . /usr/src/server
WORKDIR /usr/src/server

# install dependencies and compile
RUN mix local.hex --force
RUN mix local.rebar --force
RUN mix deps.get
RUN mix deps.compile
RUN mix release

# launch server
CMD ["./_build/prod/rel/benchmarker/bin/benchmarker", "start"]
