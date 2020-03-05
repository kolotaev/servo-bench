defmodule Benchmarker do
  use Plug.Router
  require Jason
  require Postgrex

  @chars "ABCDEFGHIJKLMNOP" |> String.split("")

  # {:ok, pid} = Postgrex.start_link(hostname: "127.0.0.1", username: "postgres", password: "root", database: "postgres")

  plug :match
  plug :dispatch

  get "/json" do
    render(conn, new_user(true))
  end

  get "/db" do
    {sleep, loop} = get_envs()
    q = "SELECT pg_sleep(#{rand_float() * sleep})"
    # users = Enum.map(0..loop, fn -> new_user(true) end)
    # q = Serv.User.run_heavy_query(sleep)
    # res = Postgrex.query!(pid, q, [])
    res = nil
    users = []
    render(conn, %{query: q, res: res, users: users})
  end

  defp render(conn, result) do
    res = Jason.encode!(result)
    send_resp(conn, 200, res)
  end

  defp rand_float(), do: :rand.uniform()

  defp rand_int(n), do: :rand.uniform(n)

  defp random_string(length) do
    # todo - why does it slow down performance so drastically?
    @chars |> Enum.shuffle |> Enum.take(length) |> to_string
    # "abcdef"
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

  defp get_envs() do
    {sleep, _} = Integer.parse(System.get_env("SQL_SLEEP_MAX"))
    if is_nil(sleep) do
      sleep = 0
    end
    {loop, _} = Integer.parse(System.get_env("LOOP_COUNT"))
    if is_nil(loop) do
      loop = 0
    end
    {sleep, loop}
  end

end
