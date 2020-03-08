root = "#{Dir.getwd}"

rackup "#{root}/config.ru"

threads 1, 400

activate_control_app

port 8080
