#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

WS = ' ' #word separator used in clean news' bodies
stopwords = [u"a", u"aby", u"ach", u"acz", u"aczkolwiek", u"aj", u"albo", u"ale", u"ależ", u"ani", u"aż",
u"bardziej", u"bardzo", u"bez", u"bo", u"bowiem", u"by", u"byli", u"bynajmniej", u"być", u"był", u"była",
u"było", u"były", u"będzie", u"będą", u"cali", u"cała", u"cały", u"ci", u"cię", u"ciebie", u"co", u"cokolwiek",
u"coś", u"czasami", u"czasem", u"czemu", u"czy", u"czyli", u"daleko", u"dla", u"dlaczego", u"dlatego", u"do",
u"dobrze", u"dokąd", u"dość", u"dużo", u"dwa", u"dwaj", u"dwie", u"dwoje", u"dziś", u"dzisiaj", u"gdy", u"gdyby",
u"gdyż", u"gdzie", u"gdziekolwiek", u"gdzieś", u"go", u"i", u"ich", u"ile", u"im", u"inna", u"inne", u"inny", u"innych",
u"iż", u"ja", u"ją", u"jak", u"jakaś", u"jakby", u"jaki", u"jakichś", u"jakie", u"jakiś", u"jakiż", u"jakkolwiek",
u"jako", u"jakoś", u"je", u"jeden", u"jedna", u"jedno", u"jednak", u"jednakże", u"jego", u"jej", u"jemu", u"jest",
u"jestem", u"jeszcze", u"jeśli", u"jeżeli", u"już", u"ją", u"każdy", u"kiedy", u"kilka", u"kimś", u"kto", u"ktokolwiek",
u"ktoś", u"która", u"które", u"którego", u"której", u"który", u"których", u"którym", u"którzy", u"ku", u"lat",
u"lecz", u"lub", u"ma", u"mają", u"mało", u"mam", u"mi", u"mimo", u"między", u"mną", u"mnie", u"mogą", u"moi", u"moim",
u"moja", u"moje", u"może", u"możliwe", u"można", u"mój", u"mu", u"musi", u"my", u"na", u"nad", u"nam", u"nami", u"nas",
u"nasi", u"nasz", u"nasza", u"nasze", u"naszego", u"naszych", u"natomiast", u"natychmiast", u"nawet", u"nią",
u"nic", u"nich", u"nie", u"niego", u"niej", u"niemu", u"nigdy", u"nim", u"nimi", u"niż", u"no", u"o", u"obok",
u"od", u"około", u"on", u"ona", u"one", u"oni", u"ono", u"oraz", u"oto", u"owszem", u"pan", u"pana", u"pani",
u"po", u"pod", u"podczas", u"pomimo", u"ponad", u"ponieważ", u"powinien", u"powinna", u"powinni", u"powinno",
u"poza", u"prawie", u"przecież", u"przed", u"przede", u"przedtem", u"przez", u"przy", u"roku", u"również",
u"sam", u"sama", u"są", u"się", u"skąd", u"sobie", u"sobą", u"sposób", u"swoje", u"ta", u"tak", u"taka",
u"taki", u"takie", u"także", u"tam", u"te", u"tego", u"tej", u"ten", u"teraz", u"też", u"to", u"tobą", u"tobie",
u"toteż", u"trzeba", u"tu", u"tutaj", u"twoi", u"twoim", u"twoja", u"twoje", u"twym", u"twój", u"ty", u"tych",
u"tylko", u"tym", u"u", u"w", u"wam", u"wami", u"was", u"wasz", u"wasza", u"wasze", u"we", u"według", u"wiele",
u"wielu", u"więc", u"więcej", u"wszyscy", u"wszystkich", u"wszystkie", u"wszystkim", u"wszystko", u"wtedy",
u"wy", u"właśnie", u"z", u"za", u"zapewne", u"zawsze", u"ze", u"zł", u"znowu", u"znów", u"został", u"żaden",
u"żadna", u"żadne", u"żadnych", u"że", u"żeby"]

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

    def remove_stopwords(self, list_of_words):
        return [word for word in list_of_words if word not in stopwords]

    def cleanup_news(self, news):
        news = news.split(" ")
        clean_news = self.remove_stopwords(list_of_words)
        return WS.join(clean_news)
