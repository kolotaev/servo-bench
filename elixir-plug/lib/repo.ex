defmodule Benchmarker.Repo do
  use Ecto.Repo,
    otp_app: :benchmarker,
    adapter: Ecto.Adapters.Postgres
end
