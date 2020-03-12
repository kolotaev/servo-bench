defmodule Benchmarker.Endpoints do
  use Plug.Router
  require Jason
  require Ecto

  plug :match
  plug :dispatch

  get "/json" do
    render(conn, new_user(true))
  end

  get "/db" do
    sleep = get_env("SQL_SLEEP_MAX")
    loop = get_env("LOOP_COUNT")
    q = if sleep == 0 do
      "SELECT count(*) FROM pg_catalog.pg_user"
    else
      "SELECT pg_sleep(#{rand_float() * sleep})"
    end
    {_, res} = Ecto.Adapters.SQL.query(Benchmarker.Repo, q)
    loop_int = round(loop)
    users = Enum.map(0..loop_int, fn _ -> new_user(true) end)
    render(conn, %{query: q, res: res.num_rows, users: users})
  end

  match _ do
    send_resp(conn, 404, "<h1>Page Not Found</h1>")
  end

  defp render(conn, result) do
    res = Jason.encode!(result)
    send_resp(conn, 200, res)
  end

  defp rand_float() do
    :rand.uniform()
  end

  defp rand_int(n) do
    :rand.uniform(n)
  end

  defp random_string(length) do
    # todo - why does it slow down performance so drastically?
    # "ABCDEFGHIJKLMNOP" |> String.split("") |> Enum.shuffle |> Enum.take(length) |> to_string
    "abcdef"
  end

  defp new_user(has_friend?) do
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
      friend: fr,
    }
  end

  defp once(key, f) do
    fn ->
      case :ets.lookup(:cache, key) do
        [{^key, val}] ->
          val
        [] ->
          val = f.()
          :ets.insert(:cache, {key, val})
          val
      end
    end
  end

  defp get_env(k) do
    fun = once(k, fn -> elem(Float.parse(System.get_env(k) || "0.0"), 0) end)
    fun.()
  end

end
