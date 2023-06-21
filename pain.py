# -*- coding: utf-8 -*-
from graphviz import Digraph

class Pain(object):

    def graph(data):
        print("Printing Troubling")
        dot = Digraph(comment='Troubling')
        dot.engine = 'neato'
        dot.format = 'svg'
        dot.attr(overlap="porthoy", sep="-0.2", outputorder="edgesfirst")
        dot.attr('node', fontsize='30')

        kanjis = set()
        for kanji in data.kanjis:
            if (data.rattrapage[kanji] < 8 or float(data.colors[kanji].split(" ")[1]) >= 0.95):
                kanjis.add(kanji)

        expand = set()
        edges = set()
        for kanji in kanjis:
                for similar in data.similars[kanji]:
                    if not similar in kanjis:
                        expand.add(similar)
                    if kanji + similar in edges or similar + kanji in edges:
                        continue

                    weight = "1"
                    if similar in kanjis:
                        weight = "5"
                    edges.add(kanji + similar)
                    dot.edge(data.descriptions[kanji], data.descriptions[similar], color="black", dir="none", penwidth=weight)#.decode('utf-8')


                for similar in data.semilars[kanji]:
                    if not similar in kanjis:
                        expand.add(similar)
                    if kanji + similar in edges or similar + kanji in edges:
                        continue

                    weight = "1"
                    if similar in kanjis:
                        weight = "5"
                    edges.add(kanji + similar)
                    dot.edge(data.descriptions[kanji], data.descriptions[similar], color="lightgrey", constraint="false", dir="none", penwidth=weight)#.decode('utf-8


        for kanji in expand:
            if kanji in kanjis:
                print("WTF")
                continue
            #try:
            k = kanji#.decode('utf-8')
            label = ("" + kanji + "\n " + data.descriptions[kanji])#.decode('utf-8')
            color = data.colors[kanji]
            dot.node(data.descriptions[kanji], color="lightgrey", fontcolor="lightgrey",fillcolor="white", label=kanji, fontsize="25", style='filled')

        for kanji in kanjis:
                k = kanji#.decode('utf-8')
                label = ("" + kanji + "\n " + data.descriptions[kanji])#.decode('utf-8')
                color = data.colors[kanji]
                dot.node(data.descriptions[kanji], label=kanji, fontsize="40", fillcolor=color, style='filled')


        return dot
