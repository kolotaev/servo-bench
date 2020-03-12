require 'json'

require 'sinatra'
require 'active_record'


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

configure {
  set :server, :puma
}

class Benchy < Sinatra::Base
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
    qry = if SLEEP_MAX == 0
      "SELECT count(*) FROM pg_catalog.pg_user"
    else
      "SELECT pg_sleep(#{Random.rand(SLEEP_MAX)})"
    end
    st = ActiveRecord::Base.connection.execute(qry)
    users = []
    LOOP_COUNT.times do
      users << create_user
    end
    { db_query: qry, data: users, result: st.first }.to_json
  end

  run! if app_file == $0
end
