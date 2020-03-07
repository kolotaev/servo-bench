defmodule Benchmarker.Endpoints do
  use Plug.Router
  require Jason
  require Ecto

  @chars "ABCDEFGHIJKLMNOP" |> String.split("")

  plug :match
  plug :dispatch

  get "/json" do
    render(conn, new_user(true))
  end

  get "/db" do
    {sleep, loop} = get_envs()
    q = "SELECT pg_sleep(#{rand_float() * sleep})"
    {_, res} = Ecto.Adapters.SQL.query(Benchmarker.Repo, q)
    users = Enum.map(0..loop, fn _ -> new_user(true) end)
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
    {sleep, _} = Application.fetch_env!(:benchmarker, :sleep_max)
    {loop, _} = Application.fetch_env!(:benchmarker, :loop_count)
    {sleep, loop}
  end

end
