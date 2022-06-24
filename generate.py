# -*- coding: utf-8 -*-
import random
import time
from components import Components
from composition import Composition
from getdata import GetData
from oroots import ORoots
from similarity import Similarity
from keywords import Keywords


# CSV format: kanji/pronounciations/meaning/components/similar kanjis/../../../ease level/
kanjis_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQtNCsV4crkpKfJGHa1dQniBbtNs1VrmE3MlhUDo2lT2DghEbO3fJKg5bR2FC_wn83hI0tgl2e1i172/pub?gid=1079852200&output=csv'
kanjisim_url1 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQtNCsV4crkpKfJGHa1dQniBbtNs1VrmE3MlhUDo2lT2DghEbO3fJKg5bR2FC_wn83hI0tgl2e1i172/pub?gid=6359283&output=csv'
kanjisim_url2 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQtNCsV4crkpKfJGHa1dQniBbtNs1VrmE3MlhUDo2lT2DghEbO3fJKg5bR2FC_wn83hI0tgl2e1i172/pub?gid=730163754&output=csv'
# https://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=16H15Te4hGrKUx1VEpvexZ94rrFWek1k3J7UL9qVVTG4&exportFormat=csv&gid=1079852200
kanjis_file_name = ('D:/Japanese/jap_anki/dumps/graph_kanjis_details.txt')
kanjissim_file_name = ('D:/Japanese/jap_anki/dumps/graph_kanjis_sim.txt')


print("Fetching data")
data = GetData()

fetchedK = False
while not fetchedK:
    try:
        fetchedK = data.get(kanjis_url, kanjis_file_name)
    except Exception as e:
        print("- retry: " + str(e))
        time.sleep(60)

fetchedKS = False
while not fetchedKS:
    try:
        fetchedKS = data.bufferKanjiSimData(kanjisim_url1, kanjisim_url2, kanjissim_file_name)
    except Exception as e:
        print("- retry: " + str(e))
        time.sleep(60)


kdot = Keywords.graph(data)
kdisplay = random.random() < 0.6 # fix after the development of this graph
kdot.render('D:\Japanese\jap_anki\graphs\keywords', view=kdisplay)

sdot = Similarity.graph(data)
sdisplay = random.random() < 0.6
sdot.render('D:\Japanese\jap_anki\graphs\similarity', view=sdisplay)

cdot = Composition.graph(data)
cdisplay = random.random() < 0.5
cdot.render('D:\Japanese\jap_anki\graphs\composition', view=cdisplay)

odot = ORoots.graph(data)
odisplay = random.random() < 0.4
odot.render('D:\Japanese\jap_anki\graphs\oroots', view=odisplay)

rdot = Components.graph(data)
rdisplay = (not (sdisplay or cdisplay or odisplay or kdisplay)) or (random.random() < 0.3)
rdot.render('D:\Japanese\jap_anki\graphs\components', view=rdisplay)

print("All done")
