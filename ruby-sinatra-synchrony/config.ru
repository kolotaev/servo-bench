Bundler.require
require './app'

DB = EM::Synchrony::ConnectionPool.new(size: 450) do
  PG::EM::Client.new(host: '127.0.0.1', port: 5432, user: 'postgres', password: 'root', dbname: 'postgres')
end

SLEEP_MAX = (ENV.fetch 'SQL_SLEEP_MAX', 0).to_f
LOOP_COUNT = (ENV.fetch 'LOOP_COUNT', 0).to_i

run App
