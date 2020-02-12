FROM ruby

ADD . .

RUN bundle install

EXPOSE 8080
CMD ["bundle", "exec", "rackup", "-s", "thin", "-o", "0.0.0.0", "-p", "8080"]
