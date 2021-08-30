# -*- coding: utf-8 -*-
from graphviz import Digraph

class ORoots(object):
    def printComponents(dot, kanji, description, fontsize, data):
        if kanji == "" or kanji == " ":
            return
        for component in data.components[kanji]:
            source = component
            if component in data.descriptions:
                source = data.descriptions[component]
            kanjicomponode = component + "[" + source + "] -> " + description
            if component in data.colors:
                color = data.colors[component]
            else:
                color = 'lightgrey'
            dot.node(kanjicomponode, label=component, fillcolor=color, fontsize=str(int(fontsize)), style='filled')
            dot.edge(kanjicomponode, description, constraint='true')#.decode('utf-8')

            if component in data.components:
                ORoots.printComponents(dot, component, kanjicomponode, fontsize*.7, data)

    def graph(data):
        print("Printing ORoots")
        dot = Digraph(comment='Roots')
        dot.engine = 'dot'
        dot.format = 'svg'
        dot.attr(rankdir='BT', nodesep='1.0', ranksep='0.1', overlap="false")
        dot.attr('node', fontsize='40')

        for kanji in data.kanjis:
            if float(data.colors[kanji].split(" ")[1]) < 0.9:
                continue

            #try:
            k = kanji#.decode('utf-8')
            label = ("" + kanji + "\n " + data.descriptions[kanji])#.decode('utf-8')
            color = data.colors[kanji]
            dot.node(data.descriptions[kanji], label=kanji, fontsize="40", fillcolor=color, style='filled')

            ORoots.printComponents(dot, kanji, data.descriptions[kanji], 25, data)


            #except Exception:
            #    print("encoding fial")


        return dot
