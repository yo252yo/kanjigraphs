# -*- coding: utf-8 -*-
from graphviz import Graph
from collections import defaultdict
import random
import math


class Keywords(object):
    def labelof(keywords, kw, data):
        if len(kw) > 1:
            return ("<b>" + kw + "</b>\n " + str(keywords[kw]))
        else:
            return data.descriptions[kw]

    def graph(data):
        print("Printing keywords")
        dot = Graph(comment='Kanjis', strict=True)
        dot.engine = 'neato'
        dot.format = 'svg'
        dot.attr(overlap="porthoy", sep="-0.1", outputorder="edgesfirst")
        dot.attr('node', fontsize='30')
        similaredges = defaultdict(set)

        kanjis = set()
        keywords = {}
        all_kw = []

        # build a list of keywords, keyword -> full string of KW
        for kanji in data.kanjis:
            kanjis.add(kanji)
            if kanji in data.keywords:
                for kw in data.keywords[kanji]:
                    l = kw.split(" ")
                    if not l[0] in keywords:
                        keywords[l[0]] = kw
                        all_kw.append(l[0])
            else: # kanjis that dont have keywords are their own keywords
                keywords[kanji] = data.descriptions[kanji]


        for kanji in kanjis:
            ease = data.rattrapage[kanji] / 10
            fcolor = "0 0 " + str(1-(0.1 + 0.2 * ease))# + " 0.5"

            bgcolor = data.colors[kanji]
            if bgcolor.startswith("0.6"):
                bgcolor =  '0.6 ' + str(1-(0.6 + 0.4 * ease)) + ' 1.0'

            shape = "circle"
            color = fcolor
            if (data.rattrapage[kanji] < 8):
                shape = "doublecircle"
                color = "red"

            # Link all kw of a kanji
            if kanji in data.keywords:
                # should we still plot the kanji node if the KW has only one kanji and kanas?
                # we could not do that if we make sure that the KW node key is only kanjis
                dot.node(data.descriptions[kanji], label=kanji, shape=shape, color=color, fontcolor=fcolor, fontsize='15', fillcolor=bgcolor, style='filled')

                for kw in data.keywords[kanji]:
                    l = kw.split(" ")
                    if not l[0]:
                        continue
                    if not l[0] in keywords:
                        keywords[l[0]] = kw
                    dot.edge(data.descriptions[kanji], Keywords.labelof(keywords, l[0], data), len="0.5", color="green", penwidth="3")#.decode('utf-8')

            for similar in (data.similars[kanji]):# + data.semilars[kanji]
                if not similar in kanjis:
                    continue
                if not similaredges[kanji] or not similar in similaredges[kanji]:
                    dot.edge(data.descriptions[kanji], data.descriptions[similar], color="lightgrey", constraint="false")#.decode('utf-8')
                similaredges[kanji].add(similar)
                similaredges[similar].add(kanji)

        for i in range(0,len(all_kw)):
            for j in range(i+1,len(all_kw)):
                for l in all_kw[i]:
                    if l in all_kw[j]:
                        dot.edge(Keywords.labelof(keywords, all_kw[i], data), Keywords.labelof(keywords, all_kw[j], data), len="0.5", color="yellow", penwidth="2")#.decode('utf-8')

        for kw in keywords:
            if not kw or len(kw) < 1:
                continue

            if len(kw) > 1 and kw[0] in data.descriptions and kw[1] in data.descriptions:
                dot.edge(data.descriptions[kw[0]], data.descriptions[kw[1]], color="green", len="0.5")#.decode('utf-8')

            label = ("<b>" + kw + "</b>\n " + str(keywords[kw]))#.decode('utf-8')

            ease = 0
            d = 0
            for kanji in kw:
                if kanji in data.ease:
                    ease += data.ease[kanji]
                    d += 1
            if d>0:
                ease /= d

            fe = str((0.05 + 0.95 * ease * ease))
            fcolor = "0.4 " + fe + " 1"
            fsize = '50'
            if(len(kw) < 2):
                fsize = '25'
            node = dot.node(Keywords.labelof(keywords, kw, data), fontsize=fsize, label=kw, shape="rectangle", style='filled', fillcolor=fcolor)

        return dot
