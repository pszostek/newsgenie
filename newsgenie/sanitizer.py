#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

stopwords = ["a", "aby", "ach", "acz", "aczkolwiek", "aj", "albo", "ale", "ależ", "ani", "aż",
"bardziej", "bardzo", "bez", "bo", "bowiem", "by", "byli", "bynajmniej", "być", "był", "była",
"było", "były", "będzie", "będą", "cali", "cała", "cały", "chyba", "ci", "cię", "ciebie", "co", "cokolwiek",
"coś", "czasami", "czasem", "czem", "czy", "czyli", "daleko", "dla", "dlaczego", "dlatego", "do",
"dobrze", "dokąd", "dość", "dużo", "dwa", "dwaj", "dwie", "dwoje", "dziś", "dzisiaj", "gdy", "gdyby",
"gdyż", "gdzie", "gdziekolwiek", "gdzieś", "go", "i", "ich", "ile", "im", "inna", "inne", "inny", "innych",
"iż", "ja", "ją", "jak", "jakaś", "jakby", "jaki", "jakichś", "jakie", "jakiś", "jakiż", "jakkolwiek",
"jako", "jakoś", "je", "jeden", "jedna", "jedno", "jednak", "jednakże", "jego", "jej", "jem", "jest",
"jestem", "jeszcze", "jeśli", "jeżeli", "już", "ją", "każdy", "kiedy", "kilka", "kimś", "kto", "ktokolwiek",
"ktoś", "która", "które", "którego", "której", "który", "których", "którym", "którzy", "k", "lat",
"lecz", "lub", "ma", "mają", "mało", "mam", "mi", "mimo", "między", "mną", "mnie", "mogą", "moi", "moim",
"moja", "moje", "może", "możliwe", "można", "mój", "m", "musi", "my", "na", "nad", "nam", "nami", "nas",
"nasi", "nasz", "nasza", "nasze", "naszego", "naszych", "natomiast", "natychmiast", "nawet", "nią",
"nic", "nich", "nie", "niego", "niej", "niem", "nigdy", "nim", "nimi", "niż", "no", "o", "obok",
"od", "około", "on", "ona", "one", "oni", "ono", "oraz", "oto", "owszem", "pan", "pana", "pani",
"po", "pod", "podczas", "pomimo", "ponad", "ponieważ", "powinien", "powinna", "powinni", "powinno",
"poza", "prawie", "przecież", "przed", "przede", "przedtem", "przez", "przy", "rok", "również",
"sam", "sama", "są", "się", "skąd", "sobie", "sobą", "sposób", "swoje", "ta", "tak", "taka",
"taki", "takie", "także", "tam", "te", "tego", "tej", "ten", "teraz", "też", "to", "tobą", "tobie",
"toteż", "trzeba", "t", "tutaj", "twoi", "twoim", "twoja", "twoje", "twym", "twój", "ty", "tych",
"tylko", "tym", "", "w", "wam", "wami", "was", "wasz", "wasza", "wasze", "we", "według", "wiele",
"wiel", "więc", "więcej", "wszyscy", "wszystkich", "wszystkie", "wszystkim", "wszystko", "wtedy",
"wy", "właśnie", "z", "za", "zapewne", "zawsze", "ze", "zł", "znow", "znów", "został", "żaden",
"żadna", "żadne", "żadnych", "że", "żeby"]

abbreviations = ["al.","adm.","afryk.","alb.","alg.","amer.","ang.","arab.","argent.","arm.",
"art.","austr.","austral.","azer.","azerb.","azjat.","b","beng.","bp","bryt.","cieśn.","cz.m.",
"czes.","dn.","dol.","duń.","dzis.", "ds.","dr","el.","fr.","g.","gen.","gm.","gr.","g-y","hiszp.",
"hol.","im.","inst.","itd.","itp.","j.","jap.","jask.","k.","kan.","kl.","kol.","ks.","l.",
"lp.","łac.","łot.","marsz.","m.in.","mc","mies.-miesiąc","muzułm.","nadl.","ndm","niem.","np.",
"nr","o.","ob.","pers.","pl.","plut.","płk.","płw.","pol.","por.","ppor.","port.","pow.",
"przeł.","przyl.","pust.","p.o.","pw.","ppoż.","r.","ros.","rz.","s.","ss.","sierż.",
"sierż.","słow.","st.","st.","st.","st.","st.","st.","st.","śrdw.-łac.","św.","taj.",
"trb.","trl.","tys.","tzn.","tzw.","ukr.","ul.","ur.","w.","wdp.","wg","w.","wł.",
"właśc.","woj.","w-y","wyb.","zat.","zb.","zm."]

