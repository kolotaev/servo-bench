-- wrk -t12 -c400 -d240s http://localhost:8080/v1/graphql --timeout 10s --latency --script graphql.lua

wrk.method = "POST"
-- wrk.body   = "{\"query\":\"query MyQuery {\n  get_random_sleep2 {\n    id\n  }\n}\n\",\"variables\":{}}"
wrk.body = "{\"query\":\"query MyQuery {\n  get_users2 {\n    count\n  }\n}\n\",\"variables\":{}}"
wrk.headers["Content-Type"] = "application/json"


-- Test that it works:

-- local counter = 1
-- local threads = {}

-- function setup(thread)
--    thread:set("id", counter)
--    thread:set("bodies", {})
--    table.insert(threads, thread)
--    counter = counter + 1
-- end

-- function init(args)
--    requests  = 0
--    responses = 0
--    my_bodies = ""

--    local msg = "thread %d created"
--    print(msg:format(id))
-- end

-- function request()
--    requests = requests + 1
--    return wrk.request()
-- end

-- function response(status, headers, body)
--    my_bodies = my_bodies .. "\n" .. body .. "\n"
--    responses = responses + 1
-- end

-- function done(summary, latency, requests)
--    for index, thread in ipairs(threads) do
--       local id        = thread:get("id")
--       local requests  = thread:get("requests")
--       local responses = thread:get("responses")
--       local my_bodies = thread:get("my_bodies")
--       local msg = "thread %d made %d requests and got %d responses with bodies: %s"
--       print(msg:format(id, requests, responses, my_bodies))
--    end
-- end