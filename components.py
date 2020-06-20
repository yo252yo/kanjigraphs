# -*- coding: utf-8 -*-
import math
from graphviz import Digraph

class Components(object):

    def fontsize(kanji, anticomponents):
        size = 20 + math.sqrt(len(anticomponents[kanji]))*10
        return str(size)

    def graph(kanjis, colors, descriptions, components, anticomponents, radicals):
        dot = Digraph(comment='Kanjis')
        dot.engine = 'neato'
        dot.format = 'svg'
        dot.attr(rankdir='TB', nodesep='5.0', ranksep='5.0', overlap="false")
        dot.attr('node', fontsize='30')

        for radical in radicals:
            if radical in kanjis:
                continue

            try:
                dot.node(radical, radical, fillcolor="grey", style="filled")
            except Exception:
                print("encoding fial")

        for kanji in kanjis:
            #try:
                k = kanji#.decode('utf-8')
                label = ("" + kanji + "\n " + descriptions[kanji])#.decode('utf-8')
                color = colors[kanji]

                if (len(components[kanji]) == 0 and  colors[kanji] != '0.6 0.8 1.0'):
                    color = "lightgrey"

                if not (len(anticomponents[kanji]) == 0):
                    dot.node(descriptions[kanji], label=kanji, fontsize=Components.fontsize(kanji, anticomponents), fillcolor=color, style='filled')
                    shape = "circle"
                else:
                    shape = "doublecircle"

                for component in components[kanji]:
                    kanjicomponode = descriptions[kanji] + " <- " + component
                    dot.node(kanjicomponode, label=kanji, fillcolor=color, fontsize=Components.fontsize(kanji, anticomponents), style='filled', shape=shape)
                    #if component in radicals or len(components[component]) == 0:
                    source = component
                    if component in descriptions:
                        source = descriptions[component]
                    dot.edge(source, kanjicomponode, constraint='true')#.decode('utf-8')
            #except Exception:
            #    print("encoding fial")

        return dot
