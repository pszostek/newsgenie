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
    clean_body = Column(String)
    url = Column(String(150))
    date = Column(Integer)

    def __str__(self):
        ret = str(self.id) + "\n"
        ret += self.title +"\n"
        ret +=self.url+ "\n"
        ret +=self.body + "\n"
        return ret

if __name__ == "__main__":
    db = Database("sqlite:///../news.db")
    db.create_tables()
    
    #news = News(title="sads", body="asdsd", clean_body="sadads", url="as", date=1234)
    #db.session.add_then_commit(news)
    
    news = db.session.query(News).all()
    print "\n\n".join([str(n) for n in news])