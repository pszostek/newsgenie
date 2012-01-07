#!/usr/bin/python
# -*- coding: utf-8 -*-

from newsgroup import Group

class NewsLabel(object):
    def __init__(self):
        pass

    def label(self, number_of_terms):
        from dbfrontend import DBProxy
        db = DBProxy()
        news = db.get_all_news()
        clusters = db.get_all_groups()
        all_documents = len(news)
        

        for c in clusters: #iterate over all terms
            for term in c.center:
                docs_w_term_in_cluster = len([n for n in c.news if term in news.vector])
                docs_wo_term_in_cluster = len(c.news) - docs_w_term_in_cluster
                docs_w_term_o_cluster = 0
                for clus in  clusters:
                    docs_w_term_o_cluster += len([n for n in clus.news if term in n.vector])
                docs_w_term_o_cluster -= docs_w_term_in_cluster
                docs_wo_term_o_cluster = all_documents - docs_w_term_o_cluster - len(c.news)

                e_0_0 = 
                o_0_0 =
                x_0_0 =

                e_0_1 =
                o_0_1 =
                x_0_1 =

                e_1_0 =
                o_1_0 =
                x_1_0 =

                e_1_1 =
                o_1_1 =
                x_1_1 =

    def _documents_not_containing(self, group, term):
        ret = 0.0
        for news in group.news:
            if term not in news.vector:
                ret += 1.0
        return ret

    def _documents_containing(self, group, term):
        ret = 0.0
        for news in group.news:
            if term in news.vector:
                ret += 1.0
        return ret