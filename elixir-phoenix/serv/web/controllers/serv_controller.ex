defmodule Serv.ServController do
  use Serv.Web, :controller

  alias ServTracker.{Repo, Tracker}

  def index(conn, _params) do
    trackers = Repo.all(Tracker)
    render(conn, "index.json", trackers: trackers)
  end
end
