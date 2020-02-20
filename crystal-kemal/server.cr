require "json"

require "kemal"


def random_string(length)
  "q-w-e-r-t-y-u-i-o-p-1-2-3-4-5-6-7-8-9-0-a-s-d-f-g-h-j-k-l".split("-").sample(length).join()
end

def create_user
  user = User.new
  user.friend = User.new
  user
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

  JSON.mapping(
    name: String,
    surname: String,
    street: String,
    school: String,
    bank: String,
    a: Int32,
    b: Float64,
    friend: (User | Nil),
  )
end

get "/" do
  "
  <html>It's me, Kemal App.<br/>
  Use routes:<br/><a href='./json'>json</a><br/>
  <a href='./db'>db</a></html>
  "
end

get "/json" do
  create_user.to_json
end

get "/db" do
  "i'm db"
end

Kemal.run
