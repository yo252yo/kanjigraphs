# -*- coding: utf-8 -*-
from graphviz import Digraph

class ORoots(object):
    def printComponents(dot, kanji, description, fontsize, components, descriptions, colors):
        if kanji == "" or kanji == " ":
            return
        for component in components[kanji]:
            source = component
            if component in descriptions:
                source = descriptions[component]
            kanjicomponode = component + "[" + source + "] -> " + description
            if component in colors:
                color = colors[component]
            else:
                color = 'lightgrey'
            dot.node(kanjicomponode, label=component, fillcolor=color, fontsize=str(int(fontsize)), style='filled')
            dot.edge(kanjicomponode, description, constraint='true')#.decode('utf-8')

            if component in components:
                ORoots.printComponents(dot, component, kanjicomponode, fontsize*.7, components, descriptions, colors)

    def graph(kanjis, colors, descriptions, components):
        dot = Digraph(comment='Roots')
        dot.engine = 'dot'
        dot.format = 'svg'
        dot.attr(rankdir='BT', nodesep='1.0', ranksep='0.1', overlap="false")
        dot.attr('node', fontsize='40')

        for kanji in kanjis:
            if float(colors[kanji].split(" ")[1]) < 0.8:
                continue

            #try:
            k = kanji#.decode('utf-8')
            label = ("" + kanji + "\n " + descriptions[kanji])#.decode('utf-8')
            color = colors[kanji]
            dot.node(descriptions[kanji], label=kanji, fontsize="40", fillcolor=color, style='filled')

            ORoots.printComponents(dot, kanji, descriptions[kanji], 25, components, descriptions, colors)


            #except Exception:
            #    print("encoding fial")


        return dot
