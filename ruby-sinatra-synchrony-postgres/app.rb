require 'json'

class App < Sinatra::Base
  register Sinatra::Synchrony

  use Rack::JSONP
  before { content_type 'application/json' }

  get '/' do
    "hello async".to_json
  end

  get '/delay/:n' do |n|
    EM::Synchrony.sleep n.to_i
    "delayed for #{n} seconds".to_json
  end
  
  get '/db/:n' do |n|
    n = rand(0...2.0)
    DB.query("SELECT NOW(), #{n} as sl, pg_sleep(#{n})") do |result|
      result.first.to_json
    end
  end
end
