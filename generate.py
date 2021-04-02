# -*- coding: utf-8 -*-
import random
import time
from components import Components
from composition import Composition
from getdata import GetData
from oroots import ORoots
from similarity import Similarity


# CSV format: kanji/pronounciations/meaning/components/similar kanjis/../../../ease level/
kanjis_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQtNCsV4crkpKfJGHa1dQniBbtNs1VrmE3MlhUDo2lT2DghEbO3fJKg5bR2FC_wn83hI0tgl2e1i172/pub?gid=1079852200&output=csv'
# https://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=16H15Te4hGrKUx1VEpvexZ94rrFWek1k3J7UL9qVVTG4&exportFormat=csv&gid=1079852200
kanjis_file_name = ('D:/Japanese/jap_anki/dumps/graph_kanjis_details.txt')


print("Fetching data")
fetched = False
while not fetched:
    try:
        data = GetData()
        data.get(kanjis_url, kanjis_file_name)
        fetched = True
    except Exception as e:
        print("- retry")
        print(e)
        time.sleep(60)


print("Printing similarity")
sdot = Similarity.graph(data)
sdisplay = random.random() < 0.7
sdot.render('D:\Japanese\jap_anki\graphs\similarity', view=sdisplay)

print("Printing composition")
cdot = Composition.graph(data)
cdisplay = random.random() < 0.7
cdot.render('D:\Japanese\jap_anki\graphs\composition', view=cdisplay)

print("Printing ORoots")
odot = ORoots.graph(data)
odisplay = random.random() < 0.5
odot.render('D:\Japanese\jap_anki\graphs\oroots', view=odisplay)

print("Printing components")
rdot = Components.graph(data)
rdisplay = (not (sdisplay or cdisplay or odisplay)) or (random.random() < 0.4)
rdot.render('D:\Japanese\jap_anki\graphs\components', view=(random.random() < 0.4))

print("All done")
