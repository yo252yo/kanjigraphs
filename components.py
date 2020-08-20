# -*- coding: utf-8 -*-
import math
from graphviz import Digraph
import random

class Components(object):

    def get(array, value, default):
        if value in array:
            return array[value]
        else:
            return default

    def fontsize(kanji, data):
        size = 20 + math.sqrt(len(data.anticomponents[kanji]))*10
        return str(size)

    def color(kanji, data):
        c = Components.get(data.colors, kanji, "grey")
        if kanji in data.components and kanji in data.colors and (len(data.components[kanji]) == 0 and data.colors[kanji] != '0.6 0.8 1.0'):
            c = "lightgrey"
        return c

    def shape(kanji, data):
        shape = "doublecircle"
        if kanji in data.anticomponents and not (len(data.anticomponents[kanji]) == 0):
            shape = "circle"
        return shape

    def graph(data):
        dot = Digraph(comment='Kanjis')
        dot.engine = 'neato'
        dot.format = 'svg'
        dot.attr(rankdir='TB', nodesep='5.0', ranksep='5.0', overlap="false")
        dot.attr('node', fontsize='30')

        kanjispresent = set()
        for radical in data.radicals:
            if radical in data.spotlight or random.random() < 0.02:
                kanjispresent.add(radical)

        for kanji in data.kanjis:
            if kanji in data.spotlight or random.random() < 0.02:
                kanjispresent.add(kanji)

        for kanji in data.spotlight:
            for component in data.components[kanji]:
                kanjispresent.add(component)

        for kanji in kanjispresent:
            #try:
                k = kanji#.decode('utf-8')
                description = Components.get(data.descriptions, kanji, kanji)

                if not (len(data.anticomponents[kanji]) == 0):
                    dot.node(description, label=kanji, fontsize=Components.fontsize(kanji, data), fillcolor=Components.color(kanji, data), style='filled', shape=Components.shape(kanji, data))

                    for component in data.anticomponents[kanji]:
                        kanjicomponode = kanji + " -> " + Components.get(data.descriptions, component, component)
                        dot.node(kanjicomponode, label=component, fillcolor=Components.color(component, data), fontsize=Components.fontsize(component, data), style='filled', shape=Components.shape(component, data))
                        #if component in radicals or len(components[component]) == 0:
                        source = Components.get(data.descriptions, component, component)
                        dot.edge(description, kanjicomponode, constraint='true')#.decode('utf-8')
            #except Exception:
            #    print("encoding fial")

        return dot
