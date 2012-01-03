#!/usr/bin/python
# -*- coding: utf-8 -*-

import RssLib




from collections import namedtuple

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
        import sanitizer
        self._sanitizer = sanitizer.Sanitizer()
        
    def fetch_rss_entries(self):
        rss_entries = []

        try:
            for url in NewsFetcher.rss_urls:
                print url
                rss = RssLib.RssLib(url).read()
                rss_date = [self._sanitizer.convert_to_timestamp(d) for d in rss["pubDate"]]
                new_rss_entries = map(RssEntry._make, zip(rss["title"], rss["link"], rss_date))
                new_rss_entries = [e for e in new_rss_entries if e.title and e.url and e.date]
                rss_entries.extend(new_rss_entries)
        except RssLib.RssLibException as e:
            print e
        return rss_entries

    def fetch_news(self, rss_entries):
        from newsparse import NewsParserFactory
        from dbfrontend import News
            from urllib2 import urlopen
        npf = NewsParserFactory()

        news = []
        for rss_entry in rss_entries:
            try:
                connection = urlopen(rss_entry.url)
                parser = npf.new(rss_entry.url)
                encoding = connection.headers.getparam('charset')
                content = connection.read().decode(encoding)
                content = self._sanitizer.remove_js(content)
                #content = sanitizer.remove_blanks(content)
                body = parser.parse(content)
                #clean_body = stemmer.stem(body)
                clean_body = content
                news.append(News(title=rss_entry.title, body=content, clean_body=clean_body, url=rss_entry.url, date=rss_entry.date))
            except e:
                print e
        return news

if __name__ == "__main__":
    from dbfrontend import DBProxy
    nf = NewsFetcher()
    rss_entries = nf.fetch_rss_entries()
    news = nf.fetch_news(rss_entries)
    db = DBProxy()
    db.add_list_of_news_if_not_duped(news)
    #print("\n\n" + unicode(rss_entry.link) + "\n" + unicode(body))
        