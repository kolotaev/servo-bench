#!/usr/bin/env ruby

require 'sinatra'

configure {
  set :server, :puma
}

class Benchy < Sinatra::Base
  get '/' do
    return 'It works!'
  end

  run! if app_file == $0
end
