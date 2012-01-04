#!/usr/bin/python
# -*- coding: utf-8 -*-

import RssLib
from collections import namedtuple
from multiprocessing import Pool

def fetch_entry(url):
    import sanitizer
    sanitizer = sanitizer.Sanitizer()
    try:
        rss = RssLib.RssLib(url).read()
        rss_date = [sanitizer.convert_to_timestamp(d) for d in rss["pubDate"]]
        new_rss_entries = map(RssEntry._make, zip(rss["title"], rss["link"], rss_date))
        new_rss_entries = [e for e in new_rss_entries if e.title and e.url and e.date]
    except Exception, e:
        #LOG HERE
        print e
        return None
    return new_rss_entries

def fetch_news(rss_entry):
    import sanitizer
    from dbfrontend import News
    from urllib2 import urlopen
    from newsparse import NewsParserFactory
    sanitizer = sanitizer.Sanitizer()
    npf = NewsParserFactory()

    news = []
    try:
        connection = urlopen(rss_entry.url)
        parser = npf.new(rss_entry.url)
        encoding = connection.headers.getparam('charset')
        content = connection.read().decode(encoding)
        content = sanitizer.remove_js(content)
        content = parser.parse(content)
        clean_body = ""
        news = News(title=rss_entry.title, body=content, clean_body=clean_body, url=rss_entry.url, date=rss_entry.date)
    except Exception, e:
        #LOG HERE
        print e
        return None
    return news

RssEntry = namedtuple('RssEntry', ['title','url','date'], verbose=False)

class NewsFetcher(object):
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

    def __init__(self):
        pass

    def fetch_rss_entries(self):
        """ Fetch rss by running multiple instances of fetch_entry function """
        pool = Pool(processes=10)
        rss_entries = pool.map(fetch_entry, NewsFetcher.rss_urls)
        rss_entries = [item for sublist in rss_entries for item in sublist if item ]
        print len(rss_entries)
        return rss_entries

    def fetch_and_parse_news(self, rss_entries):
        """ Fetch news in a parallel way """
        from multiprocessing import Pool

        pool = Pool(processes=5)
        news = pool.map(fetch_news, rss_entries)
        print len(news)
        return news

    def run(self):
        from dbfrontend import DBProxy
        rss_entries = self.fetch_rss_entries()
        news = self.fetch_and_parse_news(rss_entries)
        for n in news:
            print n.title
            print n.body[0:100]
            print ""
        db = DBProxy()
        db.add_list_of_news_if_not_duped(news)

if __name__ == "__main__":
    news_fetcher = NewsFetcher()
    news_fetcher.run()