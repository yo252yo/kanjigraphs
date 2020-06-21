# -*- coding: utf-8 -*-
from graphviz import Digraph

class Composition(object):

    def graph(data):
        dot = Digraph(comment='Kanjis')
        dot.engine = 'neato'
        dot.format = 'svg'
        dot.attr(rankdir='TB', nodesep='5.0', ranksep='5.0', overlap="false")
        dot.attr('node', fontsize='30')

        for kanji in data.kanjis:
            if kanji in data.radicals:
                continue
            #try:
            k = kanji#.decode('utf-8')
            label = ("" + kanji + "\n " + data.descriptions[kanji])#.decode('utf-8')
            color = data.colors[kanji]

            if (len(data.components[kanji]) == 0 and  data.colors[kanji] != '0.6 0.8 1.0'):
                color = "lightgrey"
            if not (len(data.anticomponents[kanji]) == 0):
                shape = "circle"
            else:
                shape = "doublecircle"

            dot.node(data.descriptions[kanji], label=kanji, fillcolor=color, style='filled', shape=shape)

            for component in data.components[kanji]:
                if component not in data.radicals:
                    source = component
                    if component in data.descriptions:
                        source = data.descriptions[component]
                    dot.edge(source, data.descriptions[kanji], constraint='true')#.decode('utf-8')
            #except Exception:
            #    print("encoding fial")
        return dot
