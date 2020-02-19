require "kemal"


def random_string(length)
  rand(36**length).to_s(36)
end

class User
  def initialize(**opts)
    @name = opts.fetch(:name, random_string 10)
    @surname = opts.fetch(:surname, random_string 3)
    @street = opts.fetch(:street, random_string 15)
    @school = opts.fetch(:school, random_string 9)
    @bank = opts.fetch(:bank, random_string 9)
    @a = opts.fetch(:a, rand(0..100))
    @b = opts.fetch(:b, rand)
    @friend = opts.fetch(:friend, nil)
  end
end

get "/" do
  "
  <html>It's me, Express App.<br/>
  Use routes:<br/><a href='./json'>json</a><br/>
  <a href='./db'>db</a></html>
  "
end

get "/json" do
  random_string 5
end

Kemal.run
