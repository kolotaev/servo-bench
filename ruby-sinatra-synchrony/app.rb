require 'json'


def random_string(length)
  rand(36**length).to_s(36)
end

def create_user
  User.new(friend: User.new)
end

class User
  def initialize(opts = {})
    @name = opts.fetch(:name, random_string(10))
    @surname = opts.fetch(:surname, random_string(3))
    @street = opts.fetch(:street, random_string(15))
    @school = opts.fetch(:school, random_string(9))
    @bank = opts.fetch(:bank, random_string(4))
    @a = opts.fetch(:a, rand(0..100))
    @b = opts.fetch(:b, rand)
    @c = opts.fetch(:c, rand(0..100))
    @friend = opts.fetch(:friend, nil)
  end

  def to_json(*options)
    instance_variables.map { |v| [v.to_s[1..-1].to_sym, instance_variable_get(v)] }.to_h.to_json
  end
end

class App < Sinatra::Base
  register Sinatra::Synchrony

  before { content_type 'application/json' }
  before '/' do
    content_type 'text/html'
  end

  get '/' do
    %Q(<html>It's me, Synchrony App.<br/>
      Use routes:<br/><a href='./json'>json</a><br/>
      <a href='./db'>db</a><br/>
      <a href='./delay/:n'>delay for n seconds</a></html>)
  end

  get '/json' do
    create_user.to_json
  end

  get '/db' do
    qry = "SELECT pg_sleep(#{Random.rand(SLEEP_MAX)})"
    DB.query(qry) do |result|
      users = []
      LOOP_COUNT.times do
        users << create_user
      end
      { db_query: qry, data: users, result: result.first }.to_json
    end
  end

  # This endpoint doesn't participate in the benchmark, but present here as an example of sleep
  get '/delay/:n' do |n|
    EM::Synchrony.sleep n.to_i
    "delayed for #{n} seconds".to_json
  end
end
