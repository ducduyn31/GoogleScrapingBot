import os
from optparse import OptionParser

import urllib.request
from googlesearch import search
from pytrends.request import TrendReq

parser = OptionParser()

countries = ['india', 'united_states', 'japan', 'united_kingdom', 'france', 'vietnam', 'indonesia', 'brazil',
             'south_korea', 'canada', 'australia', 'mexico']


def main():
    (options, args) = parser.parse_args()
    ext = options.extension
    inp = [options.input] if options.input else []
    n = int(options.number)
    out = options.output
    if len(inp) == 0:
        pytrend = TrendReq()
        inp = []
        for country in countries:
            inp += pytrend.trending_searches(pn=country).values.tolist()

    if not os.path.exists(out):
        os.makedirs(out)

    with open('list.txt', 'w') as l:
        for query in inp:
            for url in search('filetype:%s %s' % (ext, query), num=n, stop=10, pause=2):
                name = url.split('/')[-1]
                print(url)
                try:
                    r = urllib.request.urlopen(url)
                except Exception as e:
                    print(e)
                    continue

                datatowrite = r.read()

                with open(os.path.join(out, name), 'wb') as f:
                    f.write(datatowrite)

                l.write(os.path.abspath(os.path.join(out, name)) + '\n')


if __name__ == '__main__':
    parser.add_option('-e', '--extension', help='select an extension to download')
    parser.add_option('-i', '--input', help='select input query', default="")
    parser.add_option('-n', '--number', help='select number of output', default=10)
    parser.add_option('-o', '--output', help='location for downloaded files', default="downloaded")
    main()
