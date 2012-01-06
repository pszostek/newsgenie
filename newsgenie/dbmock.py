#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple

News = namedtuple("News", ['title','body','clean_body','url','date'], verbose=False)

from time import time

dirty_news="moja mama była w domu a tata gdzieś poszedł kraty były zamknięte ale to chyba nikogo nie"
"dziwi bo tak się zawsze robi to jest taka praktyka"

class m_news(object):
  bodies = ['dsa dsa fdasfsd gdfg dfg dfg fdgerg ghrhy etg ger gre ger',
  'dsa dsa fdasfsd gdfg dfg ee fdgerg fd etg ger gre asd',
  'dsa rer fdasfsd azz ghrhy etg ger gre ger',
  'dsa dsa fdas dfg dfg dfg  ger gre ger',
  'dsa fda ghrhy gdfg ger gre dsa',]
  def __init__(self):
    pass
  def __call__(self, arg):
    return News(title='abc', body=m_news.bodies[arg], clean_body=m_news.bodies[arg], url="http://dfsd.fd.com", date=int(time()))
  
from newsgroup import NewsGroup 
from sanitizer import Sanitizer
s=Sanitizer()
ng = NewsGroup()
m_news = m_news()
nr = [ng.quantity_reduce(m_news(i)) for i in range(0, len(m_news.bodies))]

print s.cleanup_news(dirty_news)
for i in range(0, len(m_news.bodies)):
  for j in range(i, len(m_news.bodies)):
    print "("+str(i)+","+str(j)+")"+str(ng.cosine_distance(nr[i], nr[j]))
print("jaccard")
nr = [ng.binary_reduce(m_news(i)) for i in range(0, len(m_news.bodies))]

for i in range(0, len(m_news.bodies)):
  for j in range(i, len(m_news.bodies)):
    print "("+str(i)+","+str(j)+")"+str(ng.jaccard_index(nr[i], nr[j]))
   
print len(ng.group(nr, 0.3, ng.jaccard_index))
print len(ng.group(nr, 0.4, ng.jaccard_index))