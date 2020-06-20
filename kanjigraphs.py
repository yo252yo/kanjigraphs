# -*- coding: utf-8 -*-
import csv
import math
import random
import codecs
from urllib.request import urlopen
from collections import defaultdict
from graphviz import Digraph
from graphviz import Graph


# ============== LOAD AND BACKUP DATA

kanjis_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQtNCsV4crkpKfJGHa1dQniBbtNs1VrmE3MlhUDo2lT2DghEbO3fJKg5bR2FC_wn83hI0tgl2e1i172/pub?gid=1079852200&output=csv'
kanjisim_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQtNCsV4crkpKfJGHa1dQniBbtNs1VrmE3MlhUDo2lT2DghEbO3fJKg5bR2FC_wn83hI0tgl2e1i172/pub?gid=6359283&single=true&output=csv'

response_kanjis = urlopen(kanjis_url)
response_kanjisim = urlopen(kanjisim_url)

lines_kanjis = response_kanjis.read().decode('utf-8').splitlines()
lines_kanjisim = response_kanjisim.read().decode('utf-8').splitlines()

kanjis_file = codecs.open('D:/Japanese/jap_anki/dumps/graph_kanjis_details.txt', 'w', 'utf-8')
kanjisim_file = codecs.open('D:/Japanese/jap_anki/dumps/graph_kanjis_sim.txt', 'w', 'utf-8')


for line in lines_kanjis:
    kanjis_file.write(line + "\r\n")
for line in lines_kanjisim:
    kanjisim_file.write(line + "\r\n")

kanjis_file.close()
kanjisim_file.close()


# ============== IMPORT DATA


cr = csv.reader(lines_kanjis)

kanjilist = []
for row in cr:
    kanjilist.append(row)

kanjis = set()
colors = {}
descriptions = {}
for i, k in enumerate(kanjilist):
    if i == 0 or k[0] == '':
        continue

    kanjis.add(k[0])
    percent =  (i + 1) / len(kanjilist)
    index = pow(percent, 9) # 1 is new, 0 is old.

    if k[8] == "" or k[8] == "#N/A":
        ease = 0
    else:
        ease = int(k[8]) # number of days until resched
    #!!!!!!!!!!!!!!!!!!!! for now, everything will be around 0, so we'll artificially enforce
    # ease += 2
    # antiease = 2 / math.pow(math.log(ease+3),1.8) # 10d -> .4, 30d -> .2, 60d -> .1
    antiease = max(1-.05*ease, 0)  # 5d -> .75, 10d -> .5, 20d -> 0

    # redness = (4*max(index, antiease) + min(index, antiease))/5
    redness = max(index, antiease)
    #!!!!!!!!!!!!!!!!!!!! for now, everything will be around 0, so we'll artificially enforce
    #redness = math.pow(redness, 2)

    colors[k[0]] = '0.6 ' + str(redness) + ' 1.0'

    if i >= len(kanjilist)-4: # 4 most recent get spotlight
        colors[k[0]] = '0.8 1.0 1.0'

    if random.random() < 0.02: # Random spotlight
        colors[k[0]] = '0.0 0.9 1.0'
    descriptions[k[0]] = k[1] + " (" + k[2] + ")"

#kanjis.remove('')

radicals = ['己', '目', '中', '工', '木', '巳', '王', '田', '丁', '日', '人', '一', '二', '十', '亖', '阝', 'ꓘ', '八', '口', '兀', '丌', '夂', '廿', '尹', '灬', 'モ', '卌', 'ン', 'ヨ', 'ム', 'ヤ', 'セ', '匕', 'ネ', 'コ', 'ラ', 'シ', '厂', 'ク', 'ケ', 'ソ', '⻌', 'イ', '宀', 'ト', '个', 'ナ', '彳', '扌', '弋', '犭', '爿', '戈', '斗', '凵', '艾', '卩', '尺', '亅', '廾', '匕', '冂', '几', '尸', '冫', '匚', '广', '勹', '杰', '丙', '之']

components = defaultdict(list)
anticomponents = defaultdict(list)
similars = defaultdict(list)
semilars = defaultdict(list)

for k in kanjilist:
    for kk in k[3]:#.split(" "):
        if kk in kanjis or kk in radicals:
            components[k[0]].append(kk)
            anticomponents[kk].append(k[0])
    splitkanjisim = k[4].split("###")
    for kk in splitkanjisim[0]:
        if kk in kanjis:
            similars[k[0]].append(kk)
    if len(splitkanjisim) > 1:
        for kk in splitkanjisim[1]:
            if kk in kanjis:
                semilars[k[0]].append(kk)



# ============== GRAPH 3
dangerzones = ['傷', '料', '投', '音', '理', '物', '話', '徒', '院', '完', '寝', '集', '攻']



sdot = Graph(comment='Kanjis', strict=True)
sdot.engine = 'neato'
sdot.format = 'svg'
sdot.attr(rankdir='TB', overlap="false")
sdot.attr('node', fontsize='30')

