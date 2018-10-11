defmodule Serv.ServController do
  use Serv.Web, :controller

  alias ServUser.{Repo}

  def jsoned(conn, _params) do
    user = Serv.User.new_user(true)
    render(conn, "jsoned.json", user: user)
  end

  def db(conn, _params) do
    {sleep, loop} = get_envs()
    users = Enum.map(0..loop, fn _ -> Serv.User.new_user(true) end)
    q = Serv.User.run_heavy_query(sleep)
    render(conn, "db.json", data: %{query: q, users: users})
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