class GoogleSearch(object):
    GOOGLE_API_URL = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s&%s&%s&%s'
    GOOGLE_API_KEY = 'ABQIAAAAWxzylnyQ3kmXOQsTHcOpDBQIU6uL29HYXxXVHyHmw13EPtToKxQhUgekYLYIA4095rutV1Pi0Xz_VA'
    def __init__(self, phrase, pages = 1):
        import urllib
        import simplejson

        print phrase
        self._phrase = phrase 
        self._responseData = {}
        self._results = []
        query = urllib.urlencode({'q' : self._phrase})
        lang = urllib.urlencode({'hl':'pl'})
        key = urllib.urlencode({'key': GoogleSearch.GOOGLE_API_KEY})
        for i in range(0,pages):
            start = urllib.urlencode({'start': i})
            url = GoogleSearch.GOOGLE_API_URL % (query, lang, start, key)
            search_results = urllib.urlopen(url)
            json = simplejson.loads(search_results.read())
            print json
            self._responseData.update(json['responseData'])
            self._results.append(json['responseData']['results'])
        try:
            self._count = int(''.join(json['responseData']['cursor']['resultCount'].split()))
        except KeyError:
            self._count = 0
        
    def get_count(self):
        return self._count

    def get_urls(self):
        return [entry['url'] for page in self._results for entry in page ]

    def wiki(self):
        for entry in self.get_urls():
            if 'pl.wikipedia.org' in entry:
               entry = entry.split('/')
               return entry[-1]
        return None
    def get_phrase(self):
        return self._phrase
class WikiSearch(object):
    WIKI_API_URL = "http://pl.wikipedia.org/w/api.php?action=opensearch&%s"
    def __init__(self, phrase):
        import urllib
        import simplejson
        
        self._phrase = phrase
        self._results = []
        search = urllib.urlencode({"search": self._phrase})
        url = WikiSearch.WIKI_API_URL % search
        wiki_res = urllib.urlopen(url)
        json = simplejson.loads(wiki_res.read())
        print json
        self._results  = json[1]
    def get_results(self):
        return self._results
    def get_first_result(self):
        try:
            return self._results[0]
        except:
            return None