similaredges = defaultdict(set)
for kanji in kanjis:
    try:
        k = kanji#.decode('utf-8')
        label = ("<b>" + kanji + "</b>\n " + descriptions[kanji])#.decode('utf-8')

        shape = "circle"
        color = "black"
        if (kanji in dangerzones):
            shape = "doublecircle"
            color = "red"

        node = sdot.node(descriptions[kanji], label=kanji, shape=shape, color=color, fillcolor=colors[kanji], style='filled')

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
#                sdot.edge(descriptions[kanji], descriptions[similar], color=color, constraint=constraint)#.decode('utf-8')
#            similaredges[kanji].add(similar)
#            similaredges[similar].add(kanji)


        for similar in similars[kanji]:
            color = "black"
            if (similar in dangerzones or kanji in dangerzones):
                color = "red"
            if not similaredges[kanji] or not similar in similaredges[kanji]:
                sdot.edge(descriptions[kanji], descriptions[similar], color=color, constraint="true")#.decode('utf-8')
            similaredges[kanji].add(similar)
            similaredges[similar].add(kanji)

        for similar in semilars[kanji]:
            color = "lightgrey"
            if (similar in dangerzones or kanji in dangerzones):
                color = "red"
            if not similaredges[kanji] or not similar in similaredges[kanji]:
                if random.random() >= 0: # random dropoff
                    sdot.edge(descriptions[kanji], descriptions[similar], color=color, constraint="false")#.decode('utf-8')
            similaredges[kanji].add(similar)
            similaredges[similar].add(kanji)


    except Exception:
        print("encoding fial")

viewgraph = random.random() < 0.8
sdot.render('D:\Japanese\jap_anki\graphs\graphs\similarity', view=viewgraph)







# ============== GRAPH 2





cdot = Digraph(comment='Kanjis')
cdot.engine = 'neato'
cdot.format = 'svg'
cdot.attr(rankdir='TB', nodesep='5.0', ranksep='5.0', overlap="false")
cdot.attr('node', fontsize='30')

for kanji in kanjis:
    if kanji in radicals:
        continue
    try:
        k = kanji#.decode('utf-8')
        label = ("" + kanji + "\n " + descriptions[kanji])#.decode('utf-8')
        color = colors[kanji]

        if (len(components[kanji]) == 0 and  colors[kanji] != '0.6 0.8 1.0'):
            color = "lightgrey"
        if not (len(anticomponents[kanji]) == 0):
            shape = "circle"
        else:
            shape = "doublecircle"

        cdot.node(descriptions[kanji], label=kanji, fillcolor=color, style='filled', shape=shape)

        for component in components[kanji]:
            if component not in radicals:
                source = component
                if component in descriptions:
                    source = descriptions[component]
                cdot.edge(source, descriptions[kanji], constraint='true')#.decode('utf-8')
    except Exception:
        print("encoding fial")

viewgraph = random.random() < 0.6
cdot.render('D:\Japanese\jap_anki\graphs\graphs\composition', view=viewgraph)






# ============== GRAPH 1





def fontsize(kanji):
    size = 20 + math.sqrt(len(anticomponents[kanji]))*10
    return str(size)





rdot = Digraph(comment='Kanjis')
rdot.engine = 'neato'
rdot.format = 'svg'
rdot.attr(rankdir='TB', nodesep='5.0', ranksep='5.0', overlap="false")
rdot.attr('node', fontsize='30')

for radical in radicals:
    if radical in kanjis:
        continue

    try:
        rdot.node(radical, radical, fillcolor="grey", style="filled")
    except Exception:
        print("encoding fial")

for kanji in kanjis:
    try:
        k = kanji#.decode('utf-8')
        label = ("" + kanji + "\n " + descriptions[kanji])#.decode('utf-8')
        color = colors[kanji]

        if (len(components[kanji]) == 0 and  colors[kanji] != '0.6 0.8 1.0'):
            color = "lightgrey"

        if not (len(anticomponents[kanji]) == 0):
            rdot.node(descriptions[kanji], label=kanji, fontsize=fontsize(kanji), fillcolor=color, style='filled')
            shape = "circle"
        else:
            shape = "doublecircle"

        for component in components[kanji]:
            kanjicomponode = descriptions[kanji] + " <- " + component
            rdot.node(kanjicomponode, label=kanji, fillcolor=color, fontsize=fontsize(kanji), style='filled', shape=shape)
            #if component in radicals or len(components[component]) == 0:
            source = component
            if component in descriptions:
                source = descriptions[component]
            rdot.edge(source, kanjicomponode, constraint='true')#.decode('utf-8')
    except Exception:
        print("encoding fial")


viewgraph = random.random() < 0.4
rdot.render('D:\Japanese\jap_anki\graphs\graphs\components', view=viewgraph)




# ============== GRAPH 0



def printComponents(odot, kanji, description, fontsize):
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
        odot.node(kanjicomponode, label=component, fillcolor=color, fontsize=str(int(fontsize)), style='filled')
        odot.edge(kanjicomponode, description, constraint='true')#.decode('utf-8')

        if component in components:
            printComponents(odot, component, kanjicomponode, fontsize*.7)


odot = Digraph(comment='Roots')
odot.engine = 'dot'
odot.format = 'svg'
odot.attr(rankdir='BT', nodesep='1.0', ranksep='0.1', overlap="false")
odot.attr('node', fontsize='40')

for kanji in kanjis:
    if float(colors[kanji].split(" ")[1]) < 0.8:
        continue

    #try:
    k = kanji#.decode('utf-8')
    label = ("" + kanji + "\n " + descriptions[kanji])#.decode('utf-8')
    color = colors[kanji]
    odot.node(descriptions[kanji], label=kanji, fontsize="40", fillcolor=color, style='filled')

    printComponents(odot, kanji, descriptions[kanji], 25)


    #except Exception:
    #    print("encoding fial")


viewgraph =  random.random() < 0.4
odot.render('D:\Japanese\jap_anki\graphs\graphs\oroots', view=viewgraph)
