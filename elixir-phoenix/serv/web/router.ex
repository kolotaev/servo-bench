defmodule Serv.Router do
  use Serv.Web, :router

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", Serv do
    pipe_through :api
  end
end
