# -*- coding: utf-8 -*-
from graphviz import Graph
from collections import defaultdict
import random
import math


class Keywords(object):
    def labelof(keywords, kw):
        return ("<b>" + kw + "</b>\n " + str(keywords[kw]))

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

        for kanji in data.kanjis:
            if kanji in data.keywords:
                kanjis.add(kanji)
                for kw in data.keywords[kanji]:
                    l = kw.split(" ")
                    if not l[0] in keywords:
                        keywords[l[0]] = kw

        newkanjis = set()
        for kanji in kanjis:
            for similar in data.similars[kanji]:
                newkanjis.add(similar)

        kanjis = kanjis.union(newkanjis)
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

            node = dot.node(data.descriptions[kanji], label=kanji, shape=shape, color=color, fontcolor=fcolor, fillcolor=bgcolor, style='filled')

            if kanji in data.keywords:
                for kw in data.keywords[kanji]:
                    l = kw.split(" ")
                    if not l[0]:
                        continue
                    if not l[0] in keywords:
                        keywords[l[0]] = kw
                    dot.edge(data.descriptions[kanji], Keywords.labelof(keywords, l[0]), len="0.5", color="green", penwidth="3")#.decode('utf-8')

            for similar in (data.similars[kanji] + data.semilars[kanji]):
                if not similar in kanjis:
                    continue
                if not similaredges[kanji] or not similar in similaredges[kanji]:
                    dot.edge(data.descriptions[kanji], data.descriptions[similar], color="lightgrey", constraint="false")#.decode('utf-8')
                similaredges[kanji].add(similar)
                similaredges[similar].add(kanji)

        for kw in keywords:
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
            node = dot.node(Keywords.labelof(keywords, kw), fontsize='50', label=kw, shape="rectangle", style='filled', fillcolor=fcolor)

        return dot
