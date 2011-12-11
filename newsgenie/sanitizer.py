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