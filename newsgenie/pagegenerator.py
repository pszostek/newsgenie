#!/usr/bin/python
# -*- coding: utf-8 -*-

class PageGenerator(object):
    def __init__(self):
        pass

    def run(self):
        from dbfrontend import DBProxy
        db = DBProxy()
        clusters = db.get_all_clusters()
        for cluster in clusters:
            print "Cluster " + str(clusters.index(cluster))
            for n in cluster.newss.all():
                print "   " + n.title
            print ""

if __name__ == "__main__":
    pg = PageGenerator()
    pg.run()
