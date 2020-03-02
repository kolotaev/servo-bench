import re
import argparse
from operator import itemgetter
import os.path

import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(description='Run plotting.')
parser.add_argument('-f', '--file', nargs='?', type=str, default='benchmark-results.md',
                    help='file with results of a benchmark (default: %(default)d)')
parser.add_argument('-d', '--dir', nargs='?', type=str, default='_images',
                    help='output dir (default: %(default)d)')
ARGS = parser.parse_args()


def generate_data_for_chart(file):
    bag = {}
    with open(file) as f:
        runs = re.split(r'====\nDate:', f.read())
        for run in runs:
            fr_m = re.search(r'Framework.*\|(.+)\|', run)
            endp_m = re.search(r'Endpoint.*\|(.+)\|', run)
            if fr_m and endp_m:
                fr = fr_m.group(1).strip()
                endp = endp_m.group(1).strip()
                if fr not in bag:
                    bag[fr] = {}
                if endp not in  bag[fr]:
                    bag[fr][endp] = []
                bag[fr][endp].append({
                    'lat-50': float(re.search(r"\('50',\s?'(.*)'\), \('70", run).group(1)),
                    'lat-90': float(re.search(r"\('99',\s?'(.*)'\), \('99\.9'", run).group(1)),
                    'reqs': round(float(re.search(r"Requests/sec.*\|(.+)\|", run).group(1))),
                    'cpu': round(float(re.search(r"CPU used \(mean\).*\|(.+)\|", run).group(1))),
                    'mem': round(float(re.search(r"Memory used \(mean\).*\|(.+)\|", run).group(1))),
                    'failed': round(float(re.search(r"5xx/4xx responses.*\|(.+)\|", run).group(1))),
                })
    return bag

def create_chart(data, outdir, name, endpoint='/db', stat_name='reqs', legend='RPS', color='gray'):
    xy = list(map(lambda x: {'res': max(data[x].get(endpoint, []), key=itemgetter(stat_name)).get(stat_name, 0), 'fr': x}, data.keys()))
    xy = sorted(xy, key=itemgetter('res'))
    frs = list(map(itemgetter('fr'), xy))
    y = list(map(itemgetter('res'), xy))
    for i, v in enumerate(y):
        plt.text(v + 3, i + 0, v)
    plt.barh(frs, y, color=color)
    plt.autoscale()
    plt.xlabel(legend)
    plt.title(name)
    plt.subplots_adjust(left=0.25)
    plt.savefig(os.path.join(outdir, name + '.png'), transparent=False)
    plt.cla()
    plt.clf()

def generate_all(in_file, outdir):
    data = generate_data_for_chart(in_file)
    create_chart(data, outdir, 'Requests per second DB (1 sec sleep)', endpoint='/db', stat_name='reqs', legend='Requests', color='#6497b1')
    create_chart(data, outdir, 'Memory usage DB', endpoint='/db', stat_name='mem', legend='Mb', color='#dec3c3')
    create_chart(data, outdir, 'CPU usage DB', endpoint='/db', stat_name='cpu', legend='%', color='#bbbbbb')
    create_chart(data, outdir, 'Failed requests DB', endpoint='/db', stat_name='failed', legend='requests', color='#ff6f69')
    create_chart(data, outdir, 'Latency for 50-percentile DB', endpoint='/db', stat_name='lat-50', legend='seconds', color='#3c2f2f')
    create_chart(data, outdir, 'Latency for 90-percentile DB', endpoint='/db', stat_name='lat-90', legend='seconds', color='#3385c6')

if __name__ == '__main__':
    generate_all(ARGS.file, ARGS.dir)
