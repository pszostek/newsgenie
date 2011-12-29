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
	def __init__(self):
		self._db = Database("sqlite:///../news.db")
		self._db.create_tables()
	
	def get_all_news(self):
		news = db.session.query(News).all()
		return news

	def count_news(self):
		""" return number of all news """
		return self._db.session.query(News).count()

	def remove_old_news(self, seconds):
		"""remove all news from the database issued later than seconds ago"""
		import time		
		news = self.get_all_news()
		cur_time = int(time.time())
		
		items_removed = 0
		for n in news:
			if n.date + seconds < cur_time:
				self._db.session.remove_then_commit(n)
				items_removed += 1
		return items_removed

	def add_news(self, news):
		""" add and commit a news to the databse """
		self._db.session.add_then_commit(news)

	def dump_news(self):
		""" return all news in the database as a string """
		news = self.get_all_news()
		return '\n'.join(unicode(news))

if __name__ == "__main__":
    db = Database("sqlite:///../news.db")
    db.create_tables()
    
    #news = News(title="sads", body="asdsd", clean_body="sadads", url="as", date=1234)
    #db.session.add_then_commit(news)
    
    news = db.session.query(News).all()
    print "\n\n".join([str(n) for n in news])
