# -*- coding: utf-8 -*-
from graphviz import Graph
from collections import defaultdict
import random
import math


class Similarity(object):
    dangerzones = ['騒', '傷', '畳' , '滴', '措', '憎', '培', '鈍', '境', '料', '投', '義', '院', '完', '集', '攻', '職', '節', '真', '墓', '慣']
    def graph(data):
        print("Printing similarity")
        dot = Graph(comment='Kanjis', strict=True)
        dot.engine = 'neato'
        dot.format = 'svg'
        dot.attr(overlap="porthox", sep="-0.2", outputorder="edgesfirst")
        dot.attr('node', fontsize='30')
        similaredges = defaultdict(set)
        for kanji in data.kanjis:
            #try:
                k = kanji#.decode('utf-8')
                label = ("<b>" + kanji + "</b>\n " + data.descriptions[kanji])#.decode('utf-8')

                shape = "circle"
                fcolor = "0 0 " + str(1-(0.2 + 0.8 * data.ease[kanji]))
                color = fcolor
                penwidth = "1"

                if (kanji in Similarity.dangerzones):
                    shape = "doublecircle"
                    color = "red"
                    penwidth = "3"
                elif (data.rattrapage[kanji] <= 9):
                    penwidth = str(2 + 10 - data.rattrapage[kanji])
                    color = "black"

                node = dot.node(data.descriptions[kanji], label=kanji, penwidth=penwidth, shape=shape, color=color, fontcolor=fcolor, fillcolor=data.colors[kanji], style='filled')

        #        constraint='true'
        #        color = "black"
        #        for similar in data.similars[kanji]:
        #            color = "black"
        #            if (similar in dangerzones or kanji in dangerzones):
        #                color = "red"
        #            if not similaredges[kanji] or not similar in similaredges[kanji]:
        #                if random.random() < 0.2 and color != "red": # Random dropoff
        #                    color= "lightgrey"
        #                    constraint='false'
        #                dot.edge(data.descriptions[kanji], data.descriptions[similar], color=color, constraint=constraint)#.decode('utf-8')
        #            similaredges[kanji].add(similar)
        #            similaredges[similar].add(kanji)


                for similar in data.similars[kanji]:
                    color = "#F1F1F1"
                    weight = "1"
                    if (similar in Similarity.dangerzones or kanji in Similarity.dangerzones):
                        color = "red"
                        style = ""
                        weight = "4"
                    if not similaredges[kanji] or not similar in similaredges[kanji]:
                        dot.edge(data.descriptions[kanji], data.descriptions[similar], color=color, constraint="true", weight=weight)#.decode('utf-8')
                    similaredges[kanji].add(similar)
                    similaredges[similar].add(kanji)

                for similar in data.semilars[kanji]:
                    color = "lightgrey"
                    if (similar in Similarity.dangerzones or kanji in Similarity.dangerzones):
                        color = "red"
                    if not similaredges[kanji] or not similar in similaredges[kanji]:
                        if random.random() >= 0: # random dropoff
                            dot.edge(data.descriptions[kanji], data.descriptions[similar], color=color, constraint="false")#.decode('utf-8')
                    similaredges[kanji].add(similar)
                    similaredges[similar].add(kanji)


            #except Exception:
            #    print("encoding fial")

        return dot
