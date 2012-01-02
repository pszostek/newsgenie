#!/usr/bin/python
# -*- coding: utf-8 -*-

from quick_orm.core import Database
from sqlalchemy import Column, String, Integer

class Cluster(object):
    __metaclass__ = Database.DefaultMeta
    name = Column(String)

@Database.foreign_key(Cluster)
class News(object):
    __metaclass__ = Database.DefaultMeta
    title = Column(String)
    body = Column(String)
    clean_body = Column(String) #news' body after stemming
    url = Column(String(150)) #news' location at actual media page
    date = Column(Integer) #issuing date as seconds from epoch

    def __unicode__(self):
        ret = str(self.id) + "\n"
        ret += self.title +"\n"
        ret +=self.url+ "\n"
        ret +=self.body + "\n"
        return ret

class DBHandler(object):
    """ Proxy for accessing SQLite DB """
    def __init__(self):
        self._db = Database("sqlite:///../news.db")
        #self._db.create_tables()
        self._news = []
        self._news_gotten_from_db = False

    def __getattribute__(self, name):
       if name == "_news":
           if self._news_gotten_from_db == False:
               self._news = self._db.session.query(News).all()
               self._news_gotten_from_db = True
           return object.__getattribute__(self, "_news")
       else:
           return object.__getattribute__(self, name)

    def get_all_news(self):
        return self._news

    def count_news(self):
        """ return number of all news """
        return len(self._news)

    def remove_old_news(self, seconds):
        """remove all news from the database issued later than seconds ago"""
        import time
        cur_time = int(time.time())
        
        items_removed = 0
        for n in self._news:
            if n.date + seconds < cur_time:
                self._db.session.remove_then_commit(n)
                self._news.remove(n)
                items_removed += 1
        return items_removed

    def add_news_if_not_duped(self, news):
        """ add and commit a news to the DB if is not duplicated """
        for saved_news in self._news:
            if news.url == saved_news.url:
                return False
        self.add_news(news)
        return True
        
    def add_news(self, news):
        """ add and commit a news to the databse """
        self._news.append(news)
        self._db.session.add_then_commit(news)

    def dump_news(self):
        """ return all news in the database as a string """
        news = self.get_all_news()
        return '\n'.join(unicode(news))

if __name__ == "__main__":
    db = DBHandler()
    
    news = News(title="sads", body="asdsd", clean_body="sadads", url="as", date=1234)
    db.add_news(news)
    print db.count_news()    
