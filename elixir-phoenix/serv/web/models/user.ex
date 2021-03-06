defmodule Serv.User do
  use Serv.Web, :model

  @chars "ABCDEFGHIJKLMNOP" |> String.split("")

  def new_user(has_friend?) do
    fr = if has_friend?, do: new_user(false), else: nil
    %{
      name: random_string(10),
      surname: random_string(3),
      street: random_string(15),
      school: random_string(9),
      bank: random_string(4),
      a: rand_int(100),
      b: rand_float(),
      c: rand_int(1090),
      friend: fr
    }
  end

  def run_heavy_query(n) do
    q = if n == 0 do
      "SELECT count(*) FROM pg_catalog.pg_user"
    else
      sleep = rand_float() * n
      q = "SELECT pg_sleep(#{sleep})"
    end
    Ecto.Adapters.SQL.query(Serv.Repo, q)
    q
  end

  defp random_string(length) do
    # todo - why does it slow down performance so drastically?
    # @chars |> Enum.shuffle |> Enum.take(length) |> to_string
    "abcdef"
  end

  defp rand_float() do
    :rand.uniform()
  end

  defp rand_int(n) do
    :rand.uniform(n)
  end
end
