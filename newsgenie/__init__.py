#!/usr/bin/python
# -*- coding: utf-8 -*-

import RssLib

rss_urls = [
#"http://wiadomosci.onet.pl/kraj/rss.xml", #polska
#"http://wiadomosci.onet.pl/swiat/rss.xml", #swiat
#"http://sport.onet.pl/wiadomosci/rss.xml", #sport
#"http://wiadomosci.wp.pl/kat,1356,ver,rss,rss.xml", #świat
##"http://wiadomosci.wp.pl/kat,1342,ver,rss,rss.xml", #polska
#"http://wiadomosci.wp.pl/kat,8131,ver,rss,rss.xml", #prasa
#"http://wiadomosci.wp.pl/kat,1355,ver,rss,rss.xml", #gospodarka
#"http://www.wp.pl/rss.xml?id=2", #sport
#"http://rss.gazeta.pl/pub/rss/wiadomosci_swiat.htm", #swiat
#"http://rss.gazeta.pl/pub/rss/wiadomosci_kraj.htm", #kraj
"http://gazeta.pl.feedsportal.com/c/32739/f/612804/index.rss", #sport
#"http://rss.feedsportal.com/c/32739/f/530278/index.rss", #gospodarka
#"http://www.tvn24.pl/polska.xml", #polska
#"http://www.tvn24.pl/swiat.xml", #swiat
#"http://www.tvn24.pl/sport.xml", #sport
#"http://www.tvn24.pl/biznes.xml", #gospodarka
]

from collections import namedtuple
RssEntry = namedtuple('RssEntry', ['title','link','date'], verbose=False)

news = []

try:
    for url in rss_urls:
        rss = RssLib.RssLib(url).read()
        news.extend(map(RssEntry._make, zip(rss["title"], rss["link"], rss["pubDate"])))
except RssLib.RssLibException as e:
    print e

import time, datetime

def convert_to_timestamp(rss_date):
    def calculate_offset(rss_date):
        if "GMT" in rss_date:
            rss_date = rss_date.rstrip("GMT")
            rss_date = rss_date.strip()
            return (rss_date,0)
        else:
            offset = rss_date[-5:]
            rss_date = rss_date[:-5]
            rss_date = rss_date.strip()
            if offset[0] == "-":
                return (rss_date,-3600*int(offset[1]))
            else:
                return (rss_date,3600*int(offset[1]))

    rss_date, offset = calculate_offset(rss_date)
    tf = "%a, %d %b %Y %H:%M:%S"
    ts = time.mktime(time.strptime(rss_date, tf))
    ts = int(ts) + offset
    return ts 
    
#for re in news:
#    print re.title, re.link, str(convert_to_timestamp(re.date))
from newsparse import NewsParserFactory 
from sanitizer import Sanitizer
npf = NewsParserFactory()

for rss_entry in news:
    from urllib2 import urlopen
    connection = urlopen(rss_entry.link)
    parser = npf.new(rss_entry.link)
    sanitizer = Sanitizer()
    encoding = connection.headers.getparam('charset')
    content = connection.read().decode(encoding)
    content = sanitizer.remove_js(content)
    #content = sanitizer.remove_blanks(content)
    body = parser.parse(content)
    print("\n\n" + unicode(rss_entry.link) + "\n" + unicode(body))