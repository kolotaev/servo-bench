FROM crystallang/crystal:latest

WORKDIR /kemal
COPY . .

ENV GC_MARKERS 1
ENV KEMAL_ENV production

RUN shards install
RUN crystal build --release --no-debug server.cr

CMD bash run.sh
