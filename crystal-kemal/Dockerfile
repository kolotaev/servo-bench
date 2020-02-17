FROM crystallang/crystal:latest

WORKDIR /kemal
# COPY views views
COPY . .

ENV GC_MARKERS 1
ENV KEMAL_ENV production
ENV DATABASE_URL postgres://benchmarkdbuser:benchmarkdbpass@tfb-database:5432/hello_world?initial_pool_size=56&max_idle_pool_size=56

RUN shards install
RUN crystal build --release --no-debug server.cr

CMD bash run.sh
