#!/usr/bin/python
# -*- coding: utf-8 -*-


from collections import namedtuple
from sanitizer import WS
Group = namedtuple('Group', ['center', 'news'], verbose=False)

class NewsGroup(object):
    def __init__(self):
        pass

    def quantity_reduce(self, news, ngram=1):
        """ make a binary vector from a text corpus """
        ret = {}
        if len(news.clean_body) == 0:
            raise RuntimeError

        body = news.clean_body.split(WS)
        for word in body:
            try:
                ret[word] += 1
            except:
                ret[word] = 1
        return ret

    def binary_reduce(self, news, ngram=1):
        """ make a quantity vector from a text corpus """
        ret = {}
        body = news.clean_body.split(WS)
        for word in body:
            ret[word] = 1
        return ret

    def cosine_distance(self, v1, v2):
        scalar_product = 0
        v1_length = 0
        v2_length = 0
        words = list(set(v1.keys() + v2.keys()))

        for word in v1.keys():
            if word in v2.keys():
                scalar_product += v1[word]*v2[word]
            v1_length += v1[word]*v1[word]

        for word in v2.keys():
            v2_length += v2[word]*v2[word]

        from math import sqrt
        return float(scalar_product)/(sqrt(v1_length)*sqrt(v2_length))

    def jaccard_index(self, v1, v2):
        v1_and_v2 = [w for w in v1.keys() if w in v2.keys()]
        v1_or_v2 = list(set(v1.keys() + v2.keys()))
        return float(v1_and_v2)/float(v1_or_v2)

    def _recalculate_group_after_add(self, group, vector):
        result = {}
        for word in group.center.keys():
            result[word] = len(group.news)*group.center[word]
        if word in result:
            result[word] += vector[word]
        else:
            result[word] = vector[word]

        for word in result:
            result[word] /= len(group.news) + 1

        #group's will be change externaly
        group.center = result
        #no return

    def _merge_groups(self, g1, g2):
        result = {}
        g1_len = len(g1.news)
        g2_len = len(g2.news)
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
        new_group_news = g1.news + g2.news
        ret = Group(center = result, news = new_group_news)
        return ret
    
    def group(self, list_of_vectors, threshold, distance_function):
        if len(list_of_vectors) == 0:
            raise RuntimeError("List of news cannot be empty")
        # step 1: create set of news being grouped
        ungrouped  = list_of_vectors

        groups = []
        # step 2: take the first news, let it be a seed of the first group
        g = Group(news=list(list_of_vectors[0]), center=list_of_vectors[0])
        groups.append(g)
        ungrouped = ungrouped[1:]
        # step 3: for each ungrouped element find its distance from
        #         center of each group. If for at least one group the distance
        #         is smaller than a threshold, assign this element to a group
        #         and recalculate group's center
        next_ungrouped = []
        for elem in ungrouped:
            min_dist = 0
            best_group = None
            for group in groups:
                dist = distance_function(elem, group.center)
                if dist < threshold:
                    if best_group == None: # no best group for this element
                       best_group = group
                       min_dist = dist
                    else:
                        if dist < min_dist:
                            best_group = group
                            min_dist = dist
            if best_group == None:
                g = Group(news=list(elem), center=elem)
                groups.append(g)
            else:
                best_group.news.append(elem)
                self._recalculate_group_after_add(best_group, elem)

        # step 4: if distance of two groups is smaller than a threshold,
        # merge these two groups and calculate the new center


            any_changes = True
            while any_changes == True:
                any_changes = False
                pairs_of_groups = []
                for p1 in range(len(groups)):
                    for p2 in range(p1+1, len(groups)):
                        pairs_of_groups.append((groups[p1], groups[p2]))
                for g1, g2 in pairs_of_groups:
                    dist = distance_function(g1.center, g2.center)
                    if dist < threshold:
                        any_changes = True
                        g = self._merge_groups(g1,g2)
                        groups.remove(g1)
                        groups.remove(g2)
                        groups.append(g)
        return groups