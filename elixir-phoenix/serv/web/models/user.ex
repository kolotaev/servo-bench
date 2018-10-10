defmodule Serv.User do
  use Serv.Web, :model

  def new_user(has_friend?) do
    friend = nil
    if has_friend? do
      friend = new_user(false)
    end
    %{
      name: random_string(10),
      surname: random_string(3),
      street: random_string(15),
      school: random_string(9),
      bank: random_string(4),
      a: rand_int(100),
      b: rand_float(),
      c: rand_int(1090),
      friend: friend
    }
  end

  def run_heavy_query(n) do
    sleep = rand_float() * n
    q = "SELECT pg_sleep(#{sleep})"
    Ecto.Adapters.SQL.query(Serv.Repo, q)
    q
  end
  
  defp random_string(n) do
    alphabet =
      ?a..?z
      |> Enum.concat(?A..?Z)
      |> Enum.concat(?0..?9)
      |> to_string
      |> String.codepoints
    Enum.reduce((1..n), [], fn (_i, acc) -> [Enum.random(alphabet) | acc] end)
      |> Enum.join()
  end
  
  defp rand_float() do
    :random.uniform()
  end

  defp rand_int(n) do
    Enum.random(0..n)
  end
end
