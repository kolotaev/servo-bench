defmodule Benchmarker.Mixfile do
  use Mix.Project

  def project do
    [app: :benchmarker,
     version: "0.0.1",
     elixir: "~> 1.8",
     deps: deps(),
     aliases: [server: ["app.start", &server/1]]]
  end

  # Configuration for the OTP application
  #
  # Type `mix help compile.app` for more information
  def application do
    [applications: [:cowboy, :plug, :logger]]
  end

  # Dependencies can be Hex packages:
  #
  #   {:mydep, "~> 0.3.0"}
  #
  # Or git/path repositories:
  #
  #   {:mydep, git: "https://github.com/elixir-lang/mydep.git", tag: "0.1.0"}
  #
  # Type `mix help deps` for more examples and options
  defp deps() do
    [
      {:plug_cowboy, "~> 2.0"},
      {:jason, "~> 1.1"},
      {:postgrex, "~> 0.15"},
    ]
  end

  defp server(_) do
    port = String.to_integer( System.get_env("PORT") || "8080" )

    Mix.shell.info "Running Benchmarker on port #{port}"
    {:ok, _} = Plug.Adapters.Cowboy.http Benchmarker, [], port: port
    :code.delete(Access)
    :timer.sleep(:infinity)
  end
end
