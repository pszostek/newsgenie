#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
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
            print rss_date
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