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

    def __eq__(self, other):
        return self.url == other.url

class DBProxy(object):
    """ Proxy for accessing SQLite DB """
    def __init__(self):
        self._db = Database("sqlite:///../news.db")
        #self._db.create_tables()
        self._news = []
        self._news_gotten_from_db = False

    def __getattribute__(self, name):
        """proxy access to the list of kept news"""
        if name == "_news":
            if self._news_gotten_from_db == False:
                self._news = self._db.session.query(News).all()
                self._news_gotten_from_db = True
            return object.__getattribute__(self, "_news")
        else:
            return object.__getattribute__(self, name)

    def get_all_news(self):
        return self._news

    def get_sorted_news(self, field):
        return sorted(self._news, key=lambda n: n.__getattribute__(field))
    
    def count_news(self):
        """ return number of all news """
        return len(self._news)

    def delete_old_news(self, seconds):
        """remove all news from the database issued later than seconds ago"""
        import time
        cur_time = int(time.time())
        
        items_removed = 0
        for n in self._news:
            if n.date + seconds < cur_time:
                self._db.session.delete(n)
                self._db.session.commit()
                self._news.remove(n)
                items_removed += 1
        return items_removed

    def add_news_if_not_duped(self, news):
        """ add and commit a news to the DB if is not duplicated """
        for saved_news in self._news:
            if saved_news == news:
                return False
        self.add_news(news)
        return True

    def add_news(self, news):
        """ add and commit a news to the databse """
        self._news.append(news)
        self._db.session.add_then_commit(news)

    def add_list_of_news(self, news):
        self._news.extend(news)
        for n in news:
            self._db.session.add(n)
        self._db.session.commit()

    def add_list_of_news_if_not_duped(self, news):
        news = list(set(self._news).difference_update())
        return self.add_list_of_news(news)

    def dump_news(self):
        """ return all news in the database as a string """
        news = self.get_all_news()
        return '\n'.join(unicode(news))

if __name__ == "__main__":
    db = DBProxy()
    
    news = News(title="sads", body="asdsd", clean_body="sadads", url="as", date=1234)
    db.add_news(news)
    print db.count_news()    
