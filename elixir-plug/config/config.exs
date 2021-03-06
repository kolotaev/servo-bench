# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
use Mix.Config

# This configuration is loaded before any dependency and is restricted
# to this project. If another project depends on this project, this
# file won't be loaded nor affect the parent project. For this reason,
# if you want to provide default values for your application for third-
# party users, it should be done in your mix.exs file.

# Sample configuration:
#
#     config :logger, :console,
#       level: :info,
#       format: "$date $time [$level] $metadata$message\n",
#       metadata: [:user_id]

# It is also possible to import configuration files, relative to this
# directory. For example, you can emulate configuration per environment
# by uncommenting the line below and defining dev.exs, test.exs and such.
# Configuration from the imported file will override the ones defined
# here (which is why it is important to import them last).
#
#     import_config "#{Mix.env}.exs"

config :logger, level: :error


# todo - fix it. Elixir resolves env at compile time!
{poolsize, _} = Integer.parse(System.get_env("POOL_SIZE") || "400")

config :benchmarker, Benchmarker.Repo,
  username: "postgres",
  password: "root",
  database: "postgres",
  hostname: "127.0.0.1",
  port: 5432,
  pool_size: poolsize,
  queue_target: 5000,
  queue_interval: 5000,
  log: false

