Bundler.require
require './app'

SLEEP_MAX = (ENV.fetch 'SQL_SLEEP_MAX', 0.0).to_f
LOOP_COUNT = (ENV.fetch 'LOOP_COUNT', 0).to_i
POOL_SIZE = (ENV.fetch 'POOL_SIZE', 1).to_i

DB = EM::Synchrony::ConnectionPool.new(size: POOL_SIZE) do
  PG::EM::Client.new(host: '127.0.0.1', port: 5432, user: 'postgres', password: 'root', dbname: 'postgres')
end

run App
