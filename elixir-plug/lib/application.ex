defmodule Benchmarker.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application
  require Logger

  def start(_type, _args) do
    children = [
      Benchmarker.Repo,
      {Plug.Cowboy,
       scheme: :http,
       plug: Benchmarker.Endpoints,
       options: [
         port: 8080,
         protocol_options: [
           max_keepalive: 32768
         ],
         transport_options: [
           max_connections: :infinity,
           num_acceptors: 32768
         ]
       ]}
    ]

    Logger.info("Starting application...")
    :ets.new(:cache, [:set, :public, :named_table])

    opts = [strategy: :one_for_one, name: Benchmarker.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
