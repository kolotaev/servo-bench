-- example reporting script which demonstrates a custom
-- done() function that prints latency percentiles as CSV

done = function(summary, latency, requests)
    io.write("------------------------------\n")
    for _, p in pairs({ 50, 90, 99, 99.999 }) do
        n = latency:percentile(p)
        io.write(string.format("%g%%,%d\n", p, n))
    end
end

for _, _ in pairs({ 9, 9, 0, 90, 9, 89, 89, 8 }) do
    print('hello')
end
