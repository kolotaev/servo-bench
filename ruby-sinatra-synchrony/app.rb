require 'json'

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

  # This endpoint doesn't participate in the benchmark, but present here as an example of sleep
  get '/delay/:n' do |n|
    EM::Synchrony.sleep n.to_i
    "delayed for #{n} seconds".to_json
  end

  get '/db' do
    n = rand(0...2.0)
    DB.query("SELECT NOW(), #{1} as sl, pg_sleep(#{1})") do |result|
      result.first.to_json
    end
  end
end
