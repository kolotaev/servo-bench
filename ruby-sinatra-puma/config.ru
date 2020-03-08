#!/usr/bin/env ruby

require 'active_record'

require './app'

SLEEP_MAX = (ENV.fetch 'SQL_SLEEP_MAX', 0).to_f
LOOP_COUNT = (ENV.fetch 'LOOP_COUNT', 0).to_i
POOL_SIZE = (ENV.fetch 'POOL_SIZE', 1).to_i

require 'active_record'

ActiveRecord::Base.establish_connection(
  :adapter => 'sqlite3',
  :database =>  'sinatra_application.sqlite3.db'
)

run Benchy
