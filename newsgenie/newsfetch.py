#!/usr/bin/python
# -*- coding: utf-8 -*-

import RssLib


rss_urls = [
#ONET
"http://wiadomosci.onet.pl/kraj/rss.xml", #polska
"http://wiadomosci.onet.pl/swiat/rss.xml", #swiat
"http://sport.onet.pl/wiadomosci/rss.xml", #sport
#WIRTUALNA POLSKA
"http://wiadomosci.wp.pl/kat,1356,ver,rss,rss.xml", #świat
"http://wiadomosci.wp.pl/kat,1342,ver,rss,rss.xml", #polska
"http://wiadomosci.wp.pl/kat,8131,ver,rss,rss.xml", #prasa
"http://wiadomosci.wp.pl/kat,1355,ver,rss,rss.xml", #gospodarka
#GAZETA
"http://rss.gazeta.pl/pub/rss/wiadomosci_swiat.htm", #swiat
"http://rss.gazeta.pl/pub/rss/wiadomosci_kraj.htm", #kraj
"http://gazeta.pl.feedsportal.com/c/32739/f/612804/index.rss", #sport
"http://rss.feedsportal.com/c/32739/f/530278/index.rss", #gospodarka
#TVN24
"http://www.tvn24.pl/polska.xml", #polska
"http://www.tvn24.pl/swiat.xml", #swiat
"http://www.tvn24.pl/sport.xml", #sport
"http://www.tvn24.pl/biznes.xml", #gospodarka
#RZECZPOSPOLITA
"http://www.rp.pl/rss/2.html", #ogolne
"http://www.rp.pl/rss/10.html", #kraj
"http://www.rp.pl/rss/11.html", #swiat
"http://www.rp.pl/rss/12.html", #sport
"http://www.rp.pl/rss/5.html" #ekonomia
]

from collections import namedtuple
RssEntry = namedtuple('RssEntry', ['title','link','date'], verbose=False)

news = []
from sanitizer import Sanitizer
sanitizer = Sanitizer()

try:
    for url in rss_urls:
        print url
        rss = RssLib.RssLib(url).read()
        rss_date = [sanitizer.convert_to_timestamp(d) for d in rss["pubDate"]]
        new_bunch = map(RssEntry._make, zip(rss["title"], rss["link"], rss_date))
        new_bunch = [e for e in new_bunch if e.title and e.link and e.date]
        news.extend(new_bunch)
except RssLib.RssLibException as e:
    print e


    
#for re in news:
#    print re.title, re.link, str(convert_to_timestamp(re.date))
from newsparse import NewsParserFactory 
npf = NewsParserFactory()

for rss_entry in news:
    from urllib2 import urlopen
    connection = urlopen(rss_entry.link)
    parser = npf.new(rss_entry.link)
    encoding = connection.headers.getparam('charset')
    content = connection.read().decode(encoding)
    content = sanitizer.remove_js(content)
    #content = sanitizer.remove_blanks(content)
    body = parser.parse(content)
    print("\n\n" + unicode(rss_entry.link) + "\n" + unicode(body))
