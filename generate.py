# -*- coding: utf-8 -*-
import random
from components import Components
from composition import Composition
from getdata import GetData
from oroots import ORoots
from similarity import Similarity


kanjis_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQtNCsV4crkpKfJGHa1dQniBbtNs1VrmE3MlhUDo2lT2DghEbO3fJKg5bR2FC_wn83hI0tgl2e1i172/pub?gid=1079852200&output=csv'
kanjisim_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQtNCsV4crkpKfJGHa1dQniBbtNs1VrmE3MlhUDo2lT2DghEbO3fJKg5bR2FC_wn83hI0tgl2e1i172/pub?gid=6359283&single=true&output=csv'

kanjis_file_name = ('D:/Japanese/jap_anki/dumps/graph_kanjis_details.txt')
kanjisim_file_name = ('D:/Japanese/jap_anki/dumps/graph_kanjis_sim.txt')



print("Fetching data")
(kanjis, colors, descriptions, components, anticomponents, radicals, similars, semilars) = GetData.get(kanjis_url, kanjisim_url, kanjis_file_name, kanjisim_file_name)

print("Printing similarity")
sdot = Similarity.graph(kanjis, colors, descriptions, components, anticomponents, radicals, similars, semilars)
sdot.render('D:\Japanese\jap_anki\graphs\similarity', view=(random.random() < 0.8))

print("Printing composition")
cdot = Composition.graph(kanjis, colors, descriptions, components, anticomponents, radicals)
cdot.render('D:\Japanese\jap_anki\graphs\composition', view=(random.random() < 0.6))

print("Printing components")
rdot = Components.graph(kanjis, colors, descriptions, components, anticomponents, radicals)
rdot.render('D:\Japanese\jap_anki\graphs\components', view=(random.random() < 0.4))

print("Printing ORoots")
odot = ORoots.graph(kanjis, colors, descriptions, components)
odot.render('D:\Japanese\jap_anki\graphs\oroots', view=(random.random() < 0.4))

print("All done")
