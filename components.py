# -*- coding: utf-8 -*-
import math
from graphviz import Digraph

class Components(object):

    def fontsize(kanji, data):
        size = 20 + math.sqrt(len(data.anticomponents[kanji]))*10
        return str(size)

    def graph(data):
        dot = Digraph(comment='Kanjis')
        dot.engine = 'neato'
        dot.format = 'svg'
        dot.attr(rankdir='TB', nodesep='5.0', ranksep='5.0', overlap="false")
        dot.attr('node', fontsize='30')

        for radical in data.radicals:
            if radical in data.kanjis:
                continue

            try:
                dot.node(radical, radical, fillcolor="grey", style="filled")
            except Exception:
                print("encoding fial")

        for kanji in data.kanjis:
            #try:
                k = kanji#.decode('utf-8')
                label = ("" + kanji + "\n " + data.descriptions[kanji])#.decode('utf-8')
                color = data.colors[kanji]

                if (len(data.components[kanji]) == 0 and  data.colors[kanji] != '0.6 0.8 1.0'):
                    color = "lightgrey"

                if not (len(data.anticomponents[kanji]) == 0):
                    dot.node(data.descriptions[kanji], label=kanji, fontsize=Components.fontsize(kanji, data), fillcolor=color, style='filled')
                    shape = "circle"
                else:
                    shape = "doublecircle"

                for component in data.components[kanji]:
                    kanjicomponode = data.descriptions[kanji] + " <- " + component
                    dot.node(kanjicomponode, label=kanji, fillcolor=color, fontsize=Components.fontsize(kanji, data), style='filled', shape=shape)
                    #if component in radicals or len(components[component]) == 0:
                    source = component
                    if component in data.descriptions:
                        source = data.descriptions[component]
                    dot.edge(source, kanjicomponode, constraint='true')#.decode('utf-8')
            #except Exception:
            #    print("encoding fial")

        return dot
