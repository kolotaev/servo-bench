-- example reporting script which demonstrates a custom
-- done() function that prints latency percentiles

done = function(summary, latency, requests)
    io.write("------------------------------\n")
    for _, p in pairs({ 50, 70, 90, 99, 99.9, 99.999 }) do
        n = latency:percentile(p)
        io.write(string.format("Latency percentile %g%%, %.03f (sec.)\n", p, n / 1000000))
    end
    io.write("------------------------------\n")
end
