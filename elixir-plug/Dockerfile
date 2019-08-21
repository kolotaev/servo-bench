FROM elixir:1.6-alpine

ENV PORT=8080 MIX_ENV=prod
EXPOSE 8080

# install hex and rebar
RUN mix local.hex --force
RUN mix local.rebar --force

# copy source files
COPY . /usr/src/app
WORKDIR /usr/src/app/serv

# install dependencies and compile
RUN mix deps.get --only prod
RUN mix compile
RUN mix phx.digest

# launch server
CMD ["mix", "phx.server"]
