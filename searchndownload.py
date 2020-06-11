import os
import random
import urllib.request
from optparse import OptionParser

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
            terms = pytrend.trending_searches(pn=country).values.tolist()
            for term in terms:
                inp.append(term[0])

    if not os.path.exists(out):
        os.makedirs(out)

    with open('list-{}.txt'.format(ext), 'w') as l:
        for query in inp:
            print('Searching for: %s' % query)
            for url in search('filetype:%s %s' % (ext, query), num=n, stop=10, pause=2):
                name = url.split('/')[-1]
                fext = name.split('.')[-1]

                if fext != ext:
                    continue

                try:
                    r = urllib.request.urlopen(url)
                except Exception as e:
                    print(e)
                    continue

                datatowrite = r.read()

                if os.path.isfile(os.path.join(out, name)):
                    names = name.split('.')
                    names[-2] = names[-2] + str(random.randint(1, 10000))
                    name = '.'.join(names)

                with open(os.path.join(out, name), 'wb') as f:
                    f.write(datatowrite)

                l.write(os.path.abspath(os.path.join(out, name)) + '\n')


if __name__ == '__main__':
    parser.add_option('-e', '--extension', help='select an extension to download')
    parser.add_option('-i', '--input', help='select input query', default="")
    parser.add_option('-n', '--number', help='select number of output', default=10)
    parser.add_option('-o', '--output', help='location for downloaded files', default="downloaded")
    main()
