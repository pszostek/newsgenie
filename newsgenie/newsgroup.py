#!/usr/bin/python
# -*- coding: utf-8 -*-


from collections import namedtuple
from dbfrontend import News, Cluster

class NewsGroup(object):
    TITLE_WEIGHT = 3
    BODY_WEIGHT = 1
    def __init__(self):
        pass

    def quantity_reduce(self, list_of_words):
        """ make a binary vector from a text corpus """
        from collections import defaultdict
        ret = defaultdict(in) 
        if len(list_of_words) == 0:
            raise RuntimeError

        for word in list_of_words:
            ret[word] += 1
        return ret

    def binary_reduce(self, list_of_words):
        """ make a quantity vector from a text corpus """
        ret = {}
        for word in list_of_words:
            ret[word] = 1
        return ret

    def cosine_distance(self, v1, v2):
        from pprint import pprint
        pprint(v1)
        pprint(v2)
        scalar_product = 0
        v1_length = 0
        v2_length = 0
        words = list(set(v1.keys() + v2.keys()))

        for word in v1.keys():
            if word in v2.keys():
                scalar_product += v1[word]*v2[word]
            v1_length += v1[word]**2.0

        for word in v2.keys():
            v2_length += v2[word]*2.0

        from math import sqrt
        return float(scalar_product)/(sqrt(v1_length)*sqrt(v2_length))

    def jaccard_index(self, v1, v2):
        v1_and_v2 = [w for w in v1.keys() if w in v2.keys()]
        v1_or_v2 = list(set(v1.keys() + v2.keys()))
        return float(len(v1_and_v2))/float(len(v1_or_v2))

    def _add_and_recalculate_cluster(self, cluster, news):
        from collections import defaultdict
        result = defaultdict(int)
        for word in cluster.center.keys():
            result[word] = len(cluster.newss.all())*cluster.center[word]
        for word in news.vector:
            result[word] += news.vector[word]

        for word in result:
            result[word] /= len(cluster.newss.all()) + 1

        cluster.center = result
        news.cluster_id = cluster.id

    def _merge_clusters(self, g1, g2):
        result = {}
        g1_len = len(g1.newss.all())
        g2_len = len(g2.newss.all())
        ##calculate the new center as a weigthed mean value of both centers
        for word in g1.center.keys():
            result[word] = g1_len*g1.center[word]
        for word in g2.center.keys():
            if word in result:
                result[word] += g2_len*g2.center[word]
            else:
                result[word] = g2_len*g2.center[word]
        result_len = g1_len + g2_len
        for word in result:
            result[word] /= result_len
        #new group consists of news taken from both groups
        new_clusters_news = g1.newss.all() + g2.newss.all()
        ret = Cluster(center = result)
        for n in new_clusters_news:
            n.cluster_id = ret.id
        db.add_list(new_clusters_news)
        return ret
    
    def group(self, db, list_of_news, threshold, distance_function):
        if len(list_of_news) == 0:
            raise RuntimeError("List of news cannot be empty")
        # step 1: create set of news being grouped
        ungrouped  = list_of_news

        clusters = []
        # step 2: take the first news, let it be a seed of the first group
        c = Cluster(newss=[list_of_news[0]], center=list_of_news[0].vector)
        clusters.append(c)
        ungrouped = ungrouped[1:]
        # step 3: for each ungrouped element find its distance from
        #         center of each group. If for at least one group the distance
        #         is smaller than a threshold, assign this element to a group
        #         and recalculate group's center
        for elem in ungrouped:
            print "grouping " + elem.title
            min_dist = 0
            best_cluster = None
            for cluster in clusters:
                dist = distance_function(elem.vector, cluster.center)
                if dist < threshold: #choose this group for merge
                    if best_cluster == None: # no best group for this element
                       best_cluster = cluster 
                       min_dist = dist
                    else:
                        if dist < min_dist:
                            best_cluster = cluster
                            min_dist = dist
                        else:
                            pass #there already chosen group is better
            if best_cluster == None:
                c = Cluster(newss=[elem], center=elem.vector)
                elem.cluster = c
                clusters.append(c)
                db.add(elem)
            else:
                self._add_and_recalculate_cluster(best_cluster, elem)
                elem.cluster = best_cluster
                db.add(elem)

        print "Created " + str(len(clusters)) + " clusters"
        # step 4: if distance of two groups is smaller than a threshold,
        # merge these two groups and calculate the new center
        any_changes = True
        while any_changes == True:
            any_changes = False
            pairs_of_clusters = []
            for p1 in range(len(clusters)):
                for p2 in range(p1+1, len(clusters)):
                    pairs_of_clusters.append((clusters[p1], clusters[p2]))
            for c1, c2 in pairs_of_clusters:
                dist = distance_function(c1.center, c2.center)
                if dist < threshold:
                    any_changes = True
                    c_result = self._merge_clusters(db, c1, c2)
                    clsters.remove(c1)
                    clusters.remove(c2)
                    clusters.append(c_result)
        return clusters

    def run(self, distance_function, reduce_function, threshold):
        from dbfrontend import DBProxy
        db = DBProxy()
        db.delete_all_clusters()
        news = db.get_all_news()
        tw = NewsGroup.TITLE_WEIGHT
        bw = NewsGroup.BODY_WEIGHT
        for n in news:
            a = reduce_function(n.clean_body)
            b = reduce_function(n.clean_title)
            n.vector = dict( (n, bw*a.get(n, 0)+tw*b.get(n, 0)) for n in set(a)|set(b) )
        clusters = self.group(db, news, threshold, distance_function)
        db.add_list(clusters)
        return clusters
        
if __name__ == "__main__":
    news_grouper = NewsGroup()
    news_grouper.run(news_grouper.cosine_distance, news_grouper.quantity_reduce, 0.4)