class Stemmer(object):
    def __init__(self):
        import os
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        pass

    def stem(self, list_of_words):
        from subprocess import Popen, PIPE
        stemmer = Popen(["java","-jar","../morfologik/morfologik-tools-1.5.2-standalone.jar","plstem"],
        shell=False, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        output = stemmer.communicate(" ".join(list_of_words))

        prev_word = None
        ret = []
        for line in (output[0].split("\n"))[:-2]:
            line = line.split("\t")
            if prev_word == line[0]:
                continue
            if line[1] == '-':
                pass #screw this word - is notrecognized by stemmer
            else:
                ret.append(line[1])
            prev_word = line[0]
        return ret

class Sanitizer(object):
    def remove_js(self, s):
        while True:
            start_index = s.find("<script")
            end_index = s.find("</script>")
            if start_index == -1 or end_index == -1:
                break
            text_before = s[:start_index]
            text_after = s[end_index+len("</script>"):]
            s = text_before + text_after
        return s

    def remove_blanks(self, s):
        last_char = None
        ret = ""
        for char in s:
            if char in ['\t',' ','\n'] and last_char == char:
                pass
            else:
                ret += char
        return ret

    def _calculate_date_offset(self, rss_date):
        if "GMT" in rss_date:
            rss_date = rss_date.rstrip("GMT")
            rss_date = rss_date.strip()
            return (rss_date,0)
        else:
            #date is like DDD, dd mmm yyyy hh:mm:ss +0100
            offset = rss_date[-5:]
            rss_date = rss_date[:-5]
            rss_date = rss_date.strip()
            if offset[0] == "-":
                return (rss_date,-3600*int(offset[1]))
            else:
                return (rss_date, 3600*int(offset[1]))

    def convert_to_timestamp(self, rss_date):
        if rss_date == '':
            from time import time
            return int(time())
        else:
            from time import mktime, strptime
            rss_date, offset = self._calculate_date_offset(rss_date)
            tf = "%a, %d %b %Y %H:%M:%S"
            ts = mktime(strptime(rss_date, tf))
            ts = int(ts) + offset
            return ts

    def _lower(self, list_of_words):
        ret = []
        for word in list_of_words:
            ret.append(word.lower())
        return ret

    def _remove_stopwords(self, list_of_words):
        return [word for word in list_of_words if word not in stopwords]

    def _remove_abbreviations(self, text):
        words = text.split(" ")
        return " ".join([word for word in words if word not in abbreviations])

    def _remove_punctuation(self, text):
        from string import punctuation
        ret = text
        for p in punctuation:
            ret = ret.replace(p,'')
        return ret

    def _remove_trailing_dot(self, text):
        if len(text) == 0:
            return text
        elif text[-1] == '.':
            return text[:-1]
        else:
            return text

    def _divide_into_sentences(self, text):
        from string import ascii_uppercase as UC
        UC = UC + "ŁŻŹĄĆĘÓ"
        temp = []

        last_cut = -1
        for index in range(0, len(text)):
            try:
                if text[index] in '.?!' and text[index+1].isspace():
                    temp.append(text[last_cut+1:index]) #screw the '.','?' or '!'
                    last_cut = index
            except IndexError:
                temp.append(text[last_cut+1:])
                break
        if len(temp) == 0:
            temp.append(text)
        ret = []
        for s in temp:
            ret.append([w for w in s.split(" ") if w])
        return [s for s in ret if s]

    def _extract_title(self, sentence, index):
        from string import ascii_uppercase as UC
        UC = UC + "ŁŻŹĄĆĘÓ"
        ret = [sentence[index]]
        while True:
            index = index+1
            try:
                if sentence[index][0] in UC:
                    ret.append(sentence[index])
                else:
                    break
            except:
                break
        return " ".join(ret)
        
    def _istitle(self, text):
        from string import ascii_uppercase as UC
        return (text[0] in UC) or (text[0]=='"' and text[1] in UC)
    def _find_eigennames(self, text):
        from string import ascii_uppercase as UC
        UC = UC + "ŁŻŹĄĆĘÓ".decode("utf-8")
        from collections import defaultdict
        eigennames = defaultdict(int) 
        text = text.replace(',', '')
        text = text.replace(':', '')
        print text
        sentences = self._divide_into_sentences(text)
        
        istitle = self._istitle
        #first iteration
        for sentence in sentences:
            #print "s" + str(sentence)
            inside_long_name = False
            for index in range(2, len(sentence)): #start with third word (first is capital)
                try:
                    if sentence[index].decode("utf-8")[0] in UC:
                        if not inside_long_name:
                            try:
                                if sentence[index+1].decode("utf-8")[0] in UC: #two capitals in a row - long name
                                    name = self._extract_title(sentence, index) stworzyć osobną kategorię dla długich
                                    inside_long_name = True
                                else:
                                    name = sentence[index] #short name
                            except IndexError:
                                name = sentence[index]
                            if name.lower() not in stopwords: #dont accept stopwords written in capital
                                eigennames[name] += 1
                        else:
                            continue
                    else:
                        inside_long_name = False
                except IndexError:
                    pass

        #second iteration - find words after dots that were stated eigennames in the first pass
        suspected = defaultdict(int)
        for sentence in sentences:
            if sentence[0].decode("utf-8")[0] in UC:
                if sentence[0] in eigennames.keys(): #if already found elsewhere -> add
                    eigennames[sentence[0]] += 1
                try:
                    if sentence[1].decode("utf-8")[0] in UC: #if the second word is also capital -> extract long name
                        title = self._extract_title(sentence, 0)
                        suspected[title] += 1
                    else:
                        if sentence[0].lower() not in stopwords:
                            suspected[sentence[0]] += 1
                except IndexError: #there is no second word
                    suspected[sentence[0]] += 1
        #third phase
        from xgoogle.search import GoogleSearch
        for name in suspected:
            try:
                w = GoogleSearch(name)
                w._lang = "pl"
                res = w.get_results()
            except:
                print "Can't acces google for lookup: " + name
                res = []
            if self._wiki_lookup(res):
                sum = suspected[name] + eigennames[name]
                eigennames.pop(name)
                eigennames[name] = sum
        
        names_wiki = defaultdict(list)
        for name in eigennames:
            try:
                w = GoogleSearch(name)
                w._lang = "pl"
                res = w.get_results()
            except:
                print "Can't acces google for lookup: " + name
                res = []
            names_wiki[self._wiki_lookup(res)].append(name)
            #names_wiki[w.get_first_result()].append(name)

        ret = defaultdict(int)
        for wiki_name, names in names_wiki.items():
            if wiki_name == None:
                for n in names:
                    ret[n.decode("utf-8")] = eigennames[n]
            else:
                ret[wiki_name] = 0
                for name in names:
                    ret[wiki_name] += eigennames[name]
        #fourth phase
        for name in sorted(eigennames.keys(), key=len, reverse=True):
            print name
            text = text.replace(name, '')
        from pprint import pprint
        return (text, ret)

    def _wiki_lookup(self,  results):
        from urllib import url2pathname
        for res in results:
            if 'pl.wikipedia.org' in res.url:
                url = res.url.split("/")
                url = url[-1].replace('_', ' ')
                try:
                    url = url2pathname(url)
                except:
                    pass
                return url
        return None
    def remove_quotes(self, content):
        return content.replace('a""', 'a"')
    def _cleanup_text(self, text):
        from pprint import pprint
        text = self._remove_abbreviations(text)
        text, eigennames = self._find_eigennames(text)
        text = self._remove_punctuation(text)
        words = text.split()
        words = self._lower(words)
        stem = Stemmer()
        words = stem.stem(words)
        words = self._remove_stopwords(words)
        words = [w.decode("utf-8") for w in words]
        return words, eigennames

    def run(self):
        from collections import defaultdict
        from dbfrontend import DBProxy
        db = DBProxy()
        news = db.get_all_news()
        news = [n for n in news if not n.clean_body and n.body]
        for n in news:
            (words_body, names_body) = self._cleanup_text(n.body.encode("utf-8"))
            (words_title, names_title) = self._cleanup_text(n.title.encode("utf-8"))
            n.clean_body = words_body
            n.clean_title = words_title
            n.eigennames = defaultdict(int)
            for name, num in names_title.items():
                n.eigennames[name] += num
            for name, num in names_body.items():
                n.eigennames[name] += num
            db.add(n)

if __name__ == "__main__":
    s = Sanitizer()
    s.run()
