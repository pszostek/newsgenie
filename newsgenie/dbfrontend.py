#!/usr/bin/python
# -*- coding: utf-8 -*-

from quick_orm.core import Database
from sqlalchemy import Column, String, Integer, PickleType

class Cluster(object):
    __metaclass__ = Database.DefaultMeta
    name = Column(String)
    center = Column(PickleType)

    def number_of_news_containing(self, term):
        return len([n for n in self.newss.all() if term in n.vector])

    def number_of_news(self):
        return len(self.news)

@Database.foreign_key(Cluster)
class News(object):
    __metaclass__ = Database.DefaultMeta
    title = Column(String)
    body = Column(String)
    url = Column(String(150)) #news' location at actual media page
    clean_title = Column(PickleType) #list of words
    clean_body = Column(PickleType) #list of words
    date = Column(Integer) #issuing date as seconds from epoch
    vector = Column(PickleType) #vector for news algorithm representation
    eigennames = Column(PickleType) #dictionary of (name:quantity)

    def __unicode__(self):
        ret = str(self.id) + "\n"
        ret += str(self.title) +"\n"
        ret += str(self.url) + "\n"
        ret += str(self.body) + "\n"
        ret += str(self.vector) +"\n"
        return ret

    def __eq__(self, other):
        return self.url == other.url

    def __hash__(self):
        return hash(self.url)

class DBProxy(object):
    def __init__(self):
        self._db = Database("sqlite:///../news.db")

    def get_all_news(self):
        return self._db.session.query(News).all()

    def get_all_clusters(self):
        return self._db.session.query(Cluster).all()

    def delete_all_clusters(self):
        for c in self.get_all_clusters():
            self._db.session.delete(c)
        self._db.session.commit()

    def delete_all_news(self):
        for n in self.get_all_news():
            self._db.session.delete(n)
        self._db.session.commit()

    def delete_old_news(self, seconds):
        from time import time
        cur_time = int(time())
        items_removed = 0

        for n in self.get_all_news():
            if n.date + seconds < cur_time:
                self._db.session.delete(n)
                items_removed += 1
        self._db.session.commit()
        return items_removed

    def add(self, sth):
        self._db.session.add_then_commit(sth)

    def add_list(self, list_of_sth):
        for item in list_of_sth:
            self._db.session.add(item)
        self._db.session.commit()

    def count_news(self):
        return len(self.get_all_news())

if __name__ == "__main__":
    db = DBProxy()
    
    news = News(vector={"dsd":11},title="sads", body="asdssd", clean_body="sadads", url="sss  a", date=1234)
    db.add(news)
    print db.count_news()    
