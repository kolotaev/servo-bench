Bundler.require
require './app'

DB = EM::Synchrony::ConnectionPool.new(size: 500) do
  # uri = URI.parse(ENV['DATABASE_URL'])
  PG::EM::Client.new(host: '127.0.0.1', port: 5432, user: 'postgres', password: 'postgres', dbname: 'postgres')
end

run App
