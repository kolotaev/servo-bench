local ngx = ngx
local json = require("cjson")
local pgmoon = require("pgmoon")
local http = require("resty.http")


local SLEEP_MAX = os.getenv("SQL_SLEEP_MAX")
local LOOP_COUNT = os.getenv("LOOP_COUNT")
local TARGET_URL = os.getenv("TARGET_URL")

local dbspec = {
    host = "127.0.0.1",
    port = "5432",
    user = "postgres",
    password = "root",
    database = "postgres",
}

local function random_string(length)
    local res = ""
    for i = 1, length do
        res = res .. string.char(math.random(97, 122))
    end
    return res
end

local function random_sleep()
    return math.random() * SLEEP_MAX
end

local function create_user(has_friend)
    local user = {
        id = random_string(34),
        name = random_string(10),
        surname = random_string(3),
        street = random_string(15),
        school = random_string(9),
        bank = random_string(4),
        a = math.random(100),
        b = math.random(),
        c = math.random(1090),
    }
    if has_friend then
        user["friend"] = create_user(false)
    end
    return user
end

-- exports
local _M = {}

function _M.json()
    local user = create_user(true)
    ngx.print(json.encode(user))
end

function _M.http()
    uri = TARGET_URL .. "/" .. random_sleep()
    local client = http.new()
    local res, err = client:request_uri(uri, { method = "GET" })
    if err then
        ngx.status = 500
        return ngx.exit(500)
    end
    ngx.print(res.body)
end

function _M.db()
    local pg = pgmoon.new(dbspec)
    assert(pg:connect())
    local users = {}
    local qry = ""
    if (SLEEP_MAX + 0) == 0 then
        qry = "SELECT count(*), 777 FROM pg_catalog.pg_user"
    else
        qry = "SELECT pg_sleep(" .. random_sleep() .. "), 42"
    end
    local res, err = pg:query(qry)
    pg:keepalive()
    pg = nil -- good practice
    
    if err then
        ngx.status = 500
        return ngx.exit(500)
    end

    for i = 0, LOOP_COUNT, 1 do
        users[i] = create_user(true)
    end
    ngx.print(json.encode({
        err = err,
        res = res,
        users = users,
        query = qry,
    }))
end

return _M
