#!/usr/bin/python
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser

class IParser():
    def __init__(self):
        self._parsed_body = None
        self._data = []

    def parse(self, s):
        if self._parsed_body is None:
            self._parsed_body = self._parse(s)
        return self._parsed_body

    def _parse(self):
        """Polymorphism"""

class GazetaParser(HTMLParser, IParser, object):
    def __init__(self):
        HTMLParser.__init__(self)
        IParser.__init__(self)
        self._inside_article = False
        self._inside_article_lead = False
        self._embedded_div = 0
        self._embedded_span = 0

    def handle_starttag(self, tag, attributes):
        if self._inside_article:
            if tag == "div":
                self._embedded_div += 1
            elif tag == "span":
                self._embedded_span += 1
            return
        if tag == 'div':
            for key, value in attributes:
                if key == 'id' and (value == "gazeta_article_lead" or value == "art"):
                    self._inside_article_lead = True
                elif key == 'id' and (value == "artykul" or value == "artykul_live"):
                    self._inside_article = True
        
    def handle_data(self, data):
        if self._inside_article or self._inside_article_lead:
            if self._embedded_div == 0 and self._embedded_span == 0:
                if data.strip():
                    self._data.append(data.strip())

    def handle_endtag(self,tag):
        if self._inside_article:
            if tag == "div":
                if self._embedded_div:
                    self._embedded_div -= 1
                else:
                    self._inside_article = False
            elif tag == "span":
                self._embedded_span -= 1
        elif tag == 'div' and self._inside_article_lead:
            self._inside_article_lead = False

    def _parse(self, s):
        self.reset()
        self._data = []
        try:
            self.feed(s)
        except Exception as e:
            print "DUPA" + str(e)
        return " ".join(self._data)

class TVN24Parser(HTMLParser, IParser, object):
    def __init__(self):
        HTMLParser.__init__(self)
        IParser.__init__(self)
        self._inside_skrot = False
        self._inside_tresc = False
        self._inside_script = False
        self._inside_strong = False
        self._embedded_div = 0
        self._embedded_span = 0
    
    def handle_starttag(self, tag, attributes):
        if self._inside_tresc:
            if tag == "strong":
                self._inside_strong = True
            elif tag == "div":
                self._embedded_div += 1
            elif tag == "span":
                self._embedded_span += 1
            return
        if tag == "div":
            for key, value in attributes:
                if key == "class" and value == "skrot":
                    self._inside_skrot = True
        if tag == "span":
            for key, value in attributes:
                if key == "class" and value == "tresc":
                    self._inside_tresc = True
        if tag == "script":
            self._inside_script = True

    def handle_endtag(self, tag):
        if tag == "strong":
            self._inside_strong = False
        elif tag == 'script':
            self._inside_script = False
        elif self._inside_skrot and tag == 'div':
            self._inside_skrot = False
        elif self._inside_tresc:
            if tag == 'span':
                if self._embedded_span == 0:
                    self._inside_tresc = False
                else:
                    self._embedded_span -= 1
    
    def handle_data(self, s):
        if self._inside_script or self._inside_strong:
            return
        if self._inside_skrot or self._inside_tresc:
            if s.strip():
                self._data.append(s.strip())

    def _parse(self, s):
        self.reset()
        self._data = [] 
        try:
            self.feed(s)
        except Exception as e:
            print e
        return " ".join(self._data)

class OnetParser(IParser, HTMLParser, object):
    def __init__(self):
        HTMLParser.__init__(self)
        IParser.__init__(self)
        self._inside_lead = False
        self._inside_intertext = False
        self._inside_script = False

    def handle_starttag(self, tag, attributes):
        if tag == "p":
            for key, value in attributes:
                if key == "class" and value == "k_lead":
                    self._inside_lead = True
        if tag == "span":
            for key, value in attributes:
                if key == "id" and value == "intertext_1":
                    self._inside_intertext = True
        if tag == "script":
            self._inside_script = True

    def handle_endtag(self, tag):
        if tag == "script":
            self._inside_script = False
        elif self._inside_lead and tag == "p":
            self._inside_lead = False
        elif self._inside_intertext and tag == "span":
            self._inside_intertext = False

    def handle_data(self, s):
        if self._inside_script:
            return
        if self._inside_lead or self._inside_intertext:
            if s.strip():
                self._data.append(s.strip())

    def _parse(self, s):
        self.reset()
        self._data = []
        try:
            self.feed(s)
        except Exception as e:
            print e
        return " ".join(self._data)

class WPParser(IParser, HTMLParser, object):
    def __init__(self):
        HTMLParser.__init__(self)
        IParser.__init__(self)
        self._inside_intertext = False
        self._inside_script = False
        self._embedded_div = 0

    def handle_starttag(self, tag, attributes):
        if self._inside_intertext and tag == "div":
            self._embedded_div += 1
        elif tag == "div":
            for key, value in attributes:
                if key == "id" and value == "intertext1":
                    self._inside_intertext = True
        elif tag == "script":
            self._inside_script = True

    def handle_endtag(self, tag):
        if tag == "script":
            self._inside_script = False
        elif self._inside_intertext and tag == "div":
            if self._embedded_div:
                self._embedded_div -= 1
            else:
                self._inside_intertext = False

    def handle_data(self, s):
        if self._inside_script or self._embedded_div:
            return
        if self._inside_intertext:
            if s.strip():
                self._data.append(s.strip())

    def _parse(self, s):
        self.reset()
        self._data = []
        try:
            self.feed(s)
        except Exception as e:
            print e
        return " ".join(self._data)

class UnknownSourceException:
    pass

class NewsParserFactory(object):
    def new(self,link):
        if "gazeta.pl" in link or "feedsportal" in link:
            return GazetaParser()
        elif "wp.pl" in link:
            return WPParser()
        elif "onet.pl" in link:
            return OnetParser()
        elif "tvn24.pl" in link:
            return TVN24Parser()
        else:
            raise UnknownSourceException()

if __name__=="__main__":
    from urllib2 import urlopen
    urls = ["http://wiadomosci.gazeta.pl/wiadomosci/1,114881,10792683,Rottweilery_zagryzly_w_Czechach_swoja_wlascicielke.html?utm_source=RSS&utm_medium=RSS&utm_campaign=10199882",
"http://www.tvn24.pl/12692,1727370,0,1,polacy-biedniejsi-niz-przed-rokiem,wiadomosc.html",
"http://wiadomosci.onet.pl/kraj/represjonowani-w-stanie-wojennym-spotkali-sie-w-il,1,4963280,wiadomosc.html",
"http://wiadomosci.gazeta.pl/wiadomosci/1,114881,10793499,W_redakcji__Nowej_Gaziety__nie_dzialaja_telefony_i.html?utm_source=RSS&utm_medium=RSS&utm_campaign=10199882",
"http://www.tvn24.pl/12692,1727379,0,1,pakt-fiskalny-przelamie-kryzys-damy-rade,wiadomosc.html"]
    npf = NewsParserFactory()
    for url in urls:
        connection = urlopen(url)
        parser = npf.new(url)
        encoding = connection.headers.getparam('charset')
        content = connection.read().decode(encoding)
        print("\n\n" + url + "\n" + parser.parse(content))
    