#!/usr/bin/python
# -*- coding: utf-8 -*-

from quick_orm.core import Database
from sqlalchemy import Column, String, Integer

class Cluster(object):
    __metaclass__ = Database.DefaultMeta
    name = Column(String)
    _center_str = Column(String)

    def number_of_news_containing(self, term):
        return len([n for n in self.news if term in n.vector])

    def number_of_news(self):
        return len(self.news)

@Database.foreign_key(Cluster)
class News(object):
    __metaclass__ = Database.DefaultMeta
    title = Column(String)
    body = Column(String)
    clean_body = Column(String) #news' body after stemming
    url = Column(String(150)) #news' location at actual media page
    date = Column(Integer) #issuing date as seconds from epoch
    _vector_str = Column(String) #vector for news algorithm representation

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
    """ Proxy for accessing SQLite DB """
    def __init__(self):
        self._db = Database("sqlite:///../news.db")
        #self._db.create_tables()
        self._news_gotten_from_db = False
        self._groups_gotten_from_db = False

    def __getattribute__(self, name):
        """proxy access to the list of kept news"""

        if name == "_news":
            if self._news_gotten_from_db == False:
                news = self._db.session.query(News).all()
                for n in news:
                    n.vector = self._deserialize(n._vector_str)
                self._news = news
                self._news_gotten_from_db = True
            return object.__getattribute__(self, "_news")
        elif name == "_groups":
            if self._groups_gotten_from_db == False:
                groups = self._db.session.query(Groups).all()
                for g in groups:
                    g.center = self._deserialize(g._center_str)
                    g.news = [n for n in self._news if n.cluster_id == g.id]
                self._groups = groups
                self._groups_gotten_from_db = True
        else:
            return object.__getattribute__(self, name)

    def get_all_news(self):
        return self._news

    def get_all_groups(self):
        return self._groups

    def get_sorted_news(self, field):
        return sorted(self._news, key=lambda n: n.__getattribute__(field))

    def count_news(self):
        """ return number of all news """
        return len(self._news)

    def delete_all_news(self):
        """ delete all news from the db """
        ret = len(self._news)
        for n in self._news:
            self._db.session.delete(n)
        self._news = []
        self._db.session.commit()
        return ret

    def delete_old_news(self, seconds):
        """remove all news from the database issued later than seconds ago"""
        import time
        cur_time = int(time.time())
        
        items_removed = 0
        new_list = []
        for n in self._news:
            if n.date + seconds < cur_time:
                self._db.session.delete(n)
                items_removed += 1
            else:
                new_list.append(n)
        self._db.session.commit()
        self._news = new_list
        return items_removed

    def delete_last_news(self, quantity):
        pass

    def add_news(self, news):
        """ add and commit a news to the databse """
        try:
            news._vector_str = self._serialize(news.vector)
        except:
            pass
        self._news.append(news)
        self._db.session.add_then_commit(news)


    def add_list_of_news(self, news):
        self._news.extend(news)
        for n in news:
            try:
                n._vector_str = self._serialize(n.vector)
            except:
                pass
            self._db.session.add(n)
        self._db.session.commit()

    def add_group(self, group):
        try:
            group._center_str = self._serialize(g.center)
        except:
            pass
        self._db.session.add_then_commit()

    def add_groups(self, groups):
        for g in groups:
            try:
                g._center_str = self._serialize(g.center)
            except:
                pass
            self._db.session.add(g)
        self._db.session.commit()

    def count_documents_containing(self, term):
        pass
    
    def dump_news(self):
        """ return all news in the database as a string """
        news = self.get_all_news()
        return '\n'.join([unicode(n) for n in news])

    def _deserialize(self, sth):
        try:
            import cPickle as pickle
        except:
            import pickle
        return pickle.loads(str(sth))

    def _serialize(self, sth):
        try:
            import cPickle as pickle
        except:
            import pickle
        return pickle.dumps(sth)

if __name__ == "__main__":
    db = DBProxy()
    
    news = News(title="sads", body="asdssd", clean_body="sadads", url="sss  a", date=1234)
    news.vector = {'dsdsa':1}
    db.add_news(news)
    print db.count_news()    
