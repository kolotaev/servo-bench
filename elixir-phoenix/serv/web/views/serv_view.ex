defmodule Serv.ServView do
  use Serv.Web, :view

  def render("jsoned.json", %{user: user}) do
    %{data: user}
  end

  def render("db.json", %{data: data}) do
    %{
      query: data.query,
      users: data.users
    }
  end
end
