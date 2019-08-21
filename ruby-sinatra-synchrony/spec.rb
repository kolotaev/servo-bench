Bundler.require
require './app'

App.set :environment, :test

Sinatra::Synchrony.patch_tests!

describe App do
  include Rack::Test::Methods
  
  def app
    App
  end
  
  it 'says hello' do
    get '/'
    last_response.ok?.should be_true
    last_response.body.should == '"hello async"'
  end
  
  it 'says hello' do
    get '/delay/1'
    last_response.ok?.should be_true
    last_response.body.should == '"delayed for 1 seconds"'
  end
end