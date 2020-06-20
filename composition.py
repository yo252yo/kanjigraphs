# -*- coding: utf-8 -*-
from graphviz import Digraph

class Composition(object):

    def graph(kanjis, colors, descriptions, components, anticomponents, radicals):
        dot = Digraph(comment='Kanjis')
        dot.engine = 'neato'
        dot.format = 'svg'
        dot.attr(rankdir='TB', nodesep='5.0', ranksep='5.0', overlap="false")
        dot.attr('node', fontsize='30')

        for kanji in kanjis:
            if kanji in radicals:
                continue
            #try:
            k = kanji#.decode('utf-8')
            label = ("" + kanji + "\n " + descriptions[kanji])#.decode('utf-8')
            color = colors[kanji]

            if (len(components[kanji]) == 0 and  colors[kanji] != '0.6 0.8 1.0'):
                color = "lightgrey"
            if not (len(anticomponents[kanji]) == 0):
                shape = "circle"
            else:
                shape = "doublecircle"

            dot.node(descriptions[kanji], label=kanji, fillcolor=color, style='filled', shape=shape)

            for component in components[kanji]:
                if component not in radicals:
                    source = component
                    if component in descriptions:
                        source = descriptions[component]
                    dot.edge(source, descriptions[kanji], constraint='true')#.decode('utf-8')
            #except Exception:
            #    print("encoding fial")
        return dot
