FROM ruby

ADD . .

RUN bundle install

EXPOSE 8080
CMD ["bundle", "exec", "puma", "--config", "puma.rb"]
