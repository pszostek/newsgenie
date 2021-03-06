#!/usr/bin/python
# -*- coding: utf-8 -*-

import RssLib
from collections import namedtuple
from multiprocessing import Pool

def fetch_entry(url):
    import sanitizer
    sanitizer = sanitizer.Sanitizer()
    try:
        print "fetch_entry " + str(url)
        rss = RssLib.RssLib(url).read()
        rss_date = [sanitizer.convert_to_timestamp(d) for d in rss["pubDate"]]
        new_rss_entries = map(RssEntry._make, zip(rss["title"], rss["link"], rss_date))
        new_rss_entries = [e for e in new_rss_entries if e.title and e.url and e.date]
    except Exception, e:
        #LOG HERE
        print "fetch_entry exception " + str(url)
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

    try:
        print "fetch_news " + rss_entry.url
        connection = urlopen(rss_entry.url, timeout = 60)
        parser = npf.new(rss_entry.url)
        encoding = connection.headers.getparam('charset')
        content = connection.read().decode(encoding)
        content = sanitizer.remove_js(content)
       # content = sanitizer.remove_quotes(content)
        content = parser.parse(content)
        news = News(title=rss_entry.title, body=content,url=rss_entry.url, date=rss_entry.date)
    except Exception, e:
        #LOG HERE
        print "fetch_news exception"
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
  #  "http://gazeta.pl.feedsportal.com/c/32739/f/612804/index.rss", #sport
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
        rss_entries = [item for sublist in rss_entries if sublist for item in sublist if item ]

        pool.close()
        pool.join()

        return rss_entries

    def fetch_and_parse_news(self, rss_entries):
        """ Fetch news in a parallel way """
        from multiprocessing import Pool

        pool = Pool(processes=5)
        news = pool.map(fetch_news, rss_entries)
        news = [n for n in news if n]

        pool.close()
        pool.join()

        return news

    def run(self):
        from dbfrontend import DBProxy
        import sanitizer
        rss_entries = self.fetch_rss_entries()
        db = DBProxy()
        db_news = db.get_all_news()
        db_urls = [n.url for n in db_news]
        yet_unfetched_entries = [rss for rss in rss_entries if rss.url not in db_urls]
        unique_rss_entries = []

        for entry in yet_unfetched_entries:
            if entry.url not in [e.url for e in unique_rss_entries]:
                unique_rss_entries.append(entry)

        print "There are " + str(len(unique_rss_entries)) + " news entries" 
        news = self.fetch_and_parse_news(unique_rss_entries)
        print "Fetched "+ str(len(news)) + " news"
        news = [n for n in news if n]
        db.add_list(news)

if __name__ == "__main__":
    news_fetcher = NewsFetcher()
    news_fetcher.run()
