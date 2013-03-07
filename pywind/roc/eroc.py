from datetime import datetime
from lxml import html
import urllib2

class EROCPrices(object):
    URL = "http://www.e-roc.co.uk/trackrecord.htm"

    def __init__(self):
        self.periods = {}
        self.get_prices()

    def get_prices(self):
        try:
            resp = urllib2.urlopen(self.URL)
        except:
            return

        def alltext(el):
            return (''.join(el.text_content())).strip()

        def process_table(tbl):
            for row in tbl.findall('.//tr'):
                datestr = alltext(row[0])
                if 'Auction Date' in datestr: continue
                try:
                    avg = float(alltext(row[1])[1:])
                    dt = datetime.strptime(datestr, "%d %B %Y")
                except ValueError:
                    continue
                numperiod = dt.year * 100 + dt.month
                if self.periods.has_key(numperiod):
                    self.periods[numperiod] = (self.periods[numperiod] + avg) / 2
                else:
                    self.periods[numperiod] = avg

        doc = html.parse(resp)
        for t in doc.findall('.//table'):
#            tr = t.findall('.//tr')
            if 'Auction Date' in alltext(t.findall('.//tr')[0]):
                process_table(t)


    def __getitem__(self, item):
        if self.periods.has_key(item):
            return self.periods[item]
        raise KeyError("No such period available [%s]" % item)
