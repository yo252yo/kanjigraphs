# -*- coding: utf-8 -*-
from graphviz import Graph
from collections import defaultdict
import random

class Similarity(object):
    dangerzones = ['傷', '料', '投', '音', '理', '物', '話', '徒', '院', '完', '寝', '集', '攻']

    def graph(kanjis, colors, descriptions, components, anticomponents, radicals, similars, semilars):
        dot = Graph(comment='Kanjis', strict=True)
        dot.engine = 'neato'
        dot.format = 'svg'
        dot.attr(rankdir='TB', overlap="false")
        dot.attr('node', fontsize='30')

        similaredges = defaultdict(set)
        for kanji in kanjis:
            #try:
                k = kanji#.decode('utf-8')
                label = ("<b>" + kanji + "</b>\n " + descriptions[kanji])#.decode('utf-8')

                shape = "circle"
                color = "black"
                if (kanji in Similarity.dangerzones):
                    shape = "doublecircle"
                    color = "red"

                node = dot.node(descriptions[kanji], label=kanji, shape=shape, color=color, fillcolor=colors[kanji], style='filled')

        #        constraint='true'
        #        color = "black"
        #        for similar in similars[kanji]:
        #            color = "black"
        #            if (similar in dangerzones or kanji in dangerzones):
        #                color = "red"
        #            if not similaredges[kanji] or not similar in similaredges[kanji]:
        #                if random.random() < 0.2 and color != "red": # Random dropoff
        #                    color= "lightgrey"
        #                    constraint='false'
        #                dot.edge(descriptions[kanji], descriptions[similar], color=color, constraint=constraint)#.decode('utf-8')
        #            similaredges[kanji].add(similar)
        #            similaredges[similar].add(kanji)


                for similar in similars[kanji]:
                    color = "black"
                    if (similar in Similarity.dangerzones or kanji in Similarity.dangerzones):
                        color = "red"
                    if not similaredges[kanji] or not similar in similaredges[kanji]:
                        dot.edge(descriptions[kanji], descriptions[similar], color=color, constraint="true")#.decode('utf-8')
                    similaredges[kanji].add(similar)
                    similaredges[similar].add(kanji)

                for similar in semilars[kanji]:
                    color = "lightgrey"
                    if (similar in Similarity.dangerzones or kanji in Similarity.dangerzones):
                        color = "red"
                    if not similaredges[kanji] or not similar in similaredges[kanji]:
                        if random.random() >= 0: # random dropoff
                            dot.edge(descriptions[kanji], descriptions[similar], color=color, constraint="false")#.decode('utf-8')
                    similaredges[kanji].add(similar)
                    similaredges[similar].add(kanji)


            #except Exception:
            #    print("encoding fial")

        return dot
