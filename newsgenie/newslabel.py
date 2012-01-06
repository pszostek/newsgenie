#!/usr/bin/python
# -*- coding: utf-8 -*-

class NewsLabel(object):
    def __init__(self):
        pass
    def label(self):
        from dbfrontend import DBProxy
        db = DBProxy()
        news = db.get_all_news()